# 🚀 API Client - Quick Reference Card

## ⚡ **ONE-PAGE REFERENCE**

---

## 🔧 **SETUP**

```python
from api_client import MaxParkAPI

# Local Network
api = MaxParkAPI("http://192.168.1.33:5001", api_key="your-api-key", verify_ssl=False)

# Cloudflare Tunnel (HTTPS)
api = MaxParkAPI("https://tunnel.trycloudflare.com", api_key="your-api-key", verify_ssl=True)
```

---

## 👥 **USER MANAGEMENT**

```python
# Add user (✅ API Key)
api.add_user("1234567890", "John Doe", "user123")

# Delete user (✅ API Key)
api.delete_user("1234567890")

# Block user (✅ API Key)
api.block_user("1234567890")

# Unblock user (✅ API Key)
api.unblock_user("1234567890")

# Get all users (❌ Public)
api.get_users()

# Search user (❌ Public)
api.search_user("1234567890")
```

---

## 🚪 **RELAY CONTROL**

```python
# Open gate (✅ API Key)
api.control_relay("open_hold", relay=1)

# Close gate (✅ API Key)
api.control_relay("close_hold", relay=1)

# Normal RFID mode (✅ API Key)
api.control_relay("normal_rfid", relay=1)
```

---

## 📊 **TRANSACTIONS**

```python
# Recent transactions (❌ Public)
api.get_transactions()

# Today's stats (❌ Public)
api.get_today_stats()

# Search by user (❌ Public)
api.search_user_transactions("John Doe", date_range="week")

# Sync to Firestore (✅ API Key)
api.sync_transactions()

# Cache status (❌ Public)
api.transaction_cache_status()

# Cleanup old (✅ API Key)
api.cleanup_old_transactions()
```

---

## 📸 **IMAGES**

```python
# List images (❌ Public)
api.get_images(limit=100)

# Offline images (❌ Public)
api.get_offline_images()

# Force upload (✅ API Key)
api.force_image_upload()

# Delete image (✅ API Key)
api.delete_image("filename.jpg")

# Clear all (✅ API Key)
api.clear_all_offline_images()
```

---

## ⚙️ **CONFIGURATION**

```python
# Get config (❌ Public)
api.get_config()

# Update config (✅ API Key)
api.update_config({"camera_1_enabled": "true"})

# Enable JSON mode (✅ API Key)
api.save_upload_config(json_enabled=True, json_url="https://api.com/upload")

# JSON status (❌ Public)
api.get_json_upload_status()
```

---

## 🌐 **NETWORK**

```python
# Network status (❌ Public)
api.get_network_status()

# Set static IP (✅ API Key)
api.apply_network_config("192.168.1.50", "192.168.1.1", "8.8.8.8")

# Reset to DHCP (✅ API Key)
api.reset_network_dhcp()
```

---

## 💾 **STORAGE**

```python
# Storage stats (❌ Public)
api.get_storage_stats()

# Storage info (❌ Public)
api.get_storage_info()

# Trigger cleanup (✅ API Key)
api.trigger_storage_cleanup()
```

---

## 🔧 **SYSTEM**

```python
# Health check (❌ Public)
api.health_check()

# Internet status (❌ Public)
api.internet_status(force=True)

# System reset (✅ API Key)
api.system_reset()
```

---

## 🔐 **AUTHENTICATION**

### **API Key Header:**
```
X-API-Key: your-api-key-from-env-file
```

### **Get API Key:**
```bash
# On Raspberry Pi
cat .env | grep API_KEY
```

### **In Code:**
```python
import os
api_key = os.getenv("MAXPARK_API_KEY")
api = MaxParkAPI(base_url="...", api_key=api_key)
```

---

## 🌐 **SSL/HTTPS**

### **Cloudflare Tunnel (Valid SSL):**
```python
api = MaxParkAPI(
    "https://tunnel.trycloudflare.com",
    api_key="...",
    verify_ssl=True  # ✅ Verify
)
```

### **Self-Signed (Testing):**
```python
api = MaxParkAPI(
    "https://self-signed.com",
    api_key="...",
    verify_ssl=False  # ⚠️ Skip verification
)
```

### **Local Network (HTTP):**
```python
api = MaxParkAPI(
    "http://192.168.1.33:5001",
    api_key="...",
    verify_ssl=False  # No SSL
)
```

---

## 🧪 **QUICK TEST**

```bash
python api_client.py
```

---

## 📝 **LEGEND**

- ✅ = Requires API Key (`X-API-Key` header)
- ❌ = Public (No authentication needed)

---

**Total Endpoints:** 47  
**Protected:** 28 (requires API key)  
**Public:** 19 (no authentication)

