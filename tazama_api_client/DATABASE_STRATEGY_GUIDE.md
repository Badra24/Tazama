# Database Query Strategy - Quick Guide

## 📋 Overview

Tazama API Client sekarang support **2 deployment** dengan **OOP Strategy Pattern**:

1. **Full Docker** - Query PostgreSQL di dalam Docker container
2. **Local PostgreSQL** - Query PostgreSQL lokal (port 5430)

---

## 🔧 Cara Switch

### **Edit `config.py` - SATU FLAG UNTUK SEMUA:**

```python
# config.py

# OPTION 1: Full Docker (Default)
USE_LOCAL_POSTGRES = False
# Auto-configures:
#   - TMS_BASE_URL = http://localhost:3000
#   - Database queries via Docker container

# OPTION 2: Local PostgreSQL
USE_LOCAL_POSTGRES = True
# Auto-configures:
#   - TMS_BASE_URL = http://localhost:3001
#   - Database queries via localhost:5430
```

**That's it!** Satu flag mengontrol:
- ✅ TMS endpoint URL (port 3000 vs 3001)
- ✅ Database query strategy (Docker vs Local)
- ✅ All routing automatically configured

Restart API client dan **EVERYTHING switches automatically**!

---

## 🏗️ Architecture (OOP)

```
DatabaseQueryService
    │
    ├── Strategy: FullDockerStrategy
    │   └── docker exec tazama-postgres-1 psql ...
    │
    └── Strategy: LocalPostgresStrategy
        └── psql -h localhost -p 5430 ...
```

### **Class Diagram:**

```
DatabaseQueryStrategy (Abstract)
├── execute_query()
└── get_name()

FullDockerStrategy extends DatabaseQueryStrategy
└── queries: docker exec tazama-postgres-1

LocalPostgresStrategy extends DatabaseQueryStrategy
└── queries: psql -h localhost -p 5430

DatabaseQueryService
├── strategy: DatabaseQueryStrategy
├── set_strategy()
└── get_transaction_summary()
```

---

## 💻 Usage Examples

### **Example 1: Default (Full Docker)**

```python
# config.py
USE_LOCAL_POSTGRES = False
```

```bash
# API endpoint automatically uses Full Docker
curl http://localhost:8000/api/test/db-summary
# Response includes: "strategy": "FullDocker(tazama-postgres-1:event_history)"
```

### **Example 2: Local PostgreSQL**

```python
# config.py
USE_LOCAL_POSTGRES = True
```

```bash
# API endpoint automatically uses Local PostgreSQL
curl http://localhost:8000/api/test/db-summary
# Response includes: "strategy": "LocalPostgres(localhost:5430/event_history)"
```

### **Example 3: Runtime Strategy Change (Advanced)**

```python
from services import DatabaseQueryService, FullDockerStrategy, LocalPostgresStrategy

# Create service with Full Docker
db_service = DatabaseQueryService(FullDockerStrategy())
result1 = db_service.get_transaction_summary()

# Switch to Local PostgreSQL at runtime
db_service.set_strategy(LocalPostgresStrategy())
result2 = db_service.get_transaction_summary()
```

---

## 🚀 Deployment Scenarios

### **Scenario 1: Testing with Full Docker**

```bash
# 1. Start Full Docker
cd Full-Stack-Docker-Tazama
docker-compose up -d

# 2. Configure API Client
# config.py: USE_LOCAL_POSTGRES = False

# 3. Run API Client
python -m uvicorn main:app --reload
```

### **Scenario 2: Production with Local PostgreSQL**

```bash
# 1. Ensure PostgreSQL running
psql -p 5430 -U badraaji -d event_history -c "SELECT 1"

# 2. Start Local Tazama
cd tazama-local-db
./start.sh

# 3. Configure API Client
# config.py: USE_LOCAL_POSTGRES = True

# 4. Run API Client
python -m uvicorn main:app --reload
```

### **Scenario 3: Switch Between Deployments**

```bash
# Currently using Full Docker, want to switch to Local

# 1. Stop Full Docker
cd Full-Stack-Docker-Tazama
docker-compose down

# 2. Start Local
cd ../tazama-local-db
./start.sh

# 3. Update config
# config.py: USE_LOCAL_POSTGRES = True

# 4. Restart API Client (auto-reload will pick up change)
```

---

## 🔍 Troubleshooting

### **Issue: "Connection refused" error**

**Check which deployment is running:**

```bash
# Check Full Docker
docker ps | grep tazama-postgres

# Check Local PostgreSQL
psql -p 5430 -l
```

**Solution:** Ensure `USE_LOCAL_POSTGRES` matches your running deployment.

### **Issue: "No data in transaction history"**

**Check database has data:**

```bash
# For Full Docker
docker exec -it tazama-postgres-1 psql -U postgres -d event_history -c "SELECT COUNT(*) FROM transaction;"

# For Local PostgreSQL
psql -p 5430 -U badraaji -d event_history -c "SELECT COUNT(*) FROM transaction;"
```

---

## 📊 Response Format

All responses include `strategy` field for debugging:

```json
{
  "status": "success",
  "total_transactions": 5,
  "debtors": [...],
  "creditors": [...],
  "strategy": "FullDocker(tazama-postgres-1:event_history)"
}
```

Or:

```json
{
  "status": "success",
  "total_transactions": 3,
  "debtors": [...],
  "creditors": [...],
  "strategy": "LocalPostgres(localhost:5430/event_history)"
}
```

---

## ✅ Benefits of OOP Approach

1. **Single Source of Truth** - Config di satu tempat (`config.py`)
2. **No Code Duplication** - Reuse query logic
3. **Easy Testing** - Mock strategies for unit tests
4. **Extensible** - Add new strategies (e.g., Remote PostgreSQL, Cloud DB)
5. **Runtime Flexibility** - Change strategy without restart
6. **Clear Separation** - Business logic terpisah dari infrastructure

---

## 🎯 Quick Reference

| Configuration | Deployment | TMS Port | PostgreSQL | DB Port |
|---------------|------------|----------|------------|---------|
| `USE_LOCAL_POSTGRES = False` | Full Docker | 3000 | Container | 5432 |
| `USE_LOCAL_POSTGRES = True` | Local DB | 3001 | Postgres.app | 5430 |

**Note:** SATU flag (`USE_LOCAL_POSTGRES`) mengontrol SEMUA konfigurasi!

---

## 📝 Files Modified

1. **`services/database_query_service.py`** - OOP service baru
2. **`services/__init__.py`** - Module exports
3. **`config.py`** - Added `USE_LOCAL_POSTGRES` flag
4. **`routers/transactions.py`** - Simplified `get_db_summary()` endpoint

---

**Happy coding!** 🚀
