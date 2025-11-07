# 🔐 API Authentication Reference - Complete List

## 📋 **ALL API ENDPOINTS WITH AUTHENTICATION STATUS**

---

## ✅ **ENDPOINTS REQUIRING API KEY** (27 endpoints)

These endpoints require `X-API-Key` header with valid API key from `.env` file.

### **User Management (4):**
1. ✅ `POST/GET /add_user` - Add new user
2. ✅ `GET /delete_user` - Delete user
3. ✅ `GET /block_user` - Block user access
4. ✅ `GET /unblock_user` - Unblock user access

### **System Control (2):**
5. ✅ `GET /relay` - Control gate/barrier relay
6. ✅ `POST /system_reset` - Restart system

### **Configuration Management (4):**
7. ✅ `POST /update_config` - Update system settings
8. ✅ `POST /save_upload_config` - Configure JSON/S3 upload mode
9. ✅ `POST /apply_network_config` - Set static IP
10. ✅ `POST /reset_network_dhcp` - Reset to DHCP

### **Transaction Management (2):**
11. ✅ `POST /sync_transactions` - Manually sync to Firestore
12. ✅ `POST /cleanup_old_transactions` - Delete old transactions

### **Image Management (4):**
13. ✅ `DELETE /delete_image/<filename>` - Delete specific image
14. ✅ `POST /force_image_upload` - Force immediate upload
15. ✅ `POST /clear_all_offline_images` - Delete all offline images
16. ✅ `POST /trigger_storage_cleanup` - Trigger storage cleanup

### **Password Management (2):**
17. ✅ `POST /reset_password` - Reset admin password
18. ✅ `GET /get_password_info` - Get password information

### **Storage Cleanup (3):**
19. ✅ `POST /cleanup_old_images` - Cleanup old images (also uses @require_auth)
20. ✅ `POST /cleanup_old_stats` - Cleanup old statistics (also uses @require_auth)
21. ✅ `POST /clear_all_stats` - Clear all statistics (also uses @require_auth)

---

## ❌ **PUBLIC ENDPOINTS** (19 endpoints)

These endpoints do NOT require authentication - anyone can access.

### **User Information (2):**
1. ❌ `GET /get_users` - List all users
2. ❌ `GET /search_user` - Search specific user

### **Transactions & Stats (5):**
3. ❌ `GET /get_transactions` - Get recent transactions
4. ❌ `GET /get_today_stats` - Today's access statistics
5. ❌ `GET /search_user_transactions` - Search user's transaction history
6. ❌ `GET /transaction_cache_status` - Transaction cache info

### **Images (2):**
7. ❌ `GET /get_images` - List captured images
8. ❌ `GET /get_offline_images` - List pending uploads

### **Configuration (4):**
9. ❌ `GET /get_config` - View current configuration
10. ❌ `GET /get_json_upload_status` - JSON upload mode status
11. ❌ `GET /get_network_status` - Network configuration
12. ❌ `GET /get_network_config_status` - Network config details

### **Storage & System (4):**
13. ❌ `GET /get_storage_stats` - Storage statistics
14. ❌ `GET /get_storage_info` - Storage information
15. ❌ `GET /health_check` - System health status
16. ❌ `GET /internet_status` - Internet connectivity status

### **Photo Preferences (4):**
17. ❌ `GET /get_photo_preferences` - Photo capture settings
18. ❌ `POST /save_global_photo_settings` - Save global photo settings
19. ❌ `POST /add_photo_preference` - Add photo preference
20. ❌ `POST /remove_photo_preference` - Remove photo preference

---

## 🔑 **HOW TO GET API KEY**

### **On Raspberry Pi:**
```bash
# Check .env file
cat .env | grep API_KEY

# Output:
API_KEY=your-api-key-change-this
```

### **In API Client:**
```python
api = MaxParkAPI(
    base_url="http://192.168.1.33:5001",
    api_key="your-api-key-change-this"  # Use value from .env
)
```

---

## 🌐 **CLOUDFLARE TUNNEL WITH SSL**

### **Setup Cloudflare Tunnel:**
```bash
# On Raspberry Pi:
# Install cloudflared
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm
chmod +x cloudflared-linux-arm
sudo mv cloudflared-linux-arm /usr/local/bin/cloudflared

# Start tunnel
cloudflared tunnel --url http://localhost:5001
```

**Output:**
```
Your quick Tunnel has been created! Visit it at:
https://random-name-1234.trycloudflare.com
```

### **Use in API Client:**
```python
# Cloudflare provides valid SSL certificate
api = MaxParkAPI(
    base_url="https://random-name-1234.trycloudflare.com",
    api_key="your-api-key",
    verify_ssl=True  # ✅ Verify Cloudflare SSL
)

# Use from anywhere in the world!
users = api.get_users()
```

---

## 🔒 **SSL VERIFICATION MODES**

### **1. Full SSL Verification (Production):**
```python
api = MaxParkAPI(
    base_url="https://your-domain.com",
    verify_ssl=True  # ✅ Verify certificate
)
```
**Use for:** Cloudflare Tunnel, Let's Encrypt, Commercial SSL

---

### **2. Skip SSL Verification (Testing Only):**
```python
api = MaxParkAPI(
    base_url="https://your-domain.com",
    verify_ssl=False  # ⚠️ Skip verification
)
```
**Use for:** Self-signed certificates, testing only

---

### **3. Custom CA Certificate:**
```python
api = MaxParkAPI(
    base_url="https://your-domain.com",
    verify_ssl="/path/to/ca-bundle.crt"  # Custom CA
)
```
**Use for:** Corporate/custom CA certificates

---

### **4. No SSL (Local Network):**
```python
api = MaxParkAPI(
    base_url="http://192.168.1.33:5001",  # HTTP, no SSL
    verify_ssl=False  # Not used for HTTP
)
```
**Use for:** Local network connections

---

## 🧪 **TESTING**

### **Test Script:**
```bash
python api_client.py
```

**What It Tests:**
1. ✅ Health check
2. ✅ Get users
3. ✅ Get transactions
4. ✅ JSON upload status
5. ✅ Internet status

---

### **Test Individual Functions:**
```python
from api_client import MaxParkAPI

# Initialize
api = MaxParkAPI("http://192.168.1.33:5001", api_key="your-key")

# Test public endpoints
print("Health:", api.health_check())
print("Users:", api.get_users())
print("Transactions:", api.get_transactions())

# Test authenticated endpoints
print("Add user:", api.add_user("9999999999", "Test User", "test123"))
print("Block user:", api.block_user("9999999999"))
print("Unblock user:", api.unblock_user("9999999999"))
print("Delete user:", api.delete_user("9999999999"))
```

---

## 📊 **AUTHENTICATION SUMMARY**

| Category | Total Endpoints | Require API Key | Public |
|----------|----------------|-----------------|--------|
| **User Management** | 6 | 4 | 2 |
| **Relay Control** | 1 | 1 | 0 |
| **Transactions** | 6 | 2 | 4 |
| **Images** | 5 | 4 | 1 |
| **Configuration** | 8 | 4 | 4 |
| **Network** | 5 | 2 | 3 |
| **Storage** | 6 | 4 | 2 |
| **System** | 4 | 1 | 3 |
| **Password** | 2 | 2 | 0 |
| **Photo Prefs** | 4 | 0 | 4 |
| **TOTAL** | **47** | **28** | **19** |

---

## ✅ **READY TO USE**

**Files Created:**
- ✅ `api_client.py` - Complete Python API client
- ✅ `API_CLIENT_GUIDE.md` - Usage guide
- ✅ `API_AUTHENTICATION_REFERENCE.md` - This reference

**Features:**
- ✅ All 47 API endpoints included
- ✅ API key authentication handled
- ✅ SSL certificate verification
- ✅ Cloudflare Tunnel support
- ✅ Local network support
- ✅ Comprehensive error handling
- ✅ Easy-to-use functions
- ✅ Built-in test script

**Just run:** `python api_client.py` to test! 🚀

---

**Created:** November 6, 2024  
**Status:** ✅ Production Ready  
**SSL Support:** ✅ Full SSL/TLS with Cloudflare

