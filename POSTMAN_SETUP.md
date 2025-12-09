# Postman Configuration untuk Tazama

## ✅ Yang Sudah Diperbaiki:

### 1. Environment File
**File**: `Tazama-Docker-Compose.postman_environment.json`

**Perubahan:**
- ✅ `tazamaTMSUrl`: `localhost:5000` → `localhost:5001`

Ini sesuai dengan deployment Anda yang TMS running di port **5001** (karena port 5000 dipakai macOS AirPlay).

### 2. Collection yang Tersedia

Saya sudah clone official Postman repository dan menemukan collection yang **SESUAI** dengan deployment Anda:

| Collection | Cocok? | Keterangan |
|-----------|--------|------------|
| **Newman - 2.1. (NO-AUTH) Public DockerHub End-to-End Test** | ✅ **GUNAKAN INI** | Untuk deployment DockerHub tanpa auth |
| Newman - 3.1. (NO-AUTH) Public DockerHub Full-Service Test | ✅ Alternatif | Jika deploy full-service dengan semua rules |
| Newman - 1.1. (NO-AUTH) Public GitHub End-to-End Test | ❌ Salah | Untuk GitHub deployment (build dari source) |
| 1.2. Rule Functionality Testing - Public GitHub | ❌ Salah | Butuh NATS Utils yang tidak aktif |

## 📂 File Locations

```
/Users/badraaji/Desktop/RND/tazama/
├── Tazama-Docker-Compose.postman_environment.json  ← Fixed (port 5001)
├── Newman - 2.1. (NO-AUTH) Public DockerHub End-to-End Test.postman_collection.json  ← RECOMMENDED
└── postman/                                        ← Full repository
    ├── newman/                                     ← Newman test collections
    │   ├── Newman - 2.1. (NO-AUTH) Public DockerHub End-to-End Test.postman_collection.json
    │   └── Newman - 3.1. (NO-AUTH) Public DockerHub Full-Service Test.postman_collection.json
    └── environments/
        └── Tazama-Docker-Compose.postman_environment.json
```

## 🚀 Cara Menggunakan di Postman

### Option 1: Via Postman App (GUI)

1. **Import Environment:**
   - Buka Postman
   - File → Import
   - Pilih: `Tazama-Docker-Compose.postman_environment.json`
   - Select environment di dropdown (kanan atas)

2. **Import Collection:**
   - File → Import
   - Pilih: `Newman - 2.1. (NO-AUTH) Public DockerHub End-to-End Test.postman_collection.json`

3. **Run Tests:**
   - Klik collection
   - Klik "Run" button
   - Pastikan environment "Tazama-Docker-Compose" selected
   - Click "Run Tazama..."

### Option 2: Via Newman CLI

```bash
cd /Users/badraaji/Desktop/RND/tazama/postman

newman run \
  "newman/Newman - 2.1. (NO-AUTH) Public DockerHub End-to-End Test.postman_collection.json" \
  -e "environments/Tazama-Docker-Compose.postman_environment.json" \
  --timeout-request 10200 \
  --delay-request 500
```

## ⚠️ Prerequisites

Pastikan Tazama stack **sedang running**:

```bash
# Check containers
docker ps --filter "name=tazama"

# Should see:
# - tazama-tms-1 (UP)
# - tazama-postgres-1 (UP and healthy)
# - tazama-valkey-1 (UP and healthy)
# - tazama-nats-1 (UP)
# + other services
```

Kalau belum running:
```bash
cd /Users/badraaji/Desktop/RND/tazama/Full-Stack-Docker-Tazama
./tazama.sh
# Pilih: Option 2 (Public DockerHub)
# Apply: a
```

## 📊 Expected Test Results

Collection "2.1" akan mengirim transaction ke TMS dan verify:
1. ✅ TMS menerima dan memproses transaction
2. ✅ Event Director routing transaction
3. ✅ Rule processors evaluate
4. ✅ Typology processor aggregate hasil
5. ✅ TADP publish evaluation results
6. ✅ Data tersimpan di database

**Expected Output:**
```
┌─────────────────────────┬──────────────────┬──────────────────┐
│                         │         executed │           failed │
├─────────────────────────┼──────────────────┼──────────────────┤
│              iterations │                1 │                0 │
├─────────────────────────┼──────────────────┼──────────────────┤
│                requests │                4 │                0 │
├─────────────────────────┼──────────────────┼──────────────────┤
│              assertions │               39 │                0 │
└─────────────────────────┴──────────────────┴──────────────────┘
```

## 🔧 Troubleshooting

### Test Gagal: "ECONNREFUSED localhost:5001"
→ TMS belum running. Start dengan `./tazama.sh`

### Test Gagal: "Timeout"
→ Service masih initializing. Tunggu 1-2 menit setelah deploy.

### Test Gagal: Database errors
→ Postgres/Hasura belum ready. Check `docker logs tazama-postgres-1`

---

**🎉 Setup Complete!** Environment dan collection sudah siap untuk testing.
