from fastapi import FastAPI, HTTPException, Request
from fastapi import FastAPI, HTTPException, Request
# from models import Pacs008, FIToFICstmrCdtTrf # Removed to avoid validation errors
import logging
from datetime import datetime, timedelta
from collections import deque, defaultdict
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger("TazamaMockTMS")

app = FastAPI(title="Tazama Mock TMS")

# Logic: In-memory transaction history for velocity rules
# Map: AccountNumber -> List of timestamps
tx_history = defaultdict(lambda: deque())

VELOCITY_LIMIT = 5
VELOCITY_WINDOW_SECONDS = 60

@app.get("/")
async def health_check():
    return {"status": "up", "service": "Tazama Mock TMS"}

@app.post("/v1/evaluate/iso20022/pacs.008.001.10")
async def evaluate_transaction(request: Request):
    """
    Simulate Tazama Evaluation.
    Rules:
    1. Schema Validation (Pydantic will handle this if we used models, but body structure varies, simplify for now)
    2. Velocity Rule (Rule 901): > 5 tx per minute per account = REJECT
    """
    try:
        body = await request.json()
        
        # 1. Extract Data
        try:
            root = body.get("FIToFICstmrCdtTrf", {})
            # Handle list or dict for CdtTrfTxInf (ISO allows list, simplified here)
            tx_node = root.get("CdtTrfTxInf")
            if isinstance(tx_node, list):
                tx_node = tx_node[0]
            
            # Extract Debtor Account (for velocity key)
            # Try IBAN first, then Othr
            dbtr_acct = tx_node.get("DbtrAcct", {}).get("Id", {})
            account_id = "UNKNOWN"
            
            if "IBAN" in dbtr_acct:
                account_id = dbtr_acct["IBAN"]
            elif "Othr" in dbtr_acct and len(dbtr_acct["Othr"]) > 0:
                account_id = dbtr_acct["Othr"][0].get("Id", "UNKNOWN")
            
            amount = float(tx_node.get("IntrBkSttlmAmt", {}).get("Amt", {}).get("Amt", 0))
            
        except Exception as e:
            # If parsing fails, just accept it for now or return 400
            print(f"⚠️ Parsing Error: {e}")
            return {"statusCode": 200, "message": "Transaction is valid (Parsing Warning)"}

        print(f"💰 Processing Tx from Account: {account_id} | Amount: {amount}")

        # 2. Check Velocity Rule (Rule 901)
        now = datetime.now()
        timestamps = tx_history[account_id]
        
        # Remove old transactions (> 1 minute ago)
        while timestamps and (now - timestamps[0]) > timedelta(seconds=VELOCITY_WINDOW_SECONDS):
            timestamps.popleft()
            
        # Add current transaction
        timestamps.append(now)
        
        # Check Count
        if len(timestamps) > VELOCITY_LIMIT:
            print(f"🚨 FRAUD ALERT: Velocity Limit Exceeded for {account_id}! Count: {len(timestamps)}")
            return {
                "statusCode": 406, # Not Acceptable / Fraud
                "message": f"Suspicious activity detected: Velocity limit exceeded (Rule 901). Count {len(timestamps)}/{VELOCITY_LIMIT}",
                "rule_id": "901",
                "typology": "Velocity",
                "status": "RJCT"
            }

        # 3. Check High Value (Rule 001) - Optional
        if amount > 1000000000: # 1 Miliar
             return {
                "statusCode": 200, 
                "message": "Suspicious activity detected: High Value Transaction",
                "status": "ACTC" 
            }

        # If Valid
        return {
            "statusCode": 200, 
            "message": "Transaction is valid",
            "data": body
        }

    except Exception as e:
        logger.error(f"Error: {e}")
        return {"statusCode": 500, "message": str(e)}

@app.post("/v1/evaluate/iso20022/pacs.002.001.12")
async def evaluate_pacs002(request: Request):
    return {"statusCode": 200, "message": "Status Accepted"}
