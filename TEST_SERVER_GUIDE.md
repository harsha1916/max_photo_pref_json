# 🧪 JSON Upload Test Server - Complete Guide

## 📋 **What is This?**

A simple test server that receives JSON uploads from your Raspberry Pi and saves the images. Use this to verify your JSON upload system is working correctly.

---

## 🚀 **Quick Start**

### **Step 1: Run Test Server (On Your Computer/Another Device)**

```bash
# Install Flask if not already installed
pip install Flask

# Run the test server
python test_json_receiver.py
```

**Expected Output:**
```
======================================================================
🚀 JSON UPLOAD TEST SERVER STARTED
======================================================================

📡 Server Address: http://192.168.1.100:8080

📤 POST Endpoint: http://192.168.1.100:8080/upload

----------------------------------------------------------------------
🔧 CONFIGURATION INSTRUCTIONS:
----------------------------------------------------------------------

1. Open Raspberry Pi web interface
2. Go to Configuration tab
3. Enable 'JSON Base64 Upload Mode' toggle
4. Enter URL: http://192.168.1.100:8080/upload
5. Click 'Save Upload Configuration'

----------------------------------------------------------------------
📊 MONITORING:
----------------------------------------------------------------------

Dashboard: http://192.168.1.100:8080
Statistics: http://192.168.1.100:8080/stats
Images List: http://192.168.1.100:8080/images
Test Server: http://192.168.1.100:8080/test

📁 Received images saved to: ./received_images/
📄 Received JSON saved to: ./received_json/

======================================================================
✅ Server is ready! Waiting for uploads...
======================================================================
```

---

### **Step 2: Configure Raspberry Pi**

1. Open Raspberry Pi web interface: `http://raspberry-pi-ip:5001`
2. Login with credentials
3. Go to **Configuration** tab
4. Find **"Upload Mode Configuration"** section
5. Enable **"Enable JSON Base64 Upload Mode"** toggle
6. Enter URL: `http://YOUR_TEST_SERVER_IP:8080/upload`
7. Click **"Save Upload Configuration"**

---

### **Step 3: Test**

1. Scan an RFID card on Raspberry Pi
2. Watch test server console for activity
3. Check `received_images/` folder for saved image

---

## 📊 **What the Test Server Does**

### **When It Receives Upload:**

```
1. Receives JSON POST request
   ↓
2. Logs all metadata:
   - Card number
   - Reader ID
   - Status
   - User name
   - Timestamp
   ↓
3. Extracts base64 image
   ↓
4. Decodes to JPG binary
   ↓
5. Saves as: cardnumber_readerid_timestamp.jpg
   ↓
6. Saves metadata JSON (without image)
   ↓
7. Updates statistics
   ↓
8. Returns 200 OK response
```

---

## 📁 **File Structure**

After receiving uploads, you'll see:

```
test_json_receiver.py         (the script)
received_images/              (extracted images)
├── 1234567890_r1_1699123456.jpg
├── 9876543210_r2_1699123500.jpg
└── ...

received_json/                (metadata only)
├── 1234567890_r1_1699123456.json
├── 9876543210_r2_1699123500.json
└── ...

receiver_stats.json           (statistics)
```

---

## 📊 **Monitoring Endpoints**

### **1. Web Dashboard**
```
URL: http://your-ip:8080/
```
- Shows real-time statistics
- Auto-refreshes every 5 seconds
- Displays total received, success/fail counts
- Shows total data received in MB

### **2. Statistics API**
```
URL: http://your-ip:8080/stats
Method: GET
```

**Response:**
```json
{
  "total_received": 25,
  "successful": 24,
  "failed": 1,
  "total_size_mb": 12.5,
  "start_time": "2024-11-06T14:00:00",
  "last_received": "2024-11-06T14:30:00"
}
```

### **3. Images List**
```
URL: http://your-ip:8080/images
Method: GET
```

**Response:**
```json
{
  "status": "success",
  "count": 24,
  "images": [
    {
      "filename": "1234567890_r1_1699123456.jpg",
      "size_kb": 512.5,
      "created_at": "2024-11-06T14:30:00"
    }
  ]
}
```

### **4. Test Endpoint**
```
URL: http://your-ip:8080/test
Method: GET
```

**Response:**
```json
{
  "status": "success",
  "message": "Server is running",
  "version": "1.0",
  "endpoint": "/upload",
  "method": "POST"
}
```

### **5. Clear All (For Testing)**
```
URL: http://your-ip:8080/clear
Method: POST
```
Deletes all received images and JSON files, resets statistics.

---

## 🧪 **Testing Scenarios**

### **Test 1: Single Upload**
```bash
# 1. Start test server
python test_json_receiver.py

# 2. Scan 1 card on Raspberry Pi

# 3. Check test server console
# Expected:
# ===================================================
# 📥 RECEIVED JSON UPLOAD #1
# Card Number: 1234567890
# Reader ID: 1
# Status: Access Granted
# User Name: John Doe
# 💾 Image saved: 1234567890_r1_1699123456.jpg (512.5 KB)
# 📄 JSON saved: 1234567890_r1_1699123456.json
# ✅ Upload #1 processed successfully
# ===================================================

# 4. Check received_images folder
ls received_images/
# Expected: 1234567890_r1_1699123456.jpg

# 5. Open dashboard
# Go to: http://your-ip:8080
# Expected: Shows 1 successful upload
```

---

### **Test 2: Multiple Uploads**
```bash
# 1. Scan 10 cards on Raspberry Pi
# 2. Watch test server console (real-time)
# 3. Open dashboard to see count increase
# 4. Check received_images/ folder
ls received_images/*.jpg | wc -l
# Expected: 10 files
```

---

### **Test 3: Offline → Online**
```bash
# 1. Stop test server (Ctrl+C)
# 2. Scan 5 cards on Raspberry Pi (server offline)
# 3. Verify pending on Pi:
#    ssh to Pi: ls json_uploads/pending/
#    Expected: 5 JSON files waiting
# 4. Start test server again
# 5. Wait 60 seconds
# 6. Watch server receive all 5 uploads
# 7. Verify on Pi:
#    ls json_uploads/uploaded/
#    Expected: 5 files moved to uploaded/
```

---

### **Test 4: Image Quality Check**
```bash
# 1. Receive upload
# 2. Open image from received_images/
# 3. Check image quality visually
# 4. Check file size (should be ~500 KB)
# 5. Adjust JSON_IMAGE_QUALITY if needed

# Too blurry? Increase quality:
JSON_IMAGE_QUALITY=85

# Too large? Decrease quality:
JSON_IMAGE_QUALITY=60
```

---

## 🔍 **Console Output Examples**

### **Successful Upload:**
```
============================================================
📥 RECEIVED JSON UPLOAD #1
Card Number: 1234567890
Reader ID: 1
Status: Access Granted
User Name: John Doe
Timestamp: 1699123456
Created At: 2024-11-06T14:30:00
Entity ID: maxpark_entity
💾 Image saved: 1234567890_r1_1699123456.jpg (512.5 KB)
📄 JSON saved: 1234567890_r1_1699123456.json
✅ Upload #1 processed successfully
============================================================
```

### **Failed Upload (Invalid JSON):**
```
============================================================
📥 RECEIVED JSON UPLOAD #2
❌ Error processing upload: No image_base64 field in JSON
============================================================
```

---

## 🛠️ **Troubleshooting**

### **Server Won't Start**

**Error:** `Address already in use`
```bash
# Change port in the script (line near bottom):
app.run(host='0.0.0.0', port=8081)  # Changed from 8080
```

**Error:** `Flask not found`
```bash
pip install Flask
```

---

### **No Uploads Received**

**Check 1: Server accessible?**
```bash
# From Raspberry Pi, test connection:
curl http://test-server-ip:8080/test

# Expected: {"status": "success", ...}
```

**Check 2: URL configured correctly?**
```bash
# On Raspberry Pi:
curl http://localhost:5001/get_json_upload_status

# Check "json_upload_url" matches your test server
```

**Check 3: Firewall blocking?**
```bash
# On test server machine, allow port 8080
# Windows: Check Windows Firewall
# Linux: sudo ufw allow 8080
```

---

### **Images Not Saving**

**Check 1: Folder permissions**
```bash
ls -la received_images/
# Should be writable
```

**Check 2: Disk space**
```bash
df -h
# Make sure there's space available
```

**Check 3: Check logs**
```bash
# Look at test server console output for error messages
```

---

## 📝 **Sample Received JSON File**

**File:** `received_json/1234567890_r1_1699123456.json`

```json
{
  "timestamp": 1699123456,
  "card_number": "1234567890",
  "reader_id": 1,
  "status": "Access Granted",
  "user_name": "John Doe",
  "created_at": "2024-11-06T14:30:00",
  "entity_id": "maxpark_entity",
  "image_filename": "1234567890_r1_1699123456.jpg",
  "image_size_kb": 512.5,
  "received_at": "2024-11-06T14:30:05"
}
```

Note: `image_base64` is NOT saved (to save disk space)

---

## 🎯 **Testing Checklist**

### **Basic Functionality:**
- [ ] Test server starts without errors
- [ ] Dashboard accessible in browser
- [ ] Raspberry Pi can reach server (curl test)
- [ ] JSON mode configured on Pi
- [ ] Card scan triggers upload
- [ ] Image appears in received_images/
- [ ] Console shows upload details
- [ ] Statistics update correctly

### **Image Quality:**
- [ ] Image file size reasonable (~500 KB)
- [ ] Image quality acceptable
- [ ] Compression ratio logged
- [ ] No corrupted images

### **Offline Mode:**
- [ ] Stop server, scan cards on Pi
- [ ] Files queue in Pi's pending/ folder
- [ ] Restart server
- [ ] Files automatically upload
- [ ] Files appear in received_images/

### **Edge Cases:**
- [ ] Invalid JSON handled gracefully
- [ ] Large images handled
- [ ] Multiple simultaneous uploads work
- [ ] Server restart doesn't lose data

---

## 🔧 **Advanced Features**

### **Custom Port:**
Edit line in script:
```python
app.run(host='0.0.0.0', port=8080)  # Change 8080 to your port
```

### **Enable Debug Mode:**
```python
app.run(host='0.0.0.0', port=8080, debug=True)  # More verbose logging
```

### **Add Authentication:**
```python
@app.route('/upload', methods=['POST'])
def upload():
    # Add API key check
    api_key = request.headers.get('X-API-Key')
    if api_key != 'your-secret-key':
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    
    # ... rest of code
```

---

## 📊 **Expected Results**

### **After 10 Card Scans:**

**Test Server Console:**
```
✅ Upload #1 processed successfully
✅ Upload #2 processed successfully
✅ Upload #3 processed successfully
...
✅ Upload #10 processed successfully
```

**received_images/ Folder:**
```
1234567890_r1_1699123456.jpg  (512 KB)
9876543210_r2_1699123460.jpg  (498 KB)
5555555555_r1_1699123465.jpg  (523 KB)
... (10 files total)
```

**Dashboard (http://your-ip:8080):**
```
Total Received: 10
Successful: 10
Failed: 0
Total Data Received: 5.12 MB
```

---

## ✅ **SUCCESS CRITERIA**

Your JSON upload system is working if:

1. ✅ Test server receives uploads
2. ✅ Images saved with correct filenames (cardnumber_readerid_timestamp.jpg)
3. ✅ Image quality is good
4. ✅ File sizes are reasonable (~500 KB)
5. ✅ Metadata is correct (card number, status, etc.)
6. ✅ Dashboard shows statistics
7. ✅ Offline mode works (files queue and upload later)
8. ✅ No errors in either server

---

## 🎯 **WHAT TO CHECK**

### **On Test Server:**
- ✅ Console shows received uploads
- ✅ Images saved to received_images/
- ✅ JSON metadata saved to received_json/
- ✅ Statistics update correctly
- ✅ No errors in console

### **On Raspberry Pi:**
- ✅ Images captured (images/ folder)
- ✅ JSON files created (json_uploads/pending/)
- ✅ Files move to uploaded/ after success
- ✅ Dashboard shows transactions
- ✅ Logs show successful uploads

---

## 🚀 **READY TO TEST!**

**Run this command to start:**
```bash
python test_json_receiver.py
```

**Then configure your Raspberry Pi with the URL shown in the startup message.**

**Scan a card and watch the magic happen!** ✨

---

**Created:** November 6, 2024  
**Purpose:** Test and verify JSON upload functionality  
**Status:** ✅ Ready to use

