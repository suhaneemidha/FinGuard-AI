# 🛡️ FinGuard AI – Payment Operations Center

FinGuard AI is a **local, agent-driven payment reliability simulator** that monitors live transaction streams, detects failures or latency spikes, reasons about root causes using an LLM (via Ollama), and autonomously intervenes using guarded decision logic.

The system runs entirely in the terminal with a real-time dashboard and a transparent Observe → Reason → Decide → Act loop.

---

## 💡 Problem

In real-world fintech systems, payment providers (HDFC, ICICI, SBI, etc.) frequently experience partial outages or latency spikes.  
These incidents are often **short-lived but costly**, and manual intervention is too slow to react at transaction-level granularity.

---

## 🤖 Solution

FinGuard AI simulates a payment environment and deploys an **autonomous Payment Operations Agent** that:

- Observes live transaction traffic
- Detects abnormal failure rates or latency
- Reasons about root cause using an LLM
- Decides whether to intervene based on confidence thresholds
- Acts by rerouting traffic in the simulation
- Learns from post-intervention outcomes

All decisions are **explainable and guarded**, not blind automation.

---

## 🏛️ Agent Architecture (Glass Box)

### Observe
- Tracks per-bank failure rates
- Monitors rolling latency windows
- Maintains short-term transactional memory

### Reason
- Sends anomaly context to a local LLM (Ollama)
- Requests structured JSON diagnosis
- Extracts root cause, confidence, and recommendation

### Decide
- Applies hard guardrails (confidence ≥ 0.7)
- Rejects unsafe or low-confidence actions
- Logs rejected alternatives for transparency

### Act
- Executes simulated rerouting (e.g., HDFC → SBI)
- Records intervention in an incident timeline

### Learn
- Compares pre- vs post-intervention failure rates
- Reports measurable impact of agent actions

---

## ⚡ Simulation Scenarios

- **HDFC outage**: High failure rate for UPI transactions
- **ICICI latency spike**: Sustained response delays
- **Mixed traffic**: UPI, Credit Card, Net Banking
- **Controlled randomness** to emulate real systems

---

## 🖥️ Live Terminal Dashboard

Built using `rich`, the dashboard displays:

- Live transaction stream
- Bank health bars
- Payment method distribution
- Real-time latency chart
- Kernel-style system logs
- Active AI decisions with confidence scores
- Incident timeline

Runs fully inside the terminal — no browser required.

---

## 🛠️ Tech Stack

- **Language**: Python 3
- **LLM Runtime**: Ollama (local)
- **Model**: llama3.2
- **UI**: rich (terminal-based dashboard)
- **Data Handling**: pandas
- **Architecture**: Agentic (Observe–Reason–Decide–Act)

---

## ⚙️ Installation & Setup

### 1. Install Ollama (one-time)
Download from: https://ollama.com/

Pull the model:
```bash
ollama pull llama3.2
Ensure Ollama is running.
2. Clone the repository
git clone <your-repository-url>
cd <project-folder-name>
3. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate
4. Install dependencies
pip install -r requirements.txt
5. Run the system
python main.py
Press Ctrl+C to stop and view the incident summary.
📁 Project Structure
.
├── main.py          # Terminal dashboard + orchestration
├── agent_core.py    # Autonomous payment operations agent
├── simulator.py     # Transaction and outage simulation
├── requirements.txt
├── README.md
└── venv/            # Virtual environment (gitignored)
🛡️ Design Notes
LLM is used only for reasoning, never direct execution
All actions are guarded by deterministic logic
No external APIs or API keys required
No real payment data is used
Fully offline after model download
🎬 How to Observe the Agent
Watch failure rates spike during simulated outages
See the agent reason and intervene in real time
Observe recovery and health improvement post-action
Inspect confidence scores and rejected alternatives
⚠️ Disclaimer
This project is a simulation and research prototype intended to demonstrate agentic AI behavior in payment reliability scenarios.
It does not interact with real banks or payment systems.