# 🔌 MaxPark RFID API Client - Complete Guide

## 📋 **What is This?**

A comprehensive Python API client for the MaxPark RFID Access Control System that includes:
- ✅ All available API endpoints
- ✅ Authentication handling (API key)
- ✅ SSL/TLS support for Cloudflare Tunnel
- ✅ Local network support
- ✅ Error handling
- ✅ Easy-to-use functions

---

## 🚀 **Quick Start**

### **For Local Network:**
```python
from api_client import MaxParkAPI

# Initialize
api = MaxParkAPI(
    base_url="http://192.168.1.33:5001",
    api_key="your-api-key",
    verify_ssl=False  # Local network, no SSL
)

# Add user
result = api.add_user("1234567890", "John Doe", "user123")
print(result)
```

### **For Cloudflare Tunnel:**
```python
from api_client import MaxParkAPI

# Initialize
api = MaxParkAPI(
    base_url="https://your-tunnel.trycloudflare.com",
    api_key="your-api-key",
    verify_ssl=True  # Cloudflare has valid SSL
)

# Block user
result = api.block_user("1234567890")
print(result)
```

---

## 🔐 **AUTHENTICATION REFERENCE**

### **Endpoints Requiring API Key (X-API-Key header):**

**User Management:**
- ✅ `add_user()` - Add new user
- ✅ `delete_user()` - Delete user
- ✅ `block_user()` - Block user
- ✅ `unblock_user()` - Unblock user

**System Control:**
- ✅ `control_relay()` - Control gate/barrier
- ✅ `system_reset()` - Restart system
- ✅ `trigger_storage_cleanup()` - Manual cleanup

**Configuration:**
- ✅ `update_config()` - Update system settings
- ✅ `save_upload_config()` - Configure JSON/S3 mode
- ✅ `apply_network_config()` - Change network settings
- ✅ `reset_network_dhcp()` - Reset to DHCP

**Transaction/Image Management:**
- ✅ `sync_transactions()` - Manual sync to Firestore
- ✅ `cleanup_old_transactions()` - Cleanup old data
- ✅ `force_image_upload()` - Force upload
- ✅ `delete_image()` - Delete specific image
- ✅ `clear_all_offline_images()` - Clear all images

**Password:**
- ✅ `reset_password()` - Reset admin password
- ✅ `get_password_info()` - Get password info

---

### **Public Endpoints (No Authentication):**

**User Info:**
- ❌ `get_users()` - List all users
- ❌ `search_user()` - Search specific user

**Transactions:**
- ❌ `get_transactions()` - Recent transactions
- ❌ `get_today_stats()` - Today's statistics
- ❌ `search_user_transactions()` - Search by user
- ❌ `transaction_cache_status()` - Cache status

**Images:**
- ❌ `get_images()` - List images
- ❌ `get_offline_images()` - Pending uploads

**Configuration:**
- ❌ `get_config()` - View configuration
- ❌ `get_json_upload_status()` - JSON upload status
- ❌ `get_photo_preferences()` - Photo settings

**System:**
- ❌ `health_check()` - System health
- ❌ `internet_status()` - Internet status
- ❌ `get_network_status()` - Network info
- ❌ `get_storage_stats()` - Storage info
- ❌ `get_storage_info()` - Storage details

---

## 📖 **USAGE EXAMPLES**

### **Example 1: User Management**

```python
from api_client import MaxParkAPI

# Initialize
api = MaxParkAPI("http://192.168.1.33:5001", api_key="your-api-key")

# Add user
result = api.add_user(
    card_number="1234567890",
    name="John Doe",
    user_id="john123"
)
print(f"Add user: {result}")

# Search user
user = api.search_user("1234567890")
print(f"User found: {user}")

# Block user
result = api.block_user("1234567890")
print(f"Block user: {result}")

# Unblock user
result = api.unblock_user("1234567890")
print(f"Unblock user: {result}")

# Delete user
result = api.delete_user("1234567890")
print(f"Delete user: {result}")

# Get all users
users = api.get_users()
print(f"Total users: {len(users.get('users', []))}")
```

---

### **Example 2: Transaction Monitoring**

```python
# Get recent transactions
transactions = api.get_transactions()
print(f"Recent scans: {len(transactions)}")

for tx in transactions:
    print(f"  - {tx['name']} ({tx['card_number']}) - {tx['status']}")

# Get today's stats
stats = api.get_today_stats()
print(f"Today's stats: {stats}")

# Search user transactions
user_txs = api.search_user_transactions("John Doe", date_range="week")
print(f"John's transactions this week: {user_txs}")
```

---

### **Example 3: System Configuration**

```python
# Get current configuration
config = api.get_config()
print(f"Current config: {config}")

# Update configuration
new_config = {
    "camera_1_enabled": "true",
    "camera_2_enabled": "false",
    "scan_delay_seconds": "30"
}
result = api.update_config(new_config)
print(f"Config updated: {result}")

# Enable JSON upload mode
result = api.save_upload_config(
    json_enabled=True,
    json_url="https://your-api.com/upload"
)
print(f"JSON mode enabled: {result}")

# Check JSON upload status
status = api.get_json_upload_status()
print(f"JSON status: {status}")
```

---

### **Example 4: Relay Control**

```python
# Open relay (gate)
result = api.control_relay(action="open_hold", relay=1)
print(f"Relay opened: {result}")

# Close relay
result = api.control_relay(action="close_hold", relay=1)
print(f"Relay closed: {result}")

# Normal mode (auto RFID control)
result = api.control_relay(action="normal_rfid", relay=1)
print(f"Normal mode: {result}")
```

---

### **Example 5: Image Management**

```python
# Get images
images = api.get_images(limit=50)
print(f"Total images: {len(images.get('images', []))}")

# Get offline images (not uploaded)
offline = api.get_offline_images()
print(f"Pending uploads: {offline.get('count', 0)}")

# Force upload
result = api.force_image_upload()
print(f"Upload triggered: {result}")

# Delete specific image
result = api.delete_image("1234567890_r1_1699123456.jpg")
print(f"Image deleted: {result}")
```

---

### **Example 6: Cloudflare Tunnel (HTTPS)**

```python
from api_client import MaxParkAPI

# For Cloudflare with valid SSL certificate
api = MaxParkAPI(
    base_url="https://your-tunnel.trycloudflare.com",
    api_key="your-api-key",
    verify_ssl=True  # Verify Cloudflare SSL certificate
)

# For self-signed certificates (testing)
api = MaxParkAPI(
    base_url="https://your-tunnel.trycloudflare.com",
    api_key="your-api-key",
    verify_ssl=False  # Skip SSL verification (testing only!)
)

# Use normally
result = api.get_users()
print(result)
```

---

## 🧪 **TESTING SCRIPT**

The `api_client.py` file includes a built-in test script:

```bash
# Run tests
python api_client.py
```

**What It Tests:**
1. Health check
2. Get users
3. Get transactions
4. JSON upload status
5. Internet status

**Expected Output:**
```
======================================================================
MaxPark RFID System - API Client
======================================================================

🔗 Connected to: http://192.168.1.33:5001
🔑 API Key: your-api-k...

======================================================================

1️⃣ Testing Health Check (Public)
----------------------------------------------------------------------
{
  "status": "success",
  "cameras": {...},
  "internet": true,
  "firebase": true
}

2️⃣ Testing Get Users (Public)
----------------------------------------------------------------------
Total users: 45

3️⃣ Testing Get Transactions (Public)
----------------------------------------------------------------------
Recent transactions: 10
Latest: John Doe - Access Granted

... etc
```

---

## 🔧 **CONFIGURATION**

### **Edit Configuration in Script:**
```python
# Line 460-461
BASE_URL = "http://192.168.1.33:5001"  # Your Pi IP or Cloudflare URL
API_KEY = "your-api-key-change-this"   # From .env file
```

### **For Cloudflare Tunnel:**
```python
BASE_URL = "https://your-tunnel.trycloudflare.com"
VERIFY_SSL = True  # Cloudflare has valid SSL cert
```

### **For Local Network:**
```python
BASE_URL = "http://192.168.1.33:5001"
VERIFY_SSL = False  # No SSL on local network
```

---

## 🔐 **SSL CERTIFICATE HANDLING**

### **Valid SSL Certificate (Cloudflare, Let's Encrypt):**
```python
api = MaxParkAPI(
    base_url="https://your-domain.com",
    verify_ssl=True  # ✅ Verify certificate
)
```

### **Self-Signed Certificate:**
```python
api = MaxParkAPI(
    base_url="https://your-domain.com",
    verify_ssl=False  # ⚠️ Skip verification (testing only!)
)
```

### **Custom CA Certificate:**
```python
api = MaxParkAPI(
    base_url="https://your-domain.com",
    verify_ssl="/path/to/ca-bundle.crt"  # Path to CA cert
)
```

---

## 📊 **COMPLETE API REFERENCE**

### **User Management (API Key Required):**
| Method | Endpoint | Authentication |
|--------|----------|----------------|
| `add_user(card, name, id)` | `/add_user` | ✅ API Key |
| `delete_user(card)` | `/delete_user` | ✅ API Key |
| `block_user(card)` | `/block_user` | ✅ API Key |
| `unblock_user(card)` | `/unblock_user` | ✅ API Key |
| `get_users()` | `/get_users` | ❌ Public |
| `search_user(card)` | `/search_user` | ❌ Public |

### **Relay Control (API Key Required):**
| Method | Endpoint | Authentication |
|--------|----------|----------------|
| `control_relay(action, relay)` | `/relay` | ✅ API Key |

### **Transactions (Public):**
| Method | Endpoint | Authentication |
|--------|----------|----------------|
| `get_transactions()` | `/get_transactions` | ❌ Public |
| `get_today_stats()` | `/get_today_stats` | ❌ Public |
| `search_user_transactions(name, range)` | `/search_user_transactions` | ❌ Public |
| `sync_transactions()` | `/sync_transactions` | ✅ API Key |
| `transaction_cache_status()` | `/transaction_cache_status` | ❌ Public |
| `cleanup_old_transactions()` | `/cleanup_old_transactions` | ✅ API Key |

### **Image Management:**
| Method | Endpoint | Authentication |
|--------|----------|----------------|
| `get_images(limit)` | `/get_images` | ❌ Public |
| `delete_image(filename)` | `/delete_image/<filename>` | ✅ API Key |
| `get_offline_images()` | `/get_offline_images` | ❌ Public |
| `force_image_upload()` | `/force_image_upload` | ✅ API Key |
| `clear_all_offline_images()` | `/clear_all_offline_images` | ✅ API Key |

### **Configuration:**
| Method | Endpoint | Authentication |
|--------|----------|----------------|
| `get_config()` | `/get_config` | ❌ Public |
| `update_config(config)` | `/update_config` | ✅ API Key |
| `save_upload_config(enabled, url)` | `/save_upload_config` | ✅ API Key |
| `get_json_upload_status()` | `/get_json_upload_status` | ❌ Public |

### **Network Configuration (API Key Required):**
| Method | Endpoint | Authentication |
|--------|----------|----------------|
| `get_network_status()` | `/get_network_status` | ❌ Public |
| `apply_network_config(ip, gateway, dns)` | `/apply_network_config` | ✅ API Key |
| `reset_network_dhcp()` | `/reset_network_dhcp` | ✅ API Key |

### **Storage & System:**
| Method | Endpoint | Authentication |
|--------|----------|----------------|
| `get_storage_stats()` | `/get_storage_stats` | ❌ Public |
| `get_storage_info()` | `/get_storage_info` | ❌ Public |
| `trigger_storage_cleanup()` | `/trigger_storage_cleanup` | ✅ API Key |
| `system_reset()` | `/system_reset` | ✅ API Key |
| `health_check()` | `/health_check` | ❌ Public |
| `internet_status(force)` | `/internet_status` | ❌ Public |

### **Password Management (API Key Required):**
| Method | Endpoint | Authentication |
|--------|----------|----------------|
| `reset_password(new_pw)` | `/reset_password` | ✅ API Key |
| `get_password_info()` | `/get_password_info` | ✅ API Key |

### **Photo Preferences (Public):**
| Method | Endpoint | Authentication |
|--------|----------|----------------|
| `get_photo_preferences()` | `/get_photo_preferences` | ❌ Public |
| `save_global_photo_settings(enabled)` | `/save_global_photo_settings` | ❌ Public |
| `add_photo_preference(id, skip, type)` | `/add_photo_preference` | ❌ Public |
| `remove_photo_preference(id, type)` | `/remove_photo_preference` | ❌ Public |

---

## 🎯 **COMMON USE CASES**

### **Use Case 1: Bulk User Import**
```python
from api_client import MaxParkAPI
import csv

api = MaxParkAPI("http://192.168.1.33:5001", api_key="your-api-key")

# Read users from CSV
with open('users.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        result = api.add_user(
            card_number=row['card_number'],
            name=row['name'],
            user_id=row['user_id']
        )
        print(f"Added {row['name']}: {result.get('status')}")
```

---

### **Use Case 2: Block Multiple Users**
```python
# Block list of card numbers
blocked_cards = ["1111111111", "2222222222", "3333333333"]

for card in blocked_cards:
    result = api.block_user(card)
    print(f"Blocked {card}: {result.get('status')}")
```

---

### **Use Case 3: Monitor System Health**
```python
import time

while True:
    health = api.health_check()
    internet = api.internet_status()
    json_status = api.get_json_upload_status()
    
    print(f"System Health: {health.get('status')}")
    print(f"Internet: {'✅' if internet.get('internet_available') else '❌'}")
    print(f"Pending JSON uploads: {json_status.get('pending_count', 0)}")
    
    time.sleep(60)  # Check every minute
```

---

### **Use Case 4: Export Daily Transactions**
```python
import json
from datetime import datetime

# Get today's transactions
transactions = api.get_transactions()
stats = api.get_today_stats()

# Save to file
export_data = {
    "date": datetime.now().isoformat(),
    "statistics": stats,
    "transactions": transactions
}

with open(f'export_{datetime.now().strftime("%Y%m%d")}.json', 'w') as f:
    json.dump(export_data, f, indent=2)

print("Export complete!")
```

---

### **Use Case 5: Remote Gate Control**
```python
# Open gate for 5 seconds
api.control_relay(action="open_hold", relay=1)
time.sleep(5)

# Return to normal RFID mode
api.control_relay(action="normal_rfid", relay=1)
```

---

## 🌐 **CLOUDFLARE TUNNEL SETUP**

### **Step 1: Set Up Cloudflare Tunnel**
```bash
# On Raspberry Pi:
cloudflared tunnel --url http://localhost:5001
```

**Output:**
```
Your quick Tunnel has been created! Visit it at:
https://your-random-name.trycloudflare.com
```

### **Step 2: Use in API Client**
```python
api = MaxParkAPI(
    base_url="https://your-random-name.trycloudflare.com",
    api_key="your-api-key",
    verify_ssl=True  # Cloudflare has valid SSL
)

# Now you can access from anywhere!
result = api.get_users()
```

---

## 🔒 **SSL CERTIFICATE TROUBLESHOOTING**

### **Error: SSL Certificate Verify Failed**
```python
# Solution 1: Skip verification (testing only)
api = MaxParkAPI(base_url="...", verify_ssl=False)

# Solution 2: Update CA certificates
# pip install --upgrade certifi

# Solution 3: Use custom CA bundle
api = MaxParkAPI(base_url="...", verify_ssl="/path/to/ca-bundle.crt")
```

### **Error: Certificate Hostname Mismatch**
```python
# For Cloudflare tunnel, make sure you're using the exact URL
# provided by cloudflared (including .trycloudflare.com domain)
```

---

## 📊 **API AUTHENTICATION SUMMARY**

### **Authentication Methods:**

1. **API Key (X-API-Key header):**
   - Used for: Sensitive operations (add/delete/block users, system control)
   - Header: `X-API-Key: your-api-key`
   - Get from: `.env` file on Raspberry Pi (`API_KEY` variable)

2. **Session-based (Login):**
   - Used for: Web dashboard access
   - Not used in API client (API key is simpler)

3. **No Authentication:**
   - Used for: Read-only operations (view users, transactions, status)
   - No credentials needed

---

## 🎯 **SECURITY BEST PRACTICES**

### **1. Protect Your API Key:**
```python
# ❌ Don't hardcode:
api = MaxParkAPI("http://...", api_key="abc123...")

# ✅ Use environment variables:
import os
api_key = os.getenv("MAXPARK_API_KEY")
api = MaxParkAPI("http://...", api_key=api_key)
```

### **2. Use HTTPS in Production:**
```python
# ❌ Don't use HTTP over internet:
api = MaxParkAPI("http://public-ip:5001", ...)

# ✅ Use Cloudflare Tunnel with HTTPS:
api = MaxParkAPI("https://your-tunnel.trycloudflare.com", ...)
```

### **3. Verify SSL Certificates:**
```python
# ❌ Don't skip verification in production:
api = MaxParkAPI("https://...", verify_ssl=False)

# ✅ Verify SSL in production:
api = MaxParkAPI("https://...", verify_ssl=True)
```

---

## 📝 **QUICK REFERENCE**

### **Initialize Client:**
```python
# Local network
api = MaxParkAPI("http://192.168.1.33:5001", api_key="your-api-key", verify_ssl=False)

# Cloudflare tunnel
api = MaxParkAPI("https://tunnel.trycloudflare.com", api_key="your-api-key", verify_ssl=True)
```

### **User Operations:**
```python
api.add_user("card", "name", "id")     # ✅ Requires API key
api.delete_user("card")                # ✅ Requires API key
api.block_user("card")                 # ✅ Requires API key
api.unblock_user("card")               # ✅ Requires API key
api.get_users()                        # ❌ Public
api.search_user("card")                # ❌ Public
```

### **System Control:**
```python
api.control_relay("open_hold", 1)      # ✅ Requires API key
api.system_reset()                     # ✅ Requires API key
api.health_check()                     # ❌ Public
api.internet_status()                  # ❌ Public
```

### **Transactions:**
```python
api.get_transactions()                 # ❌ Public
api.get_today_stats()                  # ❌ Public
api.search_user_transactions("name")   # ❌ Public
```

### **Configuration:**
```python
api.get_config()                       # ❌ Public
api.update_config({...})               # ✅ Requires API key
api.save_upload_config(True, "url")    # ✅ Requires API key
api.get_json_upload_status()           # ❌ Public
```

---

## ✅ **READY TO USE**

**Files Created:**
- ✅ `api_client.py` - Complete API client with all endpoints
- ✅ `API_CLIENT_GUIDE.md` - This documentation

**To Use:**
1. Update `BASE_URL` and `API_KEY` in script
2. Run: `python api_client.py` (tests all public endpoints)
3. Import in your own scripts: `from api_client import MaxParkAPI`

**The API client is ready for both local network and Cloudflare Tunnel!** 🚀

---

**Created:** November 6, 2024  
**Status:** ✅ Production Ready  
**SSL Support:** ✅ Full SSL/TLS support

