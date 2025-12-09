"""
Transactions Router
Endpoints for pacs.008, pacs.002 quick-status, and full-transaction
"""
from fastapi import APIRouter, Form
from typing import Optional
from datetime import datetime
import time

from services.tms_client import tms_client
from utils.payload_generator import generate_pacs008, generate_pacs002
from config import VALID_STATUS_CODES
from models.schemas import (
    Pacs008Response,
    QuickStatusResponse,
    FullTransactionResponse,
    ErrorResponse
)

router = APIRouter(prefix="/api/test", tags=["Transactions"])

# In-memory storage reference
test_history = []


def set_history_reference(history_list):
    global test_history
    test_history = history_list


@router.post(
    "/pacs008",
    summary="Send pacs.008 Transaction",
    description="Send a test pacs.008 (Credit Transfer) message to Tazama TMS"
)
async def test_pacs008(
    debtor_account: Optional[str] = Form(None, description="Debtor account ID"),
    amount: Optional[str] = Form(None, description="Transaction amount"),
    debtor_name: Optional[str] = Form(None, description="Debtor name")
):
    """Send test pacs.008 transaction"""
    try:
        amt = float(amount) if amount else None
        if debtor_account and not debtor_account.strip():
            debtor_account = None
        if debtor_name and not debtor_name.strip():
            debtor_name = None

        payload = generate_pacs008(debtor_account, amt, debtor_name)
        status_code, response_time, response_data = tms_client.send_pacs008(payload)
        
        test_record = {
            "timestamp": datetime.now().isoformat(),
            "type": "pacs.008",
            "status": status_code,
            "response_time_ms": response_time,
            "success": status_code == 200,
            "message_id": payload.get("FIToFICstmrCdtTrf", {}).get("GrpHdr", {}).get("MsgId"),
            "end_to_end_id": payload.get("FIToFICstmrCdtTrf", {}).get("CdtTrfTxInf", {}).get("PmtId", {}).get("EndToEndId")
        }
        test_history.append(test_record)
        
        return {
            "status": "success" if status_code == 200 else "error",
            "http_code": status_code,
            "response_time_ms": response_time,
            "payload_sent": payload,
            "tms_response": response_data,
            "test_record": test_record
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.post(
    "/quick-status",
    summary="Quick Status Test",
    description="Send pacs.008 + pacs.002 with selectable status code (ACCC/ACSC/RJCT)"
)
async def test_quick_status(
    status_code: str = Form("ACCC", description="Status code: ACCC, ACSC, or RJCT"),
    debtor_account: Optional[str] = Form(None, description="Debtor account ID"),
    amount: Optional[float] = Form(None, description="Transaction amount")
):
    """
    Quick Test: Send pacs.008 + pacs.002 with selectable status code.
    Supports ACCC (Accepted), ACSC (Settled), RJCT (Rejected)
    """
    if status_code not in VALID_STATUS_CODES:
        return {
            "status": "error",
            "message": f"Invalid status code. Must be one of: {', '.join(VALID_STATUS_CODES)}"
        }
    
    pacs008_payload = generate_pacs008(debtor_account, amount)
    message_id = pacs008_payload.get("FIToFICstmrCdtTrf", {}).get("GrpHdr", {}).get("MsgId")
    end_to_end_id = pacs008_payload.get("FIToFICstmrCdtTrf", {}).get("CdtTrfTxInf", {}).get("PmtId", {}).get("EndToEndId")
    
    try:
        start_time = datetime.now()
        
        # Send pacs.008
        status_008, _, _ = tms_client.send_pacs008(pacs008_payload)
        
        if status_008 == 200:
            time.sleep(0.3)
            
            pacs002_payload = generate_pacs002(message_id, end_to_end_id, status_code)
            status_002, pacs002_time, response_002 = tms_client.send_pacs002(pacs002_payload)
            
            total_time = (datetime.now() - start_time).total_seconds() * 1000
            
            test_record = {
                "timestamp": start_time.isoformat(),
                "type": f"Quick Test ({status_code})",
                "status": status_002,
                "response_time_ms": total_time,
                "success": status_002 == 200,
                "message_id": message_id
            }
            test_history.append(test_record)
            
            return {
                "status": "success" if status_002 == 200 else "error",
                "http_code": status_002,
                "response_time_ms": total_time,
                "payload_sent": pacs002_payload,
                "tms_response": response_002,
                "test_record": test_record
            }
        else:
            return {
                "status": "error",
                "http_code": status_008,
                "message": "pacs.008 failed"
            }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.post(
    "/full-transaction",
    summary="Full Transaction Test",
    description="Send complete transaction flow: pacs.008 followed by pacs.002 ACCC"
)
async def test_full_transaction(
    debtor_account: Optional[str] = Form(None, description="Debtor account ID"),
    amount: Optional[float] = Form(None, description="Transaction amount")
):
    """Send complete transaction (pacs.008 + pacs.002 ACCC)"""
    results = {
        "pacs008": None,
        "pacs002": None,
        "overall_status": "pending"
    }
    
    pacs008_payload = generate_pacs008(debtor_account, amount)
    message_id = pacs008_payload.get("FIToFICstmrCdtTrf", {}).get("GrpHdr", {}).get("MsgId")
    end_to_end_id = pacs008_payload.get("FIToFICstmrCdtTrf", {}).get("CdtTrfTxInf", {}).get("PmtId", {}).get("EndToEndId")
    
    try:
        status_008, time_008, response_008 = tms_client.send_pacs008(pacs008_payload)
        
        results["pacs008"] = {
            "status": status_008,
            "success": status_008 == 200,
            "response": response_008
        }
        
        if status_008 == 200:
            time.sleep(0.5)
            
            pacs002_payload = generate_pacs002(message_id, end_to_end_id, "ACCC")
            status_002, time_002, response_002 = tms_client.send_pacs002(pacs002_payload)
            
            results["pacs002"] = {
                "status": status_002,
                "success": status_002 == 200,
                "response": response_002
            }
            
            results["overall_status"] = "success" if status_002 == 200 else "partial"
        else:
            results["overall_status"] = "failed"
        
        return results
        
    except Exception as e:
        results["overall_status"] = "error"
        results["error"] = str(e)
        return results
