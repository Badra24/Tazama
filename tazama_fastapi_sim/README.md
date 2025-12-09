# Tazama FastAPI Simulation

Mock Transaction Monitoring Service (TMS) untuk testing dan development fraud detection scenarios tanpa perlu deploy full Tazama stack.

## 🎯 Tujuan

Project ini menyediakan **lightweight simulation environment** untuk:
- ✅ Test format ISO 20022 message (pacs.008.001.10)
- ✅ Simulasi fraud attack patterns (velocity attack)
- ✅ Quick development & debugging
- ✅ Demo fraud scenarios

## 📁 Struktur Project

```
tazama_fastapi_sim/
├── main.py                 # Mock TMS Server (FastAPI)
├── simulation.py           # Velocity Attack Client
├── models.py               # ISO 20022 Pydantic Models
├── utils/
│   ├── __init__.py
│   └── iso_generator.py    # Payload Generator (Faker)
├── requirements.txt        # Dependencies
├── run.sh                  # Quick Start Script
└── README.md              # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### Running the Simulation

**Option 1: Using the script (recommended)**
```bash
./run.sh
```

**Option 2: Manual**
```bash
# Terminal 1: Start Mock TMS Server
uvicorn main:app --port 8000

# Terminal 2: Run Attack Simulation
python simulation.py
```

## 📊 Komponen

### 1. Mock TMS Server (`main.py`)

Meniru behavior TMS Service yang real dengan endpoint:

```
POST /v1/evaluate/iso20022/pacs.008.001.10
```

**Features:**
- Strict ISO 20022 validation menggunakan Pydantic
- Logging transaction details (EndToEndId & Amount)
- Response: `{"status": "ACTC", "reason": "Passed Validation"}`

**Example Request:**
```bash
curl -X POST http://localhost:8000/v1/evaluate/iso20022/pacs.008.001.10 \
  -H "Content-Type: application/json" \
  -d @sample_payload.json
```

### 2. Attack Simulator (`simulation.py`)

Generate **Velocity Attack** scenario:
- 🎯 1 Attacker IBAN (debtor account yang sama)
- 🔄 20 transaksi berturut-turut
- ⏱️ Delay 50ms antar request (high-frequency pattern)
- 💰 Random amounts (IDR 100 - 10,000)

**Output Example:**
```
🚀 Starting Velocity Attack Simulation...
😈 Attacker Account Locked: GB19IVBT76290014170742

💰 Received Transaction: EndToEndId=PMT4B7D1DD9, Amount=4482.19
⚠️  [Tx 1/20] Attack Transaction sent | Status: ACTC
💰 Received Transaction: EndToEndId=PMT353A57FB, Amount=890.81
⚠️  [Tx 2/20] Attack Transaction sent | Status: ACTC
...
✅ Simulation Complete.
```

### 3. ISO 20022 Models (`models.py`)

Pydantic schemas untuk `pacs.008.001.10`:

```python
Pacs008Message
├── GrpHdr (GroupHeader)
│   ├── MsgId
│   ├── CreDtTm
│   ├── NbOfTx
│   └── InitgPty
└── CdtTrfTxInf (CreditTransferTransactionInformation)
    ├── PmtId
    ├── IntrBkSttlmAmt
    │   ├── Amount
    │   └── Ccy
    ├── Dbtr (Party)
    ├── DbtrAcct (Account)
    ├── DbtrAgt (Agent)
    ├── CdtrAgt (Agent)
    ├── Cdtr (Party)
    └── CdtrAcct (Account)
```

### 4. Payload Generator (`utils/iso_generator.py`)

Generate realistic Indonesian transaction data:

```python
from utils.iso_generator import create_payload

# Random creditor
payload = create_payload(amount=5000.00)

# Fixed debtor (velocity attack)
payload = create_payload(
    amount=5000.00, 
    debtor_account="GB19IVBT76290014170742"
)
```

**Features:**
- `Faker('id_ID')` untuk data Indonesia
- Generate IBAN, nama, BIC codes
- Configurable debtor account untuk attack patterns

## 🔍 Use Cases

### ✅ Kapan Menggunakan Mock?

| Scenario | Recommended |
|----------|-------------|
| Testing payload format | ✅ Mock |
| Quick development iteration | ✅ Mock |
| Demo fraud patterns | ✅ Mock |
| Debug client code | ✅ Mock |
| **Real fraud detection** | ❌ Use Full Stack |
| **Performance testing** | ❌ Use Full Stack |
| **Integration testing** | ❌ Use Full Stack |

### Development Workflow

```
1. Test format di Mock     →  tazama_fastapi_sim (30 detik)
2. Integration test        →  Full-Stack-Docker-Tazama (5 menit)
3. Production deployment   →  Real Tazama (Kubernetes)
```

## 📝 Customization

### Change Target URL
Edit `simulation.py`:
```python
TARGET_URL = "http://localhost:8000/v1/evaluate/iso20022/pacs.008.001.10"
```

### Change Number of Transactions
Edit `simulation.py`:
```python
for i in range(1, 21):  # Change 21 to desired count + 1
```

### Change Currency/Amount Range
Edit `simulation.py`:
```python
amount = round(fake.random.uniform(100, 10000), 2)  # Min, Max
```

Edit `utils/iso_generator.py`:
```python
"Ccy": "IDR"  # Change currency code
```

## 🆚 Comparison: Mock vs Full Stack

| Aspect | Mock (`tazama_fastapi_sim`) | Full Stack |
|--------|----------------------------|------------|
| **Setup Time** | ~1 minute | ~5-10 minutes |
| **Memory Usage** | ~50MB | ~2-4GB |
| **Fraud Detection** | ❌ None (validation only) | ✅ Full (rules, typologies) |
| **Database** | ❌ None | ✅ Postgres, Valkey |
| **Message Queue** | ❌ None | ✅ NATS |
| **Use Case** | Development, format testing | Real evaluation, E2E testing |

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Change port in main.py or run.sh
uvicorn main:app --port 8001  # Change 8000 to 8001
```

### Module Not Found
```bash
# Ensure you're in the right directory
cd tazama_fastapi_sim
pip install -r requirements.txt
```

### Permission Denied (run.sh)
```bash
chmod +x run.sh
```

## 📚 Resources

- [ISO 20022 Documentation](https://www.iso20022.org/)
- [Tazama Full Stack Repository](https://github.com/tazama-lf/Full-Stack-Docker-Tazama)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## 🤝 Contributing

This is a development tool for the Tazama ecosystem. For production fraud detection, use:
- [Tazama Full Stack](https://github.com/tazama-lf/Full-Stack-Docker-Tazama)
- [Tazama Kubernetes Deployments](https://github.com/tazama-lf)

## 📄 License

Part of the Tazama Transaction Monitoring project.

---

**💡 Tip**: Start with this mock for quick testing, then move to Full Stack Docker for real fraud detection evaluation!
