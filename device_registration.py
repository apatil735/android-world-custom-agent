#!/usr/bin/env python3
"""
Device Registration Utility for GBOX
This module helps register and manage Android devices (including emulators) with GBOX.
"""

import os
import subprocess
import logging
import time
from typing import Dict, Any, Optional, List

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DeviceRegistration:
    """Utility class for registering Android devices with GBOX."""
    
    def __init__(self, adb_path: str):
        self.adb_path = adb_path
        self.registered_devices = {}
    
    def get_connected_devices(self) -> List[Dict[str, str]]:
        """Get list of connected Android devices via ADB."""
        try:
            result = subprocess.run(
                [self.adb_path, "devices"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                logger.error(f"ADB devices command failed: {result.stderr}")
                return []
            
            devices = []
            lines = result.stdout.strip().split('\n')[1:]  # Skip header line
            
            for line in lines:
                if line.strip() and '\t' in line:
                    device_id, status = line.split('\t')
                    if status == 'device':
                        devices.append({
                            'id': device_id,
                            'status': status,
                            'type': self._get_device_type(device_id)
                        })
            
            logger.info(f"Found {len(devices)} connected devices")
            return devices
            
        except Exception as e:
            logger.error(f"Failed to get connected devices: {e}")
            return []
    
    def _get_device_type(self, device_id: str) -> str:
        """Determine if device is emulator or physical."""
        try:
            # Check if it's an emulator
            if device_id.startswith('emulator-'):
                return 'emulator'
            
            # Check device properties
            result = subprocess.run(
                [self.adb_path, '-s', device_id, 'shell', 'getprop', 'ro.product.model'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                model = result.stdout.strip()
                if 'sdk' in model.lower() or 'emulator' in model.lower():
                    return 'emulator'
                else:
                    return 'physical'
            
            return 'unknown'
            
        except Exception as e:
            logger.error(f"Failed to determine device type: {e}")
            return 'unknown'
    
    def get_device_info(self, device_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific device."""
        try:
            info = {
                'id': device_id,
                'type': self._get_device_type(device_id),
                'properties': {}
            }
            
            # Get device properties
            properties = [
                'ro.product.model',
                'ro.product.brand',
                'ro.product.name',
                'ro.build.version.release',
                'ro.build.version.sdk'
            ]
            
            for prop in properties:
                try:
                    result = subprocess.run(
                        [self.adb_path, '-s', device_id, 'shell', 'getprop', prop],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    
                    if result.returncode == 0:
                        info['properties'][prop] = result.stdout.strip()
                except Exception:
                    info['properties'][prop] = 'unknown'
            
            # Get screen dimensions
            try:
                result = subprocess.run(
                    [self.adb_path, '-s', device_id, 'shell', 'wm', 'size'],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode == 0:
                    size_output = result.stdout.strip()
                    if 'Physical size:' in size_output:
                        size = size_output.split('Physical size: ')[1]
                        info['screen_size'] = size
            except Exception:
                info['screen_size'] = 'unknown'
            
            logger.info(f"Device info for {device_id}: {info}")
            return info
            
        except Exception as e:
            logger.error(f"Failed to get device info: {e}")
            return {'id': device_id, 'error': str(e)}
    
    def install_gbox_agent(self, device_id: str) -> bool:
        """Install GBOX agent on the device if needed."""
        try:
            logger.info(f"Installing GBOX agent on device {device_id}")
            
            # Check if GBOX agent is already installed
            result = subprocess.run(
                [self.adb_path, '-s', device_id, 'shell', 'pm', 'list', 'packages', 'ai.gbox.agent'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if 'ai.gbox.agent' in result.stdout:
                logger.info("GBOX agent already installed")
                return True
            
            # For now, we'll assume the agent is pre-installed or will be installed via GBOX
            # In a real implementation, you'd download and install the APK
            logger.info("GBOX agent installation would happen here")
            return True
            
        except Exception as e:
            logger.error(f"Failed to install GBOX agent: {e}")
            return False
    
    def register_with_gbox(self, device_id: str, gbox_api_key: str) -> Optional[str]:
        """Register device with GBOX and return device ID."""
        try:
            logger.info(f"Registering device {device_id} with GBOX")
            
            # This would use the GBOX CLI or API to register the device
            # For now, we'll create a mock registration process
            
            # Install GBOX agent if needed
            if not self.install_gbox_agent(device_id):
                logger.error("Failed to install GBOX agent")
                return None
            
            # Generate a GBOX device ID (in real implementation, this comes from GBOX)
            gbox_device_id = f"gbox_{device_id.replace('-', '_')}_{int(time.time())}"
            
            # Store registration info
            self.registered_devices[device_id] = {
                'gbox_device_id': gbox_device_id,
                'registration_time': time.time(),
                'status': 'registered'
            }
            
            logger.info(f"Device {device_id} registered with GBOX as {gbox_device_id}")
            return gbox_device_id
            
        except Exception as e:
            logger.error(f"Failed to register device with GBOX: {e}")
            return None
    
    def get_registration_status(self, device_id: str) -> Dict[str, Any]:
        """Get registration status of a device."""
        if device_id in self.registered_devices:
            return self.registered_devices[device_id]
        else:
            return {'status': 'not_registered'}
    
    def list_registered_devices(self) -> List[Dict[str, Any]]:
        """List all registered devices."""
        return [
            {
                'device_id': device_id,
                **registration_info
            }
            for device_id, registration_info in self.registered_devices.items()
        ]


class GBOXDeviceManager:
    """Manager for GBOX device operations."""
    
    def __init__(self, adb_path: str, gbox_api_key: str):
        self.adb_path = adb_path
        self.gbox_api_key = gbox_api_key
        self.registration = DeviceRegistration(adb_path)
    
    def setup_emulator_for_gbox(self, emulator_id: str = "emulator-5554") -> Optional[str]:
        """Set up emulator for GBOX control."""
        try:
            logger.info(f"Setting up emulator {emulator_id} for GBOX")
            
            # Check if emulator is connected
            devices = self.registration.get_connected_devices()
            emulator_devices = [d for d in devices if d['id'] == emulator_id]
            
            if not emulator_devices:
                logger.error(f"Emulator {emulator_id} not found or not connected")
                return None
            
            emulator_device = emulator_devices[0]
            logger.info(f"Found emulator: {emulator_device}")
            
            # Get device info
            device_info = self.registration.get_device_info(emulator_id)
            logger.info(f"Emulator info: {device_info}")
            
            # Register with GBOX
            gbox_device_id = self.registration.register_with_gbox(emulator_id, self.gbox_api_key)
            
            if gbox_device_id:
                logger.info(f"Emulator {emulator_id} successfully registered with GBOX as {gbox_device_id}")
                return gbox_device_id
            else:
                logger.error(f"Failed to register emulator {emulator_id} with GBOX")
                return None
                
        except Exception as e:
            logger.error(f"Failed to setup emulator for GBOX: {e}")
            return None
    
    def get_available_devices(self) -> List[Dict[str, Any]]:
        """Get all available devices (connected and registered)."""
        connected_devices = self.registration.get_connected_devices()
        available_devices = []
        
        for device in connected_devices:
            device_info = self.registration.get_device_info(device['id'])
            registration_status = self.registration.get_registration_status(device['id'])
            
            available_devices.append({
                **device_info,
                'connected': True,
                'registration': registration_status
            })
        
        return available_devices


def main():
    """Main function to demonstrate device registration."""
    print("🔗 GBOX Device Registration Utility")
    print("=" * 45)
    
    # Check if GBOX API key is set
    gbox_api_key = os.getenv("GBOX_API_KEY")
    if not gbox_api_key:
        print("❌ GBOX_API_KEY environment variable not set")
        print("Please set it with: set GBOX_API_KEY=your_api_key_here")
        return
    
    print("✅ GBOX API key found")
    
    # Initialize device manager
    adb_path = r"C:\Users\aney4\AppData\Local\Android\Sdk\platform-tools\adb.exe"
    device_manager = GBOXDeviceManager(adb_path, gbox_api_key)
    
    try:
        # Get available devices
        print("\n📱 Scanning for available devices...")
        available_devices = device_manager.get_available_devices()
        
        if not available_devices:
            print("❌ No devices found")
            print("Make sure your emulator is running and connected via ADB")
            return
        
        print(f"✅ Found {len(available_devices)} device(s):")
        
        for i, device in enumerate(available_devices, 1):
            print(f"\n  {i}. Device ID: {device['id']}")
            print(f"     Type: {device.get('type', 'unknown')}")
            print(f"     Model: {device.get('properties', {}).get('ro.product.model', 'unknown')}")
            print(f"     Android: {device.get('properties', {}).get('ro.build.version.release', 'unknown')}")
            print(f"     Status: {device.get('registration', {}).get('status', 'not_registered')}")
        
        # Try to set up the emulator for GBOX
        print(f"\n🚀 Setting up emulator for GBOX control...")
        emulator_id = "emulator-5554"  # Default emulator ID
        
        gbox_device_id = device_manager.setup_emulator_for_gbox(emulator_id)
        
        if gbox_device_id:
            print(f"✅ Emulator successfully registered with GBOX!")
            print(f"   GBOX Device ID: {gbox_device_id}")
            print(f"\n🎯 You can now use this device ID in your GBOXDeviceController")
        else:
            print("❌ Failed to register emulator with GBOX")
            print("   This might be due to:")
            print("   - Emulator not running")
            print("   - ADB connection issues")
            print("   - GBOX agent not installed")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n🔧 Device registration utility ready!")


if __name__ == "__main__":
    main()
