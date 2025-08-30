#!/usr/bin/env python3
"""
Complete Integration Test for Custom Agent + GBOX + AndroidWorld
This script tests the full pipeline from device registration to task execution.
"""

import os
import sys
import time
import logging
from typing import Dict, Any

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_device_registration():
    """Test device registration with GBOX."""
    print("\n🔧 Testing Device Registration...")
    print("=" * 40)
    
    try:
        from device_registration import GBOXDeviceManager
        
        # Check if GBOX API key is set
        gbox_api_key = os.getenv("GBOX_API_KEY")
        if not gbox_api_key:
            print("❌ GBOX_API_KEY not set. Skipping device registration test.")
            return False
        
        adb_path = r"C:\Users\aney4\AppData\Local\Android\Sdk\platform-tools\adb.exe"
        device_manager = GBOXDeviceManager(adb_path, gbox_api_key)
        
        # Get available devices
        available_devices = device_manager.get_available_devices()
        print(f"📱 Found {len(available_devices)} device(s)")
        
        if not available_devices:
            print("❌ No devices found. Make sure emulator is running.")
            return False
        
        # Show device information
        for device in available_devices:
            print(f"\n  Device: {device['id']}")
            print(f"    Type: {device.get('type', 'unknown')}")
            print(f"    Model: {device.get('properties', {}).get('ro.product.model', 'unknown')}")
            print(f"    Android: {device.get('properties', {}).get('ro.build.version.release', 'unknown')}")
        
        # Try to register emulator
        emulator_id = "emulator-5554"
        gbox_device_id = device_manager.setup_emulator_for_gbox(emulator_id)
        
        if gbox_device_id:
            print(f"✅ Emulator registered with GBOX: {gbox_device_id}")
            return gbox_device_id
        else:
            print("❌ Failed to register emulator")
            return False
            
    except Exception as e:
        logger.error(f"Device registration test failed: {e}")
        return False


def test_gbox_device_controller(gbox_device_id: str):
    """Test GBOX device controller functionality."""
    print(f"\n🎮 Testing GBOX Device Controller...")
    print("=" * 45)
    
    try:
        from gbox_device_controller import GBOXLocalDeviceController
        
        gbox_api_key = os.getenv("GBOX_API_KEY")
        if not gbox_api_key:
            print("❌ GBOX_API_KEY not set. Skipping device controller test.")
            return False
        
        # Create device controller
        controller = GBOXLocalDeviceController(gbox_device_id, gbox_api_key)
        print(f"✅ GBOX device controller created for: {gbox_device_id}")
        
        # Test basic operations
        print("\n📱 Testing device operations...")
        
        # Get screen info
        screen_info = controller.get_screen_info()
        print(f"📺 Screen info: {screen_info}")
        
        # Test click (this will actually click on the device)
        print("🖱️ Testing click operation...")
        success = controller.click(500, 1200)
        print(f"Click result: {success}")
        
        # Test text input
        print("⌨️ Testing text input...")
        success = controller.type_text("Test Input")
        print(f"Text input result: {success}")
        
        # Clean up
        controller.close_box()
        print("🧹 Device controller closed")
        
        return True
        
    except Exception as e:
        logger.error(f"GBOX device controller test failed: {e}")
        return False


def test_custom_agent():
    """Test custom agent with mock device controller."""
    print(f"\n🤖 Testing Custom Agent...")
    print("=" * 35)
    
    try:
        from custom_agent import CustomAgent
        
        # Create custom agent with mock controller
        agent = CustomAgent()
        print("✅ Custom agent created")
        
        # Test task execution
        print("\n📋 Testing task execution...")
        
        # Test recipe task
        recipe_result = agent.run_task("RecipeAddMultipleRecipes", {
            "recipe_name": "Test Recipe",
            "ingredients": ["ingredient1", "ingredient2"],
            "instructions": "Test instructions"
        })
        print(f"✅ Recipe task result: {recipe_result['success']}")
        
        # Test calendar task
        calendar_result = agent.run_task("SimpleCalendarAddOneEvent", {
            "event_title": "Test Event",
            "event_date": "2025-08-30"
        })
        print(f"✅ Calendar task result: {calendar_result['success']}")
        
        # Get agent status
        status = agent.get_status()
        print(f"🤖 Agent status: {status['status']}")
        print(f"📊 Tasks executed: {status['tasks_executed']}")
        
        return True
        
    except Exception as e:
        logger.error(f"Custom agent test failed: {e}")
        return False


def test_androidworld_integration(gbox_device_id: str):
    """Test complete AndroidWorld integration."""
    print(f"\n🔗 Testing AndroidWorld Integration...")
    print("=" * 45)
    
    try:
        from android_world_integration import AndroidWorldIntegration
        
        gbox_api_key = os.getenv("GBOX_API_KEY")
        if not gbox_api_key:
            print("❌ GBOX_API_KEY not set. Skipping AndroidWorld integration test.")
            return False
        
        adb_path = r"C:\Users\aney4\AppData\Local\Android\Sdk\platform-tools\adb.exe"
        integration = AndroidWorldIntegration(adb_path, gbox_api_key)
        
        # Set up GBOX device
        print("🔧 Setting up GBOX device...")
        if not integration.setup_gbox_device():
            print("❌ Failed to setup GBOX device")
            return False
        
        print("✅ GBOX device setup complete")
        
        # Get device status
        device_status = integration.get_device_status()
        print(f"📱 Device status: {device_status.get('registration', {}).get('status', 'unknown')}")
        
        # Initialize AndroidWorld
        print("\n🚀 Initializing AndroidWorld...")
        if not integration.initialize_androidworld():
            print("❌ Failed to initialize AndroidWorld")
            return False
        
        print("✅ AndroidWorld initialized")
        
        # Get available tasks
        available_tasks = integration.get_available_tasks()
        print(f"📋 Available tasks: {len(available_tasks)}")
        
        if available_tasks:
            # Show sample tasks
            sample_tasks = available_tasks[:3]
            for i, task in enumerate(sample_tasks, 1):
                print(f"  {i}. {task}")
            
            # Test a specific task if available
            if "RecipeAddMultipleRecipes" in available_tasks:
                print(f"\n🎯 Testing RecipeAddMultipleRecipes task...")
                result = integration.run_benchmark_task("RecipeAddMultipleRecipes")
                print(f"✅ Task result: {result}")
        
        # Clean up
        integration.cleanup()
        print("🧹 Integration cleanup complete")
        
        return True
        
    except Exception as e:
        logger.error(f"AndroidWorld integration test failed: {e}")
        return False


def main():
    """Main test function."""
    print("🧪 Complete Integration Test Suite")
    print("=" * 50)
    print("Testing: Custom Agent + GBOX + AndroidWorld Integration")
    
    # Check prerequisites
    gbox_api_key = os.getenv("GBOX_API_KEY")
    if not gbox_api_key:
        print("\n⚠️  GBOX_API_KEY not set!")
        print("To set it, run: set GBOX_API_KEY=your_api_key_here")
        print("You can get an API key from: https://gbox.ai")
        print("\nContinuing with tests that don't require GBOX...")
    
    test_results = {}
    
    # Test 1: Custom Agent (no GBOX required)
    print("\n" + "="*60)
    test_results['custom_agent'] = test_custom_agent()
    
    # Test 2: Device Registration (requires GBOX API key)
    if gbox_api_key:
        test_results['device_registration'] = test_device_registration()
        
        if test_results['device_registration']:
            gbox_device_id = test_results['device_registration']
            
            # Test 3: GBOX Device Controller
            test_results['gbox_controller'] = test_gbox_device_controller(gbox_device_id)
            
            # Test 4: Complete Integration
            test_results['androidworld_integration'] = test_androidworld_integration(gbox_device_id)
        else:
            test_results['gbox_controller'] = False
            test_results['androidworld_integration'] = False
    else:
        test_results['device_registration'] = False
        test_results['gbox_controller'] = False
        test_results['androidworld_integration'] = False
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST RESULTS SUMMARY")
    print("="*60)
    
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:.<30} {status}")
    
    # Recommendations
    print("\n💡 RECOMMENDATIONS:")
    
    if not gbox_api_key:
        print("• Set GBOX_API_KEY environment variable to enable full testing")
        print("• Get API key from: https://gbox.ai")
    
    if test_results.get('custom_agent', False):
        print("• Custom agent framework is working correctly")
    
    if test_results.get('device_registration', False):
        print("• Device registration with GBOX is working")
    
    if test_results.get('gbox_controller', False):
        print("• GBOX device controller is functional")
    
    if test_results.get('androidworld_integration', False):
        print("• Complete integration is working!")
        print("• You can now run AndroidWorld tasks with your custom agent!")
    
    print("\n🎯 Integration test suite completed!")


if __name__ == "__main__":
    main()
