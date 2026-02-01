import ollama
import json
import pandas as pd
from collections import deque
from datetime import datetime

# configuration
MODEL_NAME = "llama3.2" 

class PaymentOpsAgent:
    def __init__(self):
        self.memory = deque(maxlen=50)
        self.active_interventions = {} 
        self.incident_timeline = []

    def ingest(self, transaction):
        self.memory.append(transaction)
        return self._detect_anomalies()

    def _detect_anomalies(self):
        df = pd.DataFrame(list(self.memory))
        if df.empty: return None

        # check 1: failure rate
        stats = df.groupby('bank')['status'].apply(lambda x: (x == 'FAILED').mean())
        failing_banks = stats[stats > 0.3].index.tolist()
        
        if failing_banks:
            current_rate = stats[failing_banks[0]]
            if len(self.incident_timeline) == 0 or "High Failure Rate" not in self.incident_timeline[-1]:
                self.incident_timeline.append(f"{datetime.now().strftime('%H:%M:%S')} - DETECTED: High Failure Rate ({current_rate:.0%}) on {failing_banks[0]}")
            return {
                "type": "high_failure_rate", 
                "entity": failing_banks[0], 
                "failure_rate": current_rate,
                "recent_errors": df[df['status']=='FAILED']['error_code'].unique().tolist()
            }

        # check 2: high latency
        latency_stats = df.groupby('bank')['latency_ms'].mean()
        slow_banks = latency_stats[latency_stats > 1000].index.tolist()
        
        if slow_banks:
            if len(self.incident_timeline) == 0 or "High Latency" not in self.incident_timeline[-1]:
                self.incident_timeline.append(f"{datetime.now().strftime('%H:%M:%S')} - DETECTED: High Latency ({int(latency_stats[slow_banks[0]])}ms) on {slow_banks[0]}")
            return {
                "type": "high_latency",
                "entity": slow_banks[0],
                "failure_rate": 0.05, 
                "recent_errors": ["SLOW_RESPONSE"]
            }
        return None

    def reason(self, anomaly_signal):
        if not anomaly_signal: return None
        if anomaly_signal['entity'] in self.active_interventions: return None

        print(f"\n[Reasoning] Analyzing {anomaly_signal['entity']}...")

        prompt = f"""
        You are a Payment Reliability Engineer. Analyze this incident.
        Data: {anomaly_signal}
        Task: Diagnose root cause and suggest 'REROUTE' or 'ALERT_OPS'.
        Output JSON ONLY:
        {{
            "root_cause": "brief text",
            "suggested_intervention": "REROUTE" or "ALERT_OPS",
            "confidence_score": 0.0 to 1.0,
            "reasoning": "brief explanation"
        }}
        """

        try:
            response = ollama.chat(model=MODEL_NAME, messages=[{'role': 'user', 'content': prompt}], format='json')
            content = response['message']['content'].strip()
            if content.startswith("```"): content = content.split("```")[1].strip()
            if content.startswith("json"): content = content[4:].strip()
            
            analysis = json.loads(content)
            analysis['affected_entity'] = anomaly_signal['entity']
            analysis['baseline_failure_rate'] = anomaly_signal['failure_rate']

            self.incident_timeline.append(f"{datetime.now().strftime('%H:%M:%S')} - REASONED: {analysis['root_cause']}")
            return analysis
        except Exception as e:
            print(f"❌ LLM Error: {e}")
            return None

    def decide_and_act(self, hypothesis):
        if not hypothesis: return None

        entity = hypothesis['affected_entity']
        suggestion = hypothesis['suggested_intervention']
        confidence = hypothesis['confidence_score']
        
        alternatives = []
        if suggestion == "REROUTE":
            alternatives = ["RETRY_BACKOFF (Rejected: High Risk)", "DO_NOTHING (Rejected: Failures > 30%)"]
        elif suggestion == "ALERT_OPS":
            alternatives = ["REROUTE (Rejected: Low Confidence)", "AUTO_FIX (Rejected: Unsafe)"]

        decision = {
            "status": "SKIPPED",
            "action": "NONE",
            "reason": "Confidence too low",
            "alternatives": alternatives,
            "guardrails": "Check: Conf > 0.7"
        }

        if confidence >= 0.7:
            if suggestion == "REROUTE":
                self.active_interventions[entity] = {
                    "action": "REROUTED_TO_SBI",
                    "baseline_failure_rate": hypothesis['baseline_failure_rate'],
                    "timestamp": datetime.now()
                }
                decision.update({"status": "EXECUTED", "action": f"REROUTE {entity}", "reason": hypothesis['reasoning'], "confidence": confidence, "guardrails": "✅ PASSED: Autonomous"})
                self.incident_timeline.append(f"{datetime.now().strftime('%H:%M:%S')} - ACT: Rerouting {entity}")

            elif suggestion == "ALERT_OPS":
                decision.update({"status": "RECOMMENDED", "action": f"ALERT OPS: {entity}", "reason": hypothesis['reasoning'], "confidence": confidence, "guardrails": "⚠️ MANUAL: High Latency"})
                self.incident_timeline.append(f"{datetime.now().strftime('%H:%M:%S')} - REC: Alert Ops for {entity}")
        
        return decision

    def learn(self):
        if not self.active_interventions: return None
        df = pd.DataFrame(list(self.memory))
        report = {}
        for entity, data in list(self.active_interventions.items()):
            recent_tx = df.tail(10)
            if recent_tx.empty: continue
            current_fail = (recent_tx['status'] == 'FAILED').mean()
            improvement = data['baseline_failure_rate'] - current_fail
            report[entity] = {
                "baseline_failure": f"{data['baseline_failure_rate']*100:.0f}%",
                "current_failure": f"{current_fail*100:.0f}%",
                "impact": f"{improvement*100:.0f}% Improvement"
            }
        return report

    def generate_summary(self):
        return f"\n=== INCIDENT SUMMARY ===\nEvents: {len(self.incident_timeline)}\nState: {list(self.active_interventions.keys())}\nTimeline:\n" + "\n".join(self.incident_timeline)