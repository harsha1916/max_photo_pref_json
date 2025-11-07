#!/usr/bin/env python3
"""
MaxPark RFID System - API Client
---------------------------------
Complete API client for all system operations.
Supports both local network and Cloudflare Tunnel with SSL.

Usage:
    from api_client import MaxParkAPI
    
    # For local network
    api = MaxParkAPI("http://192.168.1.33:5001", api_key="your-api-key")
    
    # For Cloudflare tunnel
    api = MaxParkAPI("https://your-tunnel.trycloudflare.com", api_key="your-api-key", verify_ssl=True)
    
    # Add user
    result = api.add_user("1234567890", "John Doe", "user123")
    print(result)
"""

import requests
import json
from typing import Optional, Dict, List, Any
from urllib3.exceptions import InsecureRequestWarning
import warnings

class MaxParkAPI:
    """
    Complete API client for MaxPark RFID Access Control System.
    
    Supports:
    - Local network connections
    - Cloudflare Tunnel with SSL
    - All API endpoints (authenticated and public)
    """
    
    def __init__(
        self, 
        base_url: str, 
        api_key: Optional[str] = None,
        verify_ssl: bool = True,
        timeout: int = 30
    ):
        """
        Initialize API client.
        
        Args:
            base_url: Base URL (e.g., "http://192.168.1.33:5001" or "https://tunnel.trycloudflare.com")
            api_key: API key for authenticated endpoints
            verify_ssl: Verify SSL certificates (True for production, False for testing)
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.verify_ssl = verify_ssl
        self.timeout = timeout
        self.session = requests.Session()
        
        # Disable SSL warnings if verify_ssl is False
        if not verify_ssl:
            warnings.simplefilter('ignore', InsecureRequestWarning)
            self.session.verify = False
        
        # Set default headers
        self.session.headers.update({
            'User-Agent': 'MaxPark-API-Client/1.0',
            'Accept': 'application/json'
        })
    
    def _get_headers(self, authenticated: bool = False, content_type: str = 'application/json') -> Dict[str, str]:
        """Get request headers with optional API key."""
        headers = {'Content-Type': content_type}
        if authenticated and self.api_key:
            headers['X-API-Key'] = self.api_key
        return headers
    
    def _request(
        self, 
        method: str, 
        endpoint: str, 
        authenticated: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """Make HTTP request with error handling."""
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers(authenticated)
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=headers,
                timeout=self.timeout,
                verify=self.verify_ssl,
                **kwargs
            )
            
            # Try to parse JSON response
            try:
                return response.json()
            except:
                # If not JSON, return text
                return {"status": "success", "text": response.text, "status_code": response.status_code}
                
        except requests.exceptions.SSLError as e:
            return {"status": "error", "message": f"SSL Error: {str(e)}", "hint": "Try verify_ssl=False for testing"}
        except requests.exceptions.ConnectionError as e:
            return {"status": "error", "message": f"Connection Error: {str(e)}"}
        except requests.exceptions.Timeout:
            return {"status": "error", "message": "Request timeout"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    # ====================================
    # USER MANAGEMENT (Requires API Key)
    # ====================================
    
    def add_user(self, card_number: str, name: str, user_id: str) -> Dict[str, Any]:
        """
        Add a new user.
        
        Args:
            card_number: Card number (numeric string)
            name: User's full name
            user_id: Unique user ID
        
        Returns:
            Response dict with status
            
        Authentication: API Key Required ✅
        """
        params = {
            'card_number': card_number,
            'name': name,
            'id': user_id
        }
        return self._request('GET', f'/add_user', authenticated=True, params=params)
    
    def delete_user(self, card_number: str) -> Dict[str, Any]:
        """
        Delete a user.
        
        Args:
            card_number: Card number to delete
        
        Returns:
            Response dict with status
            
        Authentication: API Key Required ✅
        """
        params = {'card_number': card_number}
        return self._request('GET', f'/delete_user', authenticated=True, params=params)
    
    def block_user(self, card_number: str) -> Dict[str, Any]:
        """
        Block a user.
        
        Args:
            card_number: Card number to block
        
        Returns:
            Response dict with status
            
        Authentication: API Key Required ✅
        """
        params = {'card_number': card_number}
        return self._request('GET', f'/block_user', authenticated=True, params=params)
    
    def unblock_user(self, card_number: str) -> Dict[str, Any]:
        """
        Unblock a user.
        
        Args:
            card_number: Card number to unblock
        
        Returns:
            Response dict with status
            
        Authentication: API Key Required ✅
        """
        params = {'card_number': card_number}
        return self._request('GET', f'/unblock_user', authenticated=True, params=params)
    
    def get_users(self) -> Dict[str, Any]:
        """
        Get list of all users.
        
        Returns:
            Response dict with users list
            
        Authentication: None (Public) ❌
        """
        return self._request('GET', '/get_users')
    
    def search_user(self, card_number: str) -> Dict[str, Any]:
        """
        Search for a specific user.
        
        Args:
            card_number: Card number to search
        
        Returns:
            Response dict with user info
            
        Authentication: None (Public) ❌
        """
        params = {'card_number': card_number}
        return self._request('GET', '/search_user', params=params)
    
    # ====================================
    # RELAY CONTROL (Requires API Key)
    # ====================================
    
    def control_relay(self, action: str, relay: int) -> Dict[str, Any]:
        """
        Control relay (gate/barrier).
        
        Args:
            action: "open_hold", "close_hold", "normal_rfid", or "normal"
            relay: Relay number (1, 2, or 3)
        
        Returns:
            Response dict with status
            
        Authentication: API Key Required ✅
        """
        params = {
            'action': action,
            'relay': str(relay)
        }
        return self._request('GET', '/relay', authenticated=True, params=params)
    
    # ====================================
    # TRANSACTIONS (Public)
    # ====================================
    
    def get_transactions(self) -> Dict[str, Any]:
        """
        Get recent transactions (last 10).
        
        Returns:
            List of recent transactions
            
        Authentication: None (Public) ❌
        """
        return self._request('GET', '/get_transactions')
    
    def get_today_stats(self) -> Dict[str, Any]:
        """
        Get today's statistics.
        
        Returns:
            Today's access stats
            
        Authentication: None (Public) ❌
        """
        return self._request('GET', '/get_today_stats')
    
    def search_user_transactions(self, name: str, date_range: str = "today") -> Dict[str, Any]:
        """
        Search transactions by user name.
        
        Args:
            name: User name to search
            date_range: "today", "week", "month", or "all"
        
        Returns:
            List of matching transactions
            
        Authentication: None (Public) ❌
        """
        params = {
            'name': name,
            'range': date_range
        }
        return self._request('GET', '/search_user_transactions', params=params)
    
    def sync_transactions(self) -> Dict[str, Any]:
        """
        Manually trigger transaction sync to Firestore.
        
        Returns:
            Sync status
            
        Authentication: API Key Required ✅
        """
        return self._request('POST', '/sync_transactions', authenticated=True)
    
    def transaction_cache_status(self) -> Dict[str, Any]:
        """
        Get transaction cache status.
        
        Returns:
            Cache statistics
            
        Authentication: None (Public) ❌
        """
        return self._request('GET', '/transaction_cache_status')
    
    def cleanup_old_transactions(self) -> Dict[str, Any]:
        """
        Cleanup transactions older than retention period.
        
        Returns:
            Cleanup result
            
        Authentication: API Key Required ✅
        """
        return self._request('POST', '/cleanup_old_transactions', authenticated=True)
    
    # ====================================
    # IMAGE MANAGEMENT
    # ====================================
    
    def get_images(self, limit: int = 100) -> Dict[str, Any]:
        """
        Get list of captured images.
        
        Args:
            limit: Maximum number of images to return
        
        Returns:
            List of images with upload status
            
        Authentication: None (Public) ❌
        """
        params = {'limit': limit}
        return self._request('GET', '/get_images', params=params)
    
    def delete_image(self, filename: str) -> Dict[str, Any]:
        """
        Delete an image file.
        
        Args:
            filename: Image filename to delete
        
        Returns:
            Deletion status
            
        Authentication: API Key Required ✅
        """
        return self._request('DELETE', f'/delete_image/{filename}', authenticated=True)
    
    def get_offline_images(self) -> Dict[str, Any]:
        """
        Get images that haven't been uploaded yet.
        
        Returns:
            List of offline images
            
        Authentication: None (Public) ❌
        """
        return self._request('GET', '/get_offline_images')
    
    def force_image_upload(self) -> Dict[str, Any]:
        """
        Force immediate image upload.
        
        Returns:
            Upload trigger status
            
        Authentication: API Key Required ✅
        """
        return self._request('POST', '/force_image_upload', authenticated=True)
    
    def clear_all_offline_images(self) -> Dict[str, Any]:
        """
        Clear all offline images.
        
        Returns:
            Deletion count
            
        Authentication: API Key Required ✅
        """
        return self._request('POST', '/clear_all_offline_images', authenticated=True)
    
    # ====================================
    # CONFIGURATION (Requires API Key)
    # ====================================
    
    def get_config(self) -> Dict[str, Any]:
        """
        Get current system configuration.
        
        Returns:
            Configuration dict
            
        Authentication: None (Public) ❌
        """
        return self._request('GET', '/get_config')
    
    def update_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update system configuration.
        
        Args:
            config: Configuration dict with settings
        
        Returns:
            Update status
            
        Authentication: API Key Required ✅
        """
        return self._request('POST', '/update_config', authenticated=True, json=config)
    
    # ====================================
    # JSON UPLOAD CONFIGURATION
    # ====================================
    
    def save_upload_config(self, json_enabled: bool, json_url: str = "") -> Dict[str, Any]:
        """
        Save JSON upload configuration.
        
        Args:
            json_enabled: Enable JSON upload mode
            json_url: Custom API URL for JSON uploads
        
        Returns:
            Configuration save status
            
        Authentication: API Key Required ✅
        """
        data = {
            'json_upload_enabled': json_enabled,
            'json_upload_url': json_url
        }
        return self._request('POST', '/save_upload_config', authenticated=True, json=data)
    
    def get_json_upload_status(self) -> Dict[str, Any]:
        """
        Get JSON upload status and statistics.
        
        Returns:
            JSON upload status dict
            
        Authentication: None (Public) ❌
        """
        return self._request('GET', '/get_json_upload_status')
    
    # ====================================
    # PHOTO PREFERENCES
    # ====================================
    
    def get_photo_preferences(self) -> Dict[str, Any]:
        """
        Get photo capture preferences.
        
        Returns:
            Photo preferences dict
            
        Authentication: None (Public) ❌
        """
        return self._request('GET', '/get_photo_preferences')
    
    def save_global_photo_settings(self, capture_registered: bool) -> Dict[str, Any]:
        """
        Save global photo settings.
        
        Args:
            capture_registered: Whether to capture photos for registered vehicles
        
        Returns:
            Save status
            
        Authentication: None (Public) ❌
        """
        data = {'capture_registered_vehicles': capture_registered}
        return self._request('POST', '/save_global_photo_settings', json=data)
    
    def add_photo_preference(
        self, 
        identifier: str, 
        skip_photo: bool, 
        pref_type: str = "card"
    ) -> Dict[str, Any]:
        """
        Add photo preference for card or user.
        
        Args:
            identifier: Card number or user name
            skip_photo: Whether to skip photo capture
            pref_type: "card" or "user"
        
        Returns:
            Save status
            
        Authentication: None (Public) ❌
        """
        data = {
            'identifier': identifier,
            'skip_photo': skip_photo,
            'type': pref_type
        }
        return self._request('POST', '/add_photo_preference', json=data)
    
    def remove_photo_preference(self, identifier: str, pref_type: str = "card") -> Dict[str, Any]:
        """
        Remove photo preference.
        
        Args:
            identifier: Card number or user name
            pref_type: "card" or "user"
        
        Returns:
            Removal status
            
        Authentication: None (Public) ❌
        """
        data = {
            'identifier': identifier,
            'type': pref_type
        }
        return self._request('POST', '/remove_photo_preference', json=data)
    
    # ====================================
    # NETWORK CONFIGURATION (Requires API Key)
    # ====================================
    
    def get_network_status(self) -> Dict[str, Any]:
        """
        Get current network status.
        
        Returns:
            Network status dict
            
        Authentication: None (Public) ❌
        """
        return self._request('GET', '/get_network_status')
    
    def apply_network_config(
        self, 
        static_ip: str, 
        static_gateway: str = "192.168.1.1",
        static_dns: str = "8.8.8.8"
    ) -> Dict[str, Any]:
        """
        Apply static IP network configuration.
        
        Args:
            static_ip: Static IP address
            static_gateway: Gateway address
            static_dns: DNS server
        
        Returns:
            Configuration status
            
        Authentication: API Key Required ✅
        """
        data = {
            'static_ip': static_ip,
            'static_gateway': static_gateway,
            'static_dns': static_dns
        }
        return self._request('POST', '/apply_network_config', authenticated=True, json=data)
    
    def reset_network_dhcp(self) -> Dict[str, Any]:
        """
        Reset network to DHCP mode.
        
        Returns:
            Reset status
            
        Authentication: API Key Required ✅
        """
        return self._request('POST', '/reset_network_dhcp', authenticated=True)
    
    # ====================================
    # STORAGE & CLEANUP (Some require API Key)
    # ====================================
    
    def get_storage_stats(self) -> Dict[str, Any]:
        """
        Get storage statistics.
        
        Returns:
            Storage stats dict
            
        Authentication: None (Public) ❌
        """
        return self._request('GET', '/get_storage_stats')
    
    def get_storage_info(self) -> Dict[str, Any]:
        """
        Get storage information.
        
        Returns:
            Storage info dict
            
        Authentication: None (Public) ❌
        """
        return self._request('GET', '/get_storage_info')
    
    def trigger_storage_cleanup(self) -> Dict[str, Any]:
        """
        Manually trigger storage cleanup.
        
        Returns:
            Cleanup result
            
        Authentication: API Key Required ✅
        """
        return self._request('POST', '/trigger_storage_cleanup', authenticated=True)
    
    # ====================================
    # SYSTEM CONTROL (Requires API Key)
    # ====================================
    
    def system_reset(self) -> Dict[str, Any]:
        """
        Restart the system.
        
        Returns:
            Reset confirmation
            
        Authentication: API Key Required ✅
        """
        return self._request('POST', '/system_reset', authenticated=True)
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check system health.
        
        Returns:
            Health status dict
            
        Authentication: None (Public) ❌
        """
        return self._request('GET', '/health_check')
    
    def internet_status(self, force: bool = False) -> Dict[str, Any]:
        """
        Get internet connection status.
        
        Args:
            force: Force fresh check (ignore cache)
        
        Returns:
            Internet status dict
            
        Authentication: None (Public) ❌
        """
        params = {'force': 'true'} if force else {}
        return self._request('GET', '/internet_status', params=params)
    
    # ====================================
    # PASSWORD MANAGEMENT (Requires API Key)
    # ====================================
    
    def reset_password(self, new_password: str = "admin123") -> Dict[str, Any]:
        """
        Reset admin password.
        
        Args:
            new_password: New password to set
        
        Returns:
            Reset status
            
        Authentication: API Key Required ✅
        """
        data = {'new_password': new_password}
        return self._request('POST', '/reset_password', authenticated=True, json=data)
    
    def get_password_info(self) -> Dict[str, Any]:
        """
        Get password information.
        
        Returns:
            Password info dict
            
        Authentication: API Key Required ✅
        """
        return self._request('GET', '/get_password_info', authenticated=True)


# ====================================
# EXAMPLE USAGE
# ====================================

def main():
    """Example usage of API client."""
    
    print("=" * 70)
    print("MaxPark RFID System - API Client")
    print("=" * 70)
    
    # Configuration
    BASE_URL = "http://192.168.1.33:5001"  # Change to your Raspberry Pi IP
    API_KEY = "your-api-key-change-this"   # Change to your API key
    
    # For Cloudflare Tunnel:
    # BASE_URL = "https://your-tunnel.trycloudflare.com"
    # VERIFY_SSL = True  # Set to False for self-signed certs
    
    # Initialize API client
    api = MaxParkAPI(BASE_URL, api_key=API_KEY, verify_ssl=False)
    
    print(f"\n🔗 Connected to: {BASE_URL}")
    print(f"🔑 API Key: {API_KEY[:10]}...")
    print("\n" + "=" * 70)
    
    # ====================================
    # Test API Endpoints
    # ====================================
    
    print("\n1️⃣ Testing Health Check (Public)")
    print("-" * 70)
    result = api.health_check()
    print(json.dumps(result, indent=2))
    
    print("\n2️⃣ Testing Get Users (Public)")
    print("-" * 70)
    result = api.get_users()
    print(f"Total users: {len(result.get('users', []))}")
    
    print("\n3️⃣ Testing Get Transactions (Public)")
    print("-" * 70)
    result = api.get_transactions()
    if isinstance(result, list):
        print(f"Recent transactions: {len(result)}")
        if result:
            print(f"Latest: {result[0].get('name')} - {result[0].get('status')}")
    
    print("\n4️⃣ Testing JSON Upload Status (Public)")
    print("-" * 70)
    result = api.get_json_upload_status()
    print(json.dumps(result, indent=2))
    
    print("\n5️⃣ Testing Internet Status (Public)")
    print("-" * 70)
    result = api.internet_status()
    print(f"Internet available: {result.get('internet_available', 'Unknown')}")
    
    # ====================================
    # Authenticated Operations (Uncomment to test)
    # ====================================
    
    # print("\n6️⃣ Testing Add User (API Key Required)")
    # print("-" * 70)
    # result = api.add_user("9999999999", "Test User", "test123")
    # print(json.dumps(result, indent=2))
    
    # print("\n7️⃣ Testing Block User (API Key Required)")
    # print("-" * 70)
    # result = api.block_user("9999999999")
    # print(json.dumps(result, indent=2))
    
    # print("\n8️⃣ Testing Unblock User (API Key Required)")
    # print("-" * 70)
    # result = api.unblock_user("9999999999")
    # print(json.dumps(result, indent=2))
    
    # print("\n9️⃣ Testing Delete User (API Key Required)")
    # print("-" * 70)
    # result = api.delete_user("9999999999")
    # print(json.dumps(result, indent=2))
    
    print("\n" + "=" * 70)
    print("✅ API Tests Complete")
    print("=" * 70)


if __name__ == '__main__':
    main()

