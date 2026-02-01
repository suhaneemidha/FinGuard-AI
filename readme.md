# 🛡️ FinGuard AI – Payment Operations Center

FinGuard AI is a **local, agent-driven payment reliability simulator** that monitors live transaction streams, detects failures or latency spikes, reasons about root causes using an LLM (via Ollama), and autonomously intervenes using guarded decision logic.

The system runs entirely in the terminal with a real-time dashboard and a transparent **Observe → Reason → Decide → Act** loop.

---

## 💡 Problem
In real-world fintech systems, payment providers (HDFC, ICICI, SBI, etc.) frequently experience partial outages or latency spikes. These incidents are often **short-lived but costly**, and manual intervention is too slow to react at transaction-level granularity.

---

## 🤖 Solution
FinGuard AI simulates a payment environment and deploys an **autonomous Payment Operations Agent** that:

*   **Observes** live transaction traffic.
*   **Detects** abnormal failure rates or latency.
*   **Reasons** about root cause using a local LLM.
*   **Decides** whether to intervene based on confidence thresholds.
*   **Acts** by rerouting traffic in the simulation.
*   **Learns** from post-intervention outcomes.

All decisions are **explainable and guarded**, not blind automation.

---

## 🏛️ Agent Architecture (Glass Box)

### 1. Observe
- Tracks per-bank failure rates.
- Monitors rolling latency windows.
- Maintains short-term transactional memory.

### 2. Reason
- Sends anomaly context to a local LLM (Ollama).
- Requests structured JSON diagnosis.
- Extracts root cause, confidence, and recommendation.

### 3. Decide
- Applies hard guardrails (confidence ≥ 0.7).
- Rejects unsafe or low-confidence actions.
- Logs rejected alternatives for transparency.

### 4. Act
- Executes simulated rerouting (e.g., HDFC → SBI).
- Records intervention in an incident timeline.

### 5. Learn
- Compares pre- vs post-intervention failure rates.
- Reports measurable impact of agent actions.

---

## ⚡ Simulation Scenarios
*   **HDFC Outage:** High failure rate for UPI transactions.
*   **ICICI Latency Spike:** Sustained response delays.
*   **Mixed Traffic:** Random distribution of UPI, Credit Card, and Net Banking.
*   **Controlled Randomness:** Real-world "noise" to emulate production systems.

---

## 🖥️ Live Terminal Dashboard
Built using `rich`, the dashboard displays:
*   Live transaction stream.
*   Bank health status bars.
*   Payment method distribution.
*   Real-time latency chart.
*   Kernel-style system logs.
*   Active AI decisions with confidence scores.
*   Incident timeline.

---

## 🛠️ Tech Stack
*   **Language:** Python 3
*   **LLM Runtime:** Ollama (local)
*   **Model:** llama3.2
*   **UI:** Rich (terminal-based dashboard)
*   **Data Handling:** Pandas
*   **Architecture:** Agentic (Observe–Reason–Decide–Act)

---

## ⚙️ Installation & Setup

### 1. Install Ollama (one-time)
Download from: [https://ollama.com/](https://ollama.com/)

Pull the required model:
```bash
ollama pull llama3.2
Ensure the Ollama application is running in the background.

2. Clone the repository
code
Bash
git clone <your-repository-url>
cd <project-folder-name>
3. Create and activate virtual environment
code
Bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
4. Install dependencies
code
Bash
pip install -r requirements.txt
5. Run the system
code
Bash
python main.py
Press Ctrl+C to stop and view the final incident summary.

📁 Project Structure
code
Text
.
├── main.py          # Terminal dashboard + orchestration
├── agent_core.py    # Autonomous payment operations agent
├── simulator.py     # Transaction and outage simulation
├── requirements.txt # Project dependencies
├── README.md        # Documentation
└── venv/            # Virtual environment (gitignored)
🛡️ Design Notes
Reasoning-only LLM: The LLM is used for diagnosis, never for direct code execution.
Deterministic Guardrails: All actions are gated by traditional code logic.
Zero External Dependencies: No external APIs or keys required.
Privacy-First: No real payment data is used; runs fully offline.
🎬 How to Observe the Agent
Watch failure rates spike during the simulated HDFC outage.
See the agent reason and provide a JSON-based diagnosis in the middle panel.
Monitor the Action: Watch the "Reroute" decision take effect.
Observe Recovery: See the "Bank Health" bars return to green after intervention.
⚠️ Disclaimer
This project is a simulation and research prototype intended to demonstrate agentic AI behavior in payment reliability scenarios. It does not interact with real banks or actual financial payment gateways.
