🛡️ FinGuard AI – Payment Operations Center
FinGuard AI is a local, agent-driven payment reliability simulator that monitors live transaction streams, detects failures or latency spikes, reasons about root causes using an LLM (via Ollama), and autonomously intervenes using guarded decision logic.

The system runs entirely in the terminal with a real-time dashboard and a transparent Observe → Reason → Decide → Act loop.

💡 Problem
In real-world fintech systems, payment providers frequently experience partial outages. These incidents are often short-lived but costly, and manual intervention is too slow to react.

🤖 Solution
FinGuard AI deploys an autonomous Payment Operations Agent that:

Observes live transaction traffic.
Detects abnormal failure rates or latency.
Reasons about root cause using a local LLM.
Decides whether to intervene based on confidence thresholds.
Acts by rerouting traffic in the simulation.
⚙️ Installation & Setup

1. Install Ollama (one-time)
Download from: https://ollama.com/

Pull the required model in your terminal:

code
Bash
ollama pull llama3.2
2. Clone the repository
code
Bash
git clone <your-repository-url>
cd <project-folder-name>
3. Create and activate virtual environment
code
Bash
python3 -m venv venv
source venv/bin/activate
4. Install dependencies
code
Bash
pip install -r requirements.txt
5. Run the system
code
Bash
python main.py
📁 Project Structure
code
Text
.
├── main.py          # Terminal dashboard + orchestration
├── agent_core.py    # Autonomous payment operations agent
├── simulator.py     # Transaction and outage simulation
├── requirements.txt # Dependencies
└── README.md        # Documentation
🛠️ Tech Stack
Language: Python 3
LLM Runtime: Ollama (local)
Model: llama3.2
UI: Rich (terminal-based dashboard)
Data Handling: Pandas
🎬 How to Observe the Agent
Watch failure rates spike during the simulated HDFC outage.
See the agent reason and provide a diagnosis in the middle panel.
Monitor the Action: Watch the "Reroute" decision take effect.
Observe Recovery: See the "Bank Health" bars return to green after intervention.
⚠️ Disclaimer
This project is a simulation and research prototype intended to demonstrate agentic AI behavior. It does not interact with real banks or actual financial payment gateways.
