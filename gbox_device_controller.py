"""
GBOX Device Controller Implementation
Provides real device control using GBOX SDK for AndroidWorld tasks
"""

import os
import time
import logging
from typing import Dict, Any, Optional, Tuple
from abc import ABC, abstractmethod

try:
    from gbox_sdk import GBoxClient, Device
    GBOX_AVAILABLE = True
except ImportError:
    GBOX_AVAILABLE = False
    print("⚠️  GBOX SDK not available. Install with: pip install gbox-sdk")

from custom_agent import DeviceController

class GBOXDeviceController(DeviceController):
    """Real device controller using GBOX SDK"""
    
    def __init__(self, device_id: str, gbox_api_key: Optional[str] = None):
        super().__init__(device_id)
        self.gbox_api_key = gbox_api_key or os.getenv('GBOX_API_KEY')
        self.client = None
        self.device = None
        
        if not self.gbox_api_key:
            raise ValueError("GBOX_API_KEY environment variable required")
        
        if GBOX_AVAILABLE:
            self._initialize_gbox()
        else:
            raise RuntimeError("GBOX SDK not available")
    
    def _initialize_gbox(self):
        """Initialize GBOX client and connect to device"""
        try:
            self.client = GBoxClient(api_key=self.gbox_api_key)
            self.device = self.client.get_device(self.device_id)
            logging.info(f"✅ Connected to GBOX device: {self.device_id}")
        except Exception as e:
            logging.error(f"❌ Failed to connect to GBOX device: {e}")
            raise
    
    def click(self, x: int, y: int) -> bool:
        """Click at specific coordinates using GBOX"""
        try:
            if self.device:
                self.device.click(x, y)
                logging.info(f"🖱️  GBOX: Clicked at ({x}, {y})")
                return True
            return False
        except Exception as e:
            logging.error(f"❌ GBOX click failed: {e}")
            return False
    
    def type_text(self, text: str) -> bool:
        """Type text using GBOX"""
        try:
            if self.device:
                self.device.type_text(text)
                logging.info(f"⌨️  GBOX: Typed text: '{text}'")
                return True
            return False
        except Exception as e:
            logging.error(f"❌ GBOX type_text failed: {e}")
            return False
    
    def swipe(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: float = 0.5) -> bool:
        """Swipe between coordinates using GBOX"""
        try:
            if self.device:
                self.device.swipe(start_x, start_y, end_x, end_y, duration)
                logging.info(f"👆 GBOX: Swiped from ({start_x}, {start_y}) to ({end_x}, {end_y})")
                return True
            return False
        except Exception as e:
            logging.error(f"❌ GBOX swipe failed: {e}")
            return False
    
    def get_screen_text(self) -> str:
        """Get screen text using GBOX OCR"""
        try:
            if self.device:
                text = self.device.get_screen_text()
                logging.info(f"📱 GBOX: Retrieved screen text ({len(text)} chars)")
                return text
            return ""
        except Exception as e:
            logging.error(f"❌ GBOX get_screen_text failed: {e}")
            return ""
    
    def take_screenshot(self) -> Optional[bytes]:
        """Take screenshot using GBOX"""
        try:
            if self.device:
                screenshot = self.device.take_screenshot()
                logging.info(f"📸 GBOX: Screenshot captured ({len(screenshot)} bytes)")
                return screenshot
            return None
        except Exception as e:
            logging.error(f"❌ GBOX screenshot failed: {e}")
            return None
    
    def is_connected(self) -> bool:
        """Check if device is connected via GBOX"""
        return self.device is not None and self.device.is_connected()
    
    def get_device_info(self) -> Dict[str, Any]:
        """Get device information from GBOX"""
        try:
            if self.device:
                info = {
                    'id': self.device.id,
                    'name': self.device.name,
                    'model': self.device.model,
                    'android_version': self.device.android_version,
                    'connected': self.device.is_connected()
                }
                return info
            return {}
        except Exception as e:
            logging.error(f"❌ GBOX get_device_info failed: {e}")
            return {}

class GBOXLocalDeviceController(DeviceController):
    """Local device controller using GBOX for emulator/ADB devices"""
    
    def __init__(self, device_id: str, gbox_api_key: Optional[str] = None):
        super().__init__(device_id)
        self.gbox_api_key = gbox_api_key or os.getenv('GBOX_API_KEY')
        self.client = None
        self.device = None
        
        if not self.gbox_api_key:
            raise ValueError("GBOX_API_KEY environment variable required")
        
        if GBOX_AVAILABLE:
            self._initialize_local_gbox()
        else:
            raise RuntimeError("GBOX SDK not available")
    
    def _initialize_local_gbox(self):
        """Initialize GBOX client for local device"""
        try:
            self.client = GBoxClient(api_key=self.gbox_api_key)
            # For local devices, we need to register them first
            self.device = self.client.register_local_device(self.device_id)
            logging.info(f"✅ Registered local device with GBOX: {self.device_id}")
        except Exception as e:
            logging.error(f"❌ Failed to register local device: {e}")
            raise
    
    def click(self, x: int, y: int) -> bool:
        """Click at specific coordinates using local GBOX"""
        try:
            if self.device:
                self.device.click(x, y)
                logging.info(f"🖱️  Local GBOX: Clicked at ({x}, {y})")
                return True
            return False
        except Exception as e:
            logging.error(f"❌ Local GBOX click failed: {e}")
            return False
    
    def type_text(self, text: str) -> bool:
        """Type text using local GBOX"""
        try:
            if self.device:
                self.device.type_text(text)
                logging.info(f"⌨️  Local GBOX: Typed text: '{text}'")
                return True
            return False
        except Exception as e:
            logging.error(f"❌ Local GBOX type_text failed: {e}")
            return False
    
    def swipe(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: float = 0.5) -> bool:
        """Swipe between coordinates using local GBOX"""
        try:
            if self.device:
                self.device.swipe(start_x, start_y, end_x, end_y, duration)
                logging.info(f"👆 Local GBOX: Swiped from ({start_x}, {start_y}) to ({end_x}, {end_y})")
                return True
            return False
        except Exception as e:
            logging.error(f"❌ Local GBOX swipe failed: {e}")
            return False
    
    def get_screen_text(self) -> str:
        """Get screen text using local GBOX OCR"""
        try:
            if self.device:
                text = self.device.get_screen_text()
                logging.info(f"📱 Local GBOX: Retrieved screen text ({len(text)} chars)")
                return text
            return ""
        except Exception as e:
            logging.error(f"❌ Local GBOX get_screen_text failed: {e}")
            return ""
    
    def take_screenshot(self) -> Optional[bytes]:
        """Take screenshot using local GBOX"""
        try:
            if self.device:
                screenshot = self.device.take_screenshot()
                logging.info(f"📸 Local GBOX: Screenshot captured ({len(screenshot)} bytes)")
                return screenshot
            return None
        except Exception as e:
            logging.error(f"❌ Local GBOX screenshot failed: {e}")
            return None
    
    def is_connected(self) -> bool:
        """Check if local device is connected via GBOX"""
        return self.device is not None and self.device.is_connected()
    
    def get_device_info(self) -> Dict[str, Any]:
        """Get local device information from GBOX"""
        try:
            if self.device:
                info = {
                    'id': self.device.id,
                    'name': self.device.name,
                    'model': self.device.model,
                    'android_version': self.device.android_version,
                    'connected': self.device.is_connected(),
                    'type': 'local_device'
                }
                return info
            return {}
        except Exception as e:
            logging.error(f"❌ Local GBOX get_device_info failed: {e}")
            return {}

if __name__ == "__main__":
    # Test the GBOX device controllers
    print("🔧 GBOX Device Controller Test")
    print("=" * 40)
    
    # Test without API key (should fail gracefully)
    try:
        controller = GBOXDeviceController("test_device")
    except ValueError as e:
        print(f"✅ Expected error (no API key): {e}")
    
    print("\n📋 GBOX Device Controllers ready for integration!")
    print("💡 Set GBOX_API_KEY environment variable to enable real device control")
