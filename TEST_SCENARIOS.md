# 🧪 Tazama Test Scenarios Guide

## 📁 Folder Structure Postman Repository

```
/Users/badraaji/Desktop/RND/tazama/postman/
├── environments/
│   └── Tazama-Docker-Compose.postman_environment.json  ← Environment config (sudah di-fix!)
│
├── newman/                                              ← Newman CLI collections
│   ├── Newman - 2.1. (NO-AUTH) Public DockerHub End-to-End Test.postman_collection.json  ✅ RECOMMENDED
│   └── Newman - 3.1. (NO-AUTH) Public DockerHub Full-Service Test.postman_collection.json
│
└── Collections (root folder):
    ├── 0.1. Authentication Services - All.postman_collection.json
    ├── 0.2. Condition Management - All.postman_collection.json
    ├── 2.1. (NO-AUTH) Public DockerHub End-to-End Test.postman_collection.json  ✅ RECOMMENDED
    ├── 2.2. Rule Functionality Testing - Public DockerHub.postman_collection.json
    └── 3.1. (NO-AUTH) Public DockerHub Full-Service Test.postman_collection.json
```

---

## 🎯 Test Scenarios untuk Deployment Anda

Deployment Anda: **Public (DockerHub)** - Rule 901 & 902

### ✅ Scenario 1: **End-to-End Transaction Testing** (RECOMMENDED)

**File:** `2.1. (NO-AUTH) Public DockerHub End-to-End Test.postman_collection.json`

**Kegiatan yang Ditest:**
1. **TMS API Availability** - Memastikan service UP
2. **Transaction Submission** - Kirim pacs.008 (transfer request) dan pacs.002 (confirmation)
3. **Database Updates** - Verify data tersimpan di Postgres
4. **Event Director Routing** - Transaksi di-route ke rules
5. **Rule Processing** - Rule 901 & 902 evaluate transaksi
6. **Typology Processing** - Hasil rules diagregasi
7. **TADP (Decisioning)** - Final decision & alert generation
8. **Evaluation Results** - Hasil tersimpan di evaluation database

**Skenario Fraud:**
- ✅ Normal transaction (tidak fraud)
- ✅ Multiple transactions dari debtor yang sama (velocity pattern)
- ✅ Transaction history check
- ✅ Entity & account relationship

**Output Expected:**
```
┌─────────────────────────┬──────────────────┬──────────────────┐
│                         │         executed │           failed │
├─────────────────────────┼──────────────────┼──────────────────┤
│              iterations │                1 │                0 │
│                requests │                4 │                0 │
│              assertions │               39 │                0 │
└─────────────────────────┴──────────────────┴──────────────────┘
```

---

### ✅ Scenario 2: **Rule Functionality Testing**

**File:** `2.2. Rule Functionality Testing - Public DockerHub.postman_collection.json`

**Kegiatan yang Ditest:**
- Test **Rule 901** secara exhaustive (langsung ke rule processor)
- Test **Rule 902** secara exhaustive
- Verify setiap possible outcome dari rule

**Use Case Rule 901:**
```
Rule 901: "Number of outgoing transactions - debtor"

Test Cases:
├── 1 transaction  → Result: indpdntVarbl = 1
├── 2 transactions → Result: indpdntVarbl = 2
├── 3+ transactions → Result: indpdntVarbl = 3+
└── Unsuccessful transaction → Result: indpdntVarbl = 0 (skip)
```

**Butuh Addon:** ⚠️ NATS Utilities (saat ini TIDAK aktif di deployment Anda)

---

### ✅ Scenario 3: **Full-Service Testing**

**File:** `3.1. (NO-AUTH) Public DockerHub Full-Service Test.postman_collection.json`

**Kegiatan yang Ditest:**
- Test semua rules yang tersedia (jika deploy full-service)
- Typology composition dengan banyak rules
- Multi-rule evaluation

**Catatan:** ⚠️ Collection ini untuk deployment "Full-Service" (Option 3 di tazama.sh).  
Deployment Anda saat ini: "Public DockerHub" (Option 2) - hanya Rule 901 & 902.

---

### 🔐 Scenario 4: **Authentication Testing** (OPTIONAL)

**File:** `0.1. Authentication Services - All.postman_collection.json`

**Kegiatan yang Ditest:**
- KeyCloak authentication flow
- JWT token generation
- Authenticated API requests
- Multi-tenant isolation

**Butuh Addon:** ⚠️ Authentication Services (saat ini TIDAK aktif)

---

### 🚦 Scenario 5: **Condition Management** (OPTIONAL)

**File:** `0.2. Condition Management - All.postman_collection.json`

**Kegiatan yang Ditest:**
- Create account conditions (block/allow)
- Create entity conditions
- Transaction blocking berdasarkan conditions
- Active/expired condition handling

**Use Case:**
```
Scenario: Block suspicious account
1. Create condition for account X
2. Submit transaction from account X
3. Verify transaction blocked/flagged
4. Remove condition
5. Verify transaction allowed
```

---

## 🎬 Services & Controllers yang Bisa Ditest

### 1. **TMS (Transaction Monitoring Service)** - Port 5001
```
Endpoints:
POST /v1/evaluate/iso20022/pacs.008.001.10  ← Transfer request
POST /v1/evaluate/iso20022/pacs.002.001.12  ← Confirmation
GET  /                                       ← Health check
```

**Test:** End-to-End collections

---

### 2. **Admin Service** - Port 5100
```
Endpoints:
POST /v1/admin/event-flow-control/account    ← Account conditions
POST /v1/admin/event-flow-control/entity     ← Entity conditions
GET  /v1/report/evaluations/{msgId}         ← Get eval results
```

**Test:** Condition Management collection

---

### 3. **Rule Processors** (Internal via NATS)
```
Rules Deployed:
- Rule 901: Number of outgoing transactions (debtor)
- Rule 902: Number of outgoing transactions (creditor)
```

**Test:** Rule Functionality collection (butuh NATS Utils)

---

### 4. **Event Director** (Internal)
```
Fungsi:
- Route transaksi ke rule processors
- Berdasarkan network_map configuration
```

**Test:** Ditest via End-to-End (tidak langsung)

---

### 5. **Typology Processor** (Internal)
```
Fungsi:
- Aggregate rule results
- Apply typology configuration
- Score typology match
```

**Test:** Ditest via End-to-End (tidak langsung)

---

### 6. **TADP - Transaction Aggregation & Decisioning** (Internal)
```
Fungsi:
- Aggregate typology results
- Generate final decision
- Create alerts jika fraud terdeteksi
```

**Test:** Ditest via End-to-End (tidak langsung)

---

## 🚀 Quick Start - Cara Menggunakan

### Option A: Postman App (GUI)

```bash
# 1. Import environment
# File → Import → Tazama-Docker-Compose.postman_environment.json

# 2. Import collection
# File → Import → 2.1. (NO-AUTH) Public DockerHub End-to-End Test.postman_collection.json

# 3. Select environment (kanan atas dropdown)

# 4. Run collection
# Klik "Run" button → Start Test Runn
```

### Option B: Newman CLI (Recommended)

```bash
cd /Users/badraaji/Desktop/RND/tazama/postman

# Test End-to-End
newman run \
  "newman/Newman - 2.1. (NO-AUTH) Public DockerHub End-to-End Test.postman_collection.json" \
  -e "environments/Tazama-Docker-Compose.postman_environment.json" \
  --timeout-request 10200 \
  --delay-request 500
```

---

## 📊 Deployment Addon Matrix

| Test Collection | Relay Services | NATS Utils | Auth | pgAdmin | Hasura |
|----------------|:--------------:|:----------:|:----:|:-------:|:------:|
| **2.1 E2E Test** | ✅ | ❌ | ❌ | ✅ | ✅ |
| **2.2 Rule Test** | ❌ | ✅ | ❌ | ✅ | ✅ |
| **0.1 Auth Test** | ❌ | ❌ | ✅ | ✅ | ✅ |
| **0.2 Condition Test** | ✅ | ✅ | ❌ | ✅ | ✅ |

**Deployment Anda saat ini:**
```
CORE ADDONS:
1. [ ] Authentication
2. [ ] Relay Services
3. [ ] Basic Logs
4. [ ] Demo UI

UTILITY ADDONS:
5. [ ] NATS Utilities
6. [ ] Batch PPA
7. [X] pgAdmin for PostgreSQL
8. [X] Hasura GraphQL API for PostgreSQL
```

**Bisa Run:**
- ✅ **2.1** - E2E Test (PRIMARY)
- ❌ 2.2 - Rule Test (butuh NATS Utils)
- ❌ 0.1 - Auth Test (butuh Auth)
- ❌ 0.2 - Condition Test (butuh NATS Utils & Relay)

---

## 💡 Recommendasi untuk Anda

### Langkah 1: Test dengan Collection 2.1 (E2E)
```bash
cd /Users/badraaji/Desktop/RND/tazama/postman
newman run "newman/Newman - 2.1. (NO-AUTH) Public DockerHub End-to-End Test.postman_collection.json" \
  -e "environments/Tazama-Docker-Compose.postman_environment.json"
```

**Ini akan test:**
- ✅ Transaction submission flow
- ✅ Database updates
- ✅ Rule 901 & 902 execution
- ✅ Complete evaluation pipeline

### Langkah 2: Jika Mau Test Individual Rules

**Redeploy dengan NATS Utils:**
```bash
cd /Users/badraaji/Desktop/RND/tazama/Full-Stack-Docker-Tazama
docker compose -p tazama down

./tazama.sh
# Select: 2 (Public DockerHub)
# Toggle: 2 (Relay Services) → ON
# Toggle: 5 (NATS Utilities) → ON
# Apply: a
```

**Kemudian run:**
```bash
newman run "2.2. Rule Functionality Testing - Public DockerHub.postman_collection.json" \
  -e "environments/Tazama-Docker-Compose.postman_environment.json"
```

---

## 🎓 Summary

**Scenario Utama untuk Kegiatan Testing Tazama:**

| # | Scenario | Kegiatan | Collection | Status |
|---|----------|----------|------------|--------|
| 1 | **Fraud Detection E2E** | Test complete transaction evaluation flow | 2.1 E2E | ✅ Ready |
| 2 | **Rule Unit Testing** | Test individual rule behavior | 2.2 Rules | ⚠️ Butuh addon |
| 3 | **Transaction Blocking** | Test account/entity conditions | 0.2 Conditions | ⚠️ Butuh addon |
| 4 | **Authentication Flow** | Test auth & multi-tenant | 0.1 Auth | ⚠️ Butuh addon |
| 5 | **Full Stack Testing** | Test all available rules | 3.1 Full | ℹ️ Different deployment |

**MULAI DARI:** Collection **2.1** - ini yang paling sesuai dengan deployment Anda saat ini! 🚀
