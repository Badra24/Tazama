
import os

# TMS Service Configuration
TMS_BASE_URL = os.getenv("TMS_BASE_URL", "http://localhost:5001")
SOURCE_TENANT_ID = os.getenv("SOURCE_TENANT_ID", "1010")

# API Endpoints
TMS_ENDPOINTS = {
    "health": "/",
    "pain001": "/v1/evaluate/iso20022/pain.001.001.11",
    "pain013": "/v1/evaluate/iso20022/pain.013.001.09",
    "pacs008": "/v1/evaluate/iso20022/pacs.008.001.10",
    "pacs002": "/v1/evaluate/iso20022/pacs.002.001.12"
}

# Server Configuration
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", "8080"))

# Timeout Configuration
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))

# Valid Status Codes for pacs.002
VALID_STATUS_CODES = ["ACCC", "ACSC", "RJCT"]
