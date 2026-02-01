import time
import random
import pandas as pd
from collections import deque
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich import box
from rich.progress import BarColumn, Progress

from simulator import PaymentSimulator
from agent_core import PaymentOpsAgent

# setup
console = Console()
sim = PaymentSimulator()
agent = PaymentOpsAgent()

# ui state
tx_history = deque(maxlen=40) 
latency_history = deque([100]*40, maxlen=40)
kernel_log = deque(maxlen=8)

def update_kernel_log():
    msgs = [
        "Verifying SSL handshake...", "Allocating memory block 0x4F...",
        "Garbage collection started...", "Heartbeat ack from Gateway...",
        "Flushing log buffer...", "Updating heuristic weights...",
        "Packet inspection complete...", "Syncing active threads..."
    ]
    if random.random() < 0.3:
        kernel_log.append(f"[dim]{datetime.now().strftime('%H:%M:%S.%f')[:-3]} [INFO] {random.choice(msgs)}[/]")

def get_ascii_chart():
    bars = "  ▂▃▄▅▆▇█"
    chart = ""
    for val in latency_history:
        normalized = min(int((val / 2000) * 8), 8)
        color = "green" if normalized < 3 else "yellow" if normalized < 6 else "red"
        chart += f"[{color}]{bars[normalized]}[/]"
    return chart

def get_header():
    grid = Table.grid(expand=True)
    grid.add_column(justify="left", ratio=1)
    grid.add_column(justify="right", ratio=1)
    
    title = Text(" 🛡️ FinGuard AI | PAYMENT OPERATIONS CENTER ", style="bold white on blue")
    stats = Text(f"UPTIME: {datetime.now().strftime('%H:%M:%S')} | CPU: {random.randint(12,40)}% | RAM: 1.2GB ", style="bold cyan on black")
    
    grid.add_row(title, stats)
    return Panel(grid, style="white on blue", box=box.HEAVY_HEAD)

def get_traffic_table():
    # expand=True ensures the table takes full width
    table = Table(expand=True, box=box.SIMPLE, padding=(0,0), show_header=True)
    table.add_column("TIME", style="dim", width=8)
    table.add_column("TX ID", style="cyan", width=8)
    table.add_column("BANK", style="magenta", width=6)
    table.add_column("STATUS", width=8)
    table.add_column("LATENCY", justify="right")

    # show newest at the top ([::-1])
    for tx in list(tx_history)[::-1]:
        ts = tx['timestamp'].split("T")[1][:8]
        status = Text("PASS", style="bold green") if tx['status'] == "SUCCESS" else Text("FAIL", style="bold white on red")
        
        lat_val = tx['latency_ms']
        lat_style = "green" if lat_val < 400 else "yellow" if lat_val < 1000 else "red"
        lat = f"[{lat_style}]{lat_val}ms[/]"
        
        table.add_row(ts, tx['transaction_id'], tx['bank'], status, lat)

    return Panel(table, title=" [bold]LIVE TRAFFIC STREAM[/] ", border_style="cyan", box=box.ROUNDED)

def get_payment_mix_panel():
    df = pd.DataFrame(list(agent.memory))
    
    grid = Table.grid(expand=True, padding=(0,1))
    grid.add_column(ratio=2) 
    grid.add_column(ratio=4) 
    grid.add_column(ratio=1, justify="right") 

    if not df.empty and 'method' in df.columns:
        counts = df['method'].value_counts(normalize=True)
    else:
        counts = {}

    meta = {
        "UPI": "cyan", 
        "CREDIT_CARD": "magenta", 
        "NET_BANKING": "yellow"
    }

    for method, pct in counts.items():
        color = meta.get(method, "white")
        filled = int(pct * 20)
        bar = f"[{color}]{'━' * filled}[dim]{'━' * (20 - filled)}[/]"
        grid.add_row(
            f"[bold {color}]{method}[/]", 
            bar, 
            f"{int(pct*100)}%"
        )
        
    return Panel(grid, title=" [bold]PAYMENT CHANNEL MIX[/] ", border_style="dim white", box=box.ROUNDED)

def get_brain_panel(decision):
    if decision and (decision.get('status') == "EXECUTED" or decision.get('status') == "RECOMMENDED"):
        color = "green" if decision['status'] == "EXECUTED" else "yellow"
        border = "bright_green" if decision['status'] == "EXECUTED" else "yellow"
        
        content = Align.center(Text(f"\n⚠ INTERVENTION {decision['status']} ⚠\n", style=f"bold {color} reverse"), vertical="middle")
        
        grid = Table.grid(expand=True, padding=(1, 2))
        grid.add_column(justify="right", style="dim white")
        grid.add_column(justify="left", style="bold white")
        
        grid.add_row("ACTION:", f"[{color}]{decision['action']}[/]")
        grid.add_row("REASON:", decision['reason'])
        
        conf = decision.get('confidence', 0)
        conf_str = f"[{'|' * int(conf*40)}{'.' * (40 - int(conf*40))}] {int(conf*100)}%"
        grid.add_row("CONFIDENCE:", f"[cyan]{conf_str}[/]")

        final_content = Layout()
        final_content.split_column(Layout(content, size=4), Layout(grid))
        return Panel(final_content, title=" [bold blink]⚠ AI DECISION ACTIVE[/] ", border_style=border, box=box.DOUBLE)
    else:
        chart_str = get_ascii_chart()
        chart_panel = Panel(Align.center(f"\n{chart_str}\n\n[dim]REAL-TIME NETWORK LATENCY (20s Window)[/]"), box=box.SIMPLE)
        log_text = "\n".join(list(kernel_log))
        log_panel = Panel(log_text, title="[bold dim]SYSTEM KERNEL LOG[/]", border_style="dim white", box=box.SIMPLE)

        layout = Layout()
        layout.split_column(Layout(chart_panel, ratio=2), Layout(log_panel, ratio=1))
        return Panel(layout, title=" [bold green]SYSTEM MONITORING ACTIVE[/] ", border_style="green", box=box.ROUNDED)

def get_stats_panel(learning_report):
    df = pd.DataFrame(list(agent.memory))
    grid = Table.grid(expand=True, padding=(0, 1))
    grid.add_column(ratio=2)
    grid.add_column(ratio=4)
    grid.add_column(ratio=1)

    for bank in ["HDFC", "ICICI", "SBI", "AXIS"]:
        health = 100
        if not df.empty:
            bank_data = df[df['bank'] == bank]
            if not bank_data.empty:
                fail_rate = (bank_data['status'] == 'FAILED').mean()
                health = 100 - (fail_rate * 100)
        
        color = "green" if health > 80 else "yellow" if health > 50 else "red"
        filled = int((health / 100) * 12)
        bar = f"[{color}]{'█' * filled}[dim white]{'░' * (12 - filled)}[/]"
        grid.add_row(bank, bar, f"[{color}]{int(health)}%[/]")
    
    health_panel = Panel(grid, title="[bold]BANK HEALTH[/]", border_style="blue", box=box.ROUNDED)

    impact_text = Text("\nWaiting for incidents...", style="dim")
    if learning_report:
        impact_text = Text("")
        for entity, data in learning_report.items():
             impact_text.append(f"✔ {entity}\n", style="bold green")
             impact_text.append(f"  Prev: {data['baseline_failure']}\n", style="red")
             impact_text.append(f"  Now:  {data['current_failure']}\n", style="green")

    impact_panel = Panel(impact_text, title="[bold]IMPACT[/]", border_style="white", box=box.ROUNDED)

    layout = Layout()
    layout.split_column(Layout(health_panel, ratio=3), Layout(impact_panel, ratio=2))
    return layout

def generate_dashboard(decision, learning_report, timeline):
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body", ratio=1),
        Layout(name="footer", size=10)
    )
    
    layout["header"].update(get_header())

    # left column: traffic (3 parts) and mix (1 part)
    left_column = Layout()
    left_column.split_column(
        Layout(get_traffic_table(), name="traffic_list", ratio=3),
        Layout(get_payment_mix_panel(), name="traffic_stats", ratio=1)
    )

    layout["body"].split_row(
        Layout(left_column, name="left", ratio=3),
        Layout(get_brain_panel(decision), name="middle", ratio=4),
        Layout(get_stats_panel(learning_report), name="right", ratio=2)
    )

    timeline_text = "\n".join(timeline[-7:]) 
    layout["footer"].update(Panel(timeline_text, title=" [bold]INCIDENT TIMELINE[/] ", style="white on black", box=box.DOUBLE_EDGE))
    
    return layout

def main():
    console.clear()
    console.show_cursor(False)
    try:
        with Live(refresh_per_second=4, screen=True) as live:
            while True:
                tx = sim.generate_transaction()
                if "HDFC" in agent.active_interventions and tx['bank'] == "HDFC":
                    tx['bank'] = "SBI"
                    tx['status'] = "SUCCESS" 
                    tx['latency_ms'] = 120
                
                tx_history.append(tx)
                latency_history.append(tx['latency_ms'])
                update_kernel_log()

                anomaly = agent.ingest(tx)
                decision = None
                if anomaly:
                    hypothesis = agent.reason(anomaly)
                    if hypothesis:
                        decision = agent.decide_and_act(hypothesis)
                report = agent.learn()

                live.update(generate_dashboard(decision, report, agent.incident_timeline))
                time.sleep(0.5)
    except KeyboardInterrupt:
        console.print(agent.generate_summary())
        console.show_cursor(True)

if __name__ == "__main__":
    main()