#!/usr/bin/env python3
"""
JSON Upload Test Server
-----------------------
Run this on a separate device to test the Raspberry Pi JSON upload functionality.
This server receives JSON payloads with base64 images and saves them locally.

Usage:
    python test_json_receiver.py

Then configure Raspberry Pi with:
    JSON_UPLOAD_URL=http://<this-device-ip>:8080/upload
"""

from flask import Flask, request, jsonify
import json
import base64
import os
import time
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

# Configuration
RECEIVED_IMAGES_DIR = "received_images"
RECEIVED_JSON_DIR = "received_json"
STATS_FILE = "receiver_stats.json"

# Create directories
os.makedirs(RECEIVED_IMAGES_DIR, exist_ok=True)
os.makedirs(RECEIVED_JSON_DIR, exist_ok=True)

# Statistics
stats = {
    "total_received": 0,
    "successful": 0,
    "failed": 0,
    "total_size_mb": 0.0,
    "start_time": datetime.now().isoformat(),
    "last_received": None
}

def load_stats():
    """Load statistics from file."""
    global stats
    try:
        if os.path.exists(STATS_FILE):
            with open(STATS_FILE, 'r') as f:
                stats = json.load(f)
    except:
        pass

def save_stats():
    """Save statistics to file."""
    try:
        with open(STATS_FILE, 'w') as f:
            json.dump(stats, f, indent=2)
    except Exception as e:
        logger.error(f"Error saving stats: {e}")

@app.route('/')
def home():
    """Home page with statistics."""
    return f"""
    <html>
    <head>
        <title>JSON Upload Test Server</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
            .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            h1 {{ color: #333; border-bottom: 3px solid #4CAF50; padding-bottom: 10px; }}
            .stats {{ background: #f9f9f9; padding: 20px; border-radius: 5px; margin: 20px 0; }}
            .stat-row {{ display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #ddd; }}
            .stat-label {{ font-weight: bold; color: #555; }}
            .stat-value {{ color: #4CAF50; font-weight: bold; }}
            .endpoint {{ background: #333; color: #0f0; padding: 15px; border-radius: 5px; font-family: monospace; margin: 20px 0; }}
            .success {{ color: #4CAF50; }}
            .error {{ color: #f44336; }}
            .folder {{ background: #e3f2fd; padding: 10px; margin: 10px 0; border-left: 4px solid #2196F3; }}
        </style>
        <meta http-equiv="refresh" content="5">
    </head>
    <body>
        <div class="container">
            <h1>🚀 JSON Upload Test Server</h1>
            <p>Status: <span class="success">● RUNNING</span></p>
            
            <div class="endpoint">
                <strong>POST Endpoint:</strong> http://YOUR_IP:8080/upload<br>
                <strong>Status Endpoint:</strong> http://YOUR_IP:8080/stats
            </div>
            
            <div class="stats">
                <h2>📊 Statistics</h2>
                <div class="stat-row">
                    <span class="stat-label">Total Received:</span>
                    <span class="stat-value">{stats['total_received']}</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Successful:</span>
                    <span class="stat-value success">{stats['successful']}</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Failed:</span>
                    <span class="stat-value error">{stats['failed']}</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Total Data Received:</span>
                    <span class="stat-value">{stats['total_size_mb']:.2f} MB</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Server Started:</span>
                    <span class="stat-value">{stats['start_time']}</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Last Received:</span>
                    <span class="stat-value">{stats['last_received'] or 'Never'}</span>
                </div>
            </div>
            
            <div class="folder">
                <strong>📁 Saved Images:</strong> {RECEIVED_IMAGES_DIR}/<br>
                <strong>📄 Saved JSON:</strong> {RECEIVED_JSON_DIR}/
            </div>
            
            <p style="color: #888; font-size: 12px; margin-top: 30px;">
                Auto-refreshes every 5 seconds • Press Ctrl+C in terminal to stop
            </p>
        </div>
    </body>
    </html>
    """

@app.route('/upload', methods=['POST'])
def upload():
    """
    Receive JSON upload from Raspberry Pi.
    Expected JSON format:
    {
        "image_base64": "data:image/jpeg;base64,...",
        "timestamp": 1699123456,
        "card_number": "1234567890",
        "reader_id": 1,
        "status": "Access Granted",
        "user_name": "John Doe",
        "created_at": "2024-11-06T14:30:00",
        "entity_id": "your_entity"
    }
    """
    global stats
    stats['total_received'] += 1
    
    try:
        # Get JSON data
        data = request.get_json()
        
        if not data:
            logger.error("No JSON data received")
            stats['failed'] += 1
            save_stats()
            return jsonify({"status": "error", "message": "No JSON data"}), 400
        
        # Log received data
        logger.info("=" * 60)
        logger.info(f"📥 RECEIVED JSON UPLOAD #{stats['total_received']}")
        logger.info(f"Card Number: {data.get('card_number', 'N/A')}")
        logger.info(f"Reader ID: {data.get('reader_id', 'N/A')}")
        logger.info(f"Status: {data.get('status', 'N/A')}")
        logger.info(f"User Name: {data.get('user_name', 'N/A')}")
        logger.info(f"Timestamp: {data.get('timestamp', 'N/A')}")
        logger.info(f"Created At: {data.get('created_at', 'N/A')}")
        logger.info(f"Entity ID: {data.get('entity_id', 'N/A')}")
        
        # Extract base64 image
        image_base64 = data.get('image_base64', '')
        if not image_base64:
            logger.error("No image_base64 field in JSON")
            stats['failed'] += 1
            save_stats()
            return jsonify({"status": "error", "message": "No image_base64 field"}), 400
        
        # Remove data URI prefix if present
        if ',' in image_base64:
            image_base64 = image_base64.split(',', 1)[1]
        
        # Decode base64
        try:
            image_data = base64.b64decode(image_base64)
        except Exception as e:
            logger.error(f"Failed to decode base64: {e}")
            stats['failed'] += 1
            save_stats()
            return jsonify({"status": "error", "message": f"Invalid base64: {str(e)}"}), 400
        
        # Create filename: cardnumber_readerid_timestamp.jpg
        card_number = data.get('card_number', 'unknown')
        reader_id = data.get('reader_id', '0')
        timestamp = data.get('timestamp', int(time.time()))
        
        filename = f"{card_number}_r{reader_id}_{timestamp}.jpg"
        image_path = os.path.join(RECEIVED_IMAGES_DIR, filename)
        
        # Save image
        with open(image_path, 'wb') as f:
            f.write(image_data)
        
        image_size_kb = len(image_data) / 1024
        logger.info(f"💾 Image saved: {filename} ({image_size_kb:.1f} KB)")
        
        # Save JSON metadata (without base64 to save space)
        json_metadata = {k: v for k, v in data.items() if k != 'image_base64'}
        json_metadata['image_filename'] = filename
        json_metadata['image_size_kb'] = round(image_size_kb, 2)
        json_metadata['received_at'] = datetime.now().isoformat()
        
        json_filename = filename.replace('.jpg', '.json')
        json_path = os.path.join(RECEIVED_JSON_DIR, json_filename)
        
        with open(json_path, 'w') as f:
            json.dump(json_metadata, f, indent=2)
        
        logger.info(f"📄 JSON saved: {json_filename}")
        
        # Update statistics
        stats['successful'] += 1
        stats['total_size_mb'] += image_size_kb / 1024
        stats['last_received'] = datetime.now().isoformat()
        save_stats()
        
        logger.info(f"✅ Upload #{stats['total_received']} processed successfully")
        logger.info("=" * 60)
        
        # Return success response
        return jsonify({
            "status": "success",
            "message": "Upload received successfully",
            "filename": filename,
            "size_kb": round(image_size_kb, 2),
            "card_number": card_number,
            "reader_id": reader_id,
            "timestamp": timestamp
        }), 200
        
    except Exception as e:
        logger.error(f"❌ Error processing upload: {e}")
        stats['failed'] += 1
        save_stats()
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get server statistics."""
    return jsonify(stats)

@app.route('/test', methods=['GET'])
def test():
    """Test endpoint to verify server is running."""
    return jsonify({
        "status": "success",
        "message": "Server is running",
        "version": "1.0",
        "endpoint": "/upload",
        "method": "POST"
    })

@app.route('/images', methods=['GET'])
def list_images():
    """List all received images."""
    try:
        images = []
        if os.path.exists(RECEIVED_IMAGES_DIR):
            for filename in sorted(os.listdir(RECEIVED_IMAGES_DIR)):
                if filename.endswith('.jpg'):
                    filepath = os.path.join(RECEIVED_IMAGES_DIR, filename)
                    size = os.path.getsize(filepath)
                    mtime = os.path.getmtime(filepath)
                    
                    images.append({
                        "filename": filename,
                        "size_kb": round(size / 1024, 2),
                        "created_at": datetime.fromtimestamp(mtime).isoformat()
                    })
        
        return jsonify({
            "status": "success",
            "count": len(images),
            "images": images
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/clear', methods=['POST'])
def clear_all():
    """Clear all received images and JSON files (for testing)."""
    try:
        deleted_count = 0
        
        # Delete images
        if os.path.exists(RECEIVED_IMAGES_DIR):
            for filename in os.listdir(RECEIVED_IMAGES_DIR):
                filepath = os.path.join(RECEIVED_IMAGES_DIR, filename)
                os.remove(filepath)
                deleted_count += 1
        
        # Delete JSON files
        if os.path.exists(RECEIVED_JSON_DIR):
            for filename in os.listdir(RECEIVED_JSON_DIR):
                filepath = os.path.join(RECEIVED_JSON_DIR, filename)
                os.remove(filepath)
                deleted_count += 1
        
        # Reset stats
        global stats
        stats = {
            "total_received": 0,
            "successful": 0,
            "failed": 0,
            "total_size_mb": 0.0,
            "start_time": datetime.now().isoformat(),
            "last_received": None
        }
        save_stats()
        
        logger.info(f"🗑️ Cleared {deleted_count} files")
        
        return jsonify({
            "status": "success",
            "message": f"Cleared {deleted_count} files",
            "deleted_count": deleted_count
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


def print_startup_info():
    """Print server startup information."""
    import socket
    
    # Get local IP address
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except:
        local_ip = "localhost"
    
    print("\n" + "=" * 70)
    print("🚀 JSON UPLOAD TEST SERVER STARTED")
    print("=" * 70)
    print(f"\n📡 Server Address: http://{local_ip}:8080")
    print(f"\n📤 POST Endpoint: http://{local_ip}:8080/upload")
    print("\n" + "-" * 70)
    print("🔧 CONFIGURATION INSTRUCTIONS:")
    print("-" * 70)
    print(f"\n1. Open Raspberry Pi web interface")
    print(f"2. Go to Configuration tab")
    print(f"3. Enable 'JSON Base64 Upload Mode' toggle")
    print(f"4. Enter URL: http://{local_ip}:8080/upload")
    print(f"5. Click 'Save Upload Configuration'")
    print(f"\n" + "-" * 70)
    print("📊 MONITORING:")
    print("-" * 70)
    print(f"\nDashboard: http://{local_ip}:8080")
    print(f"Statistics: http://{local_ip}:8080/stats")
    print(f"Images List: http://{local_ip}:8080/images")
    print(f"Test Server: http://{local_ip}:8080/test")
    print(f"\n📁 Received images saved to: ./{RECEIVED_IMAGES_DIR}/")
    print(f"📄 Received JSON saved to: ./{RECEIVED_JSON_DIR}/")
    print(f"\n" + "=" * 70)
    print("✅ Server is ready! Waiting for uploads...")
    print("=" * 70)
    print("\nPress Ctrl+C to stop the server\n")


if __name__ == '__main__':
    # Load existing stats
    load_stats()
    
    # Print startup information
    print_startup_info()
    
    # Start Flask server
    try:
        app.run(
            host='0.0.0.0',  # Listen on all interfaces
            port=8080,
            debug=False,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        print(f"📊 Final Statistics:")
        print(f"   Total Received: {stats['total_received']}")
        print(f"   Successful: {stats['successful']}")
        print(f"   Failed: {stats['failed']}")
        print(f"   Total Data: {stats['total_size_mb']:.2f} MB")
        print("\n👋 Goodbye!\n")

