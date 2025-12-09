import requests
import time
import sys
from utils.iso_generator import create_payload
from faker import Faker

fake = Faker('id_ID')

TARGET_URL = "http://localhost:8000/v1/evaluate/iso20022/pacs.008.001.10"

def run_velocity_attack():
    print("🚀 Starting Velocity Attack Simulation...")
    
    # 1. Define one Attacker IBAN (Debtor Account)
    attacker_iban = fake.iban()
    print(f"😈 Attacker Account Locked: {attacker_iban}\n")
    
    # 2. Run loop of 20 transactions
    for i in range(1, 21):
        # Generate payload with same debtor account and random amount
        amount = round(fake.random.uniform(100, 10000), 2)
        payload = create_payload(amount=amount, debtor_account=attacker_iban)
        
        try:
            response = requests.post(TARGET_URL, json=payload)
            response.raise_for_status()
            
            # Colorful log
            print(f"⚠️  [Tx {i}/20] Attack Transaction sent | Status: {response.json().get('status')}")
        except Exception as e:
            print(f"❌ [Tx {i}/20] Failed: {e}")
            
        # 3. Sleep to mimic high-frequency bot
        time.sleep(0.05)

    print("\n✅ Simulation Complete.")

if __name__ == "__main__":
    run_velocity_attack()
