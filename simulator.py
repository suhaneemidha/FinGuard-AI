import random
import uuid
from datetime import datetime

class PaymentSimulator:
    def __init__(self):
        self.banks = ["HDFC", "ICICI", "SBI", "AXIS"]
        self.methods = ["UPI", "CREDIT_CARD", "NET_BANKING"]
        self.transaction_count = 0 
        self.active_outage = False

    def generate_transaction(self):
        self.transaction_count += 1
        
        # 1. HDFC Outage (Tx 15-50)
        if self.transaction_count > 15 and self.transaction_count < 50:
            self.active_outage = True
        else:
            self.active_outage = False

        # 2. ICICI Latency Spike (Tx 60-90)
        active_latency_spike = False
        if self.transaction_count > 60 and self.transaction_count < 90:
            active_latency_spike = True

        tx_id = str(uuid.uuid4())[:8]
        bank = random.choice(self.banks)
        method = random.choice(self.methods)
        amount = round(random.uniform(100, 5000), 2)
        
        # default behavior
        status = "SUCCESS"
        error_code = None
        latency = random.randint(50, 400) 

        # Scenario 1: HDFC Failure
        if self.active_outage and bank == "HDFC" and method == "UPI":
            if random.random() < 0.8: 
                status = "FAILED"
                error_code = "ERR_BANK_TIMEOUT"
                latency = random.randint(2000, 5000)

        # Scenario 2: ICICI Latency
        if active_latency_spike and bank == "ICICI":
            latency = random.randint(1500, 4000)
            if random.random() < 0.1: 
                status = "FAILED"
                error_code = "ERR_LATENCY_TIMEOUT"

        return {
            "transaction_id": tx_id,
            "timestamp": datetime.now().isoformat(),
            "bank": bank,
            "method": method,
            "amount": amount,
            "status": status,
            "latency_ms": latency,
            "error_code": error_code,
            "retry_count": 0
        }