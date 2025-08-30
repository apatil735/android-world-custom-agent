#!/usr/bin/env python3
"""
AndroidWorld Integration Layer for Custom Agent
This module integrates our custom agent with the AndroidWorld benchmark framework.
"""

import os
import sys
import logging
from typing import Dict, Any, Optional

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from custom_agent import CustomAgent
from gbox_device_controller import GBOXDeviceController, GBOXLocalDeviceController
from device_registration import GBOXDeviceManager

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AndroidWorldIntegration:
    """Integration layer between Custom Agent and AndroidWorld."""
    
    def __init__(self, adb_path: str, gbox_api_key: str, device_id: str = "emulator-5554"):
        self.adb_path = adb_path
        self.gbox_api_key = gbox_api_key
        self.device_id = device_id
        self.custom_agent = None
        self.task_registry = None
        self.env = None
        self.device_manager = GBOXDeviceManager(adb_path, gbox_api_key)
        
        logger.info(f"AndroidWorld Integration initialized for device: {device_id}")
    
    def setup_gbox_device(self) -> bool:
        """Set up GBOX device controller for the emulator."""
        try:
            logger.info("Setting up GBOX device controller...")
            
            # First, register the emulator with GBOX
            gbox_device_id = self.device_manager.setup_emulator_for_gbox(self.device_id)
            
            if not gbox_device_id:
                logger.error("Failed to register emulator with GBOX")
                return False
            
            # Create GBOX device controller
            if self.device_id.startswith('emulator-'):
                # Use local device controller for emulator
                self.custom_agent = CustomAgent(
                    device_controller=GBOXLocalDeviceController(gbox_device_id, self.gbox_api_key)
                )
                logger.info(f"Created GBOX local device controller for emulator: {gbox_device_id}")
            else:
                # Use cloud device controller for physical devices
                self.custom_agent = CustomAgent(
                    device_controller=GBOXDeviceController(self.gbox_api_key)
                )
                logger.info("Created GBOX cloud device controller")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to setup GBOX device: {e}")
            return False
    
    def initialize_androidworld(self):
        """Initialize the AndroidWorld environment."""
        try:
            # Import AndroidWorld components
            from android_world import registry
            from android_world.env import env_launcher
            
            logger.info("AndroidWorld components imported successfully")
            
            # Get task registry
            self.task_registry = registry.TaskRegistry()
            aw_registry = self.task_registry.get_registry(
                self.task_registry.ANDROID_WORLD_FAMILY
            )
            
            logger.info(f"Available tasks: {list(aw_registry.keys())}")
            
            # Initialize environment
            self.env = env_launcher.load_and_setup_env(
                console_port=5554,
                emulator_setup=False,
                adb_path=self.adb_path
            )
            
            logger.info("AndroidWorld environment initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize AndroidWorld: {e}")
            return False
    
    def run_benchmark_task(self, task_name: str) -> Dict[str, Any]:
        """Run a specific benchmark task using our custom agent."""
        if not self.task_registry:
            return {"success": False, "error": "AndroidWorld not initialized"}
        
        if not self.custom_agent:
            return {"success": False, "error": "GBOX device not set up"}
        
        try:
            # Get task from registry
            aw_registry = self.task_registry.get_registry(
                self.task_registry.ANDROID_WORLD_FAMILY
            )
            
            if task_name not in aw_registry:
                return {"success": False, "error": f"Task {task_name} not found"}
            
            task_type = aw_registry[task_name]
            logger.info(f"Running benchmark task: {task_name}")
            
            # Generate random parameters for the task
            params = task_type.generate_random_params()
            task = task_type(params)
            
            # Initialize the task
            task.initialize_task(self.env)
            
            # Execute using our custom agent with GBOX device controller
            result = self.custom_agent.run_task(task_name, {
                "goal": str(task.goal),
                "complexity": task.complexity,
                "params": params
            })
            
            # Check if task was successful
            if self.env:
                task_success = task.is_successful(self.env) == 1
                result["task_success"] = task_success
                result["goal"] = str(task.goal)
            
            return result
            
        except Exception as e:
            logger.error(f"Task execution failed: {e}")
            return {"success": False, "error": str(e)}
    
    def get_available_tasks(self) -> list:
        """Get list of available benchmark tasks."""
        if not self.task_registry:
            return []
        
        try:
            aw_registry = self.task_registry.get_registry(
                self.task_registry.ANDROID_WORLD_FAMILY
            )
            return list(aw_registry.keys())
        except Exception as e:
            logger.error(f"Failed to get available tasks: {e}")
            return []
    
    def run_multiple_tasks(self, task_names: list, max_tasks: int = 5) -> Dict[str, Any]:
        """Run multiple benchmark tasks."""
        results = []
        successful_tasks = 0
        
        for i, task_name in enumerate(task_names[:max_tasks]):
            logger.info(f"Running task {i+1}/{len(task_names[:max_tasks])}: {task_name}")
            
            result = self.run_benchmark_task(task_name)
            results.append(result)
            
            if result.get("success", False):
                successful_tasks += 1
            
            # Small delay between tasks
            import time
            time.sleep(1)
        
        return {
            "total_tasks": len(results),
            "successful_tasks": successful_tasks,
            "success_rate": successful_tasks / len(results) if results else 0,
            "results": results
        }
    
    def get_device_status(self) -> Dict[str, Any]:
        """Get current device status and information."""
        try:
            available_devices = self.device_manager.get_available_devices()
            emulator_device = None
            
            for device in available_devices:
                if device['id'] == self.device_id:
                    emulator_device = device
                    break
            
            if emulator_device:
                return {
                    "device_id": self.device_id,
                    "connected": True,
                    "type": emulator_device.get('type', 'unknown'),
                    "model": emulator_device.get('properties', {}).get('ro.product.model', 'unknown'),
                    "android_version": emulator_device.get('properties', {}).get('ro.build.version.release', 'unknown'),
                    "registration": emulator_device.get('registration', {}),
                    "screen_size": emulator_device.get('screen_size', 'unknown')
                }
            else:
                return {
                    "device_id": self.device_id,
                    "connected": False,
                    "error": "Device not found"
                }
                
        except Exception as e:
            logger.error(f"Failed to get device status: {e}")
            return {"error": str(e)}
    
    def cleanup(self):
        """Clean up resources."""
        if self.custom_agent and hasattr(self.custom_agent.device_controller, 'close_box'):
            try:
                self.custom_agent.device_controller.close_box()
                logger.info("GBOX device controller closed")
            except Exception as e:
                logger.error(f"Error closing GBOX device controller: {e}")
        
        if self.env:
            try:
                self.env.close()
                logger.info("AndroidWorld environment closed")
            except Exception as e:
                logger.error(f"Error closing environment: {e}")


def main():
    """Main function to demonstrate the integration."""
    print("🔗 AndroidWorld Integration with GBOX Custom Agent")
    print("=" * 60)
    
    # Check if GBOX API key is set
    gbox_api_key = os.getenv("GBOX_API_KEY")
    if not gbox_api_key:
        print("❌ GBOX_API_KEY environment variable not set")
        print("Please set it with: set GBOX_API_KEY=your_api_key_here")
        return
    
    print("✅ GBOX API key found")
    
    # Initialize integration
    adb_path = r"C:\Users\aney4\AppData\Local\Android\Sdk\platform-tools\adb.exe"
    integration = AndroidWorldIntegration(adb_path, gbox_api_key)
    
    try:
        # Set up GBOX device controller
        print("\n🔧 Setting up GBOX device controller...")
        if integration.setup_gbox_device():
            print("✅ GBOX device controller set up successfully!")
            
            # Get device status
            device_status = integration.get_device_status()
            print(f"\n📱 Device Status:")
            print(f"   ID: {device_status.get('device_id', 'unknown')}")
            print(f"   Type: {device_status.get('type', 'unknown')}")
            print(f"   Model: {device_status.get('model', 'unknown')}")
            print(f"   Android: {device_status.get('android_version', 'unknown')}")
            print(f"   Registration: {device_status.get('registration', {}).get('status', 'unknown')}")
            
            # Initialize AndroidWorld
            print("\n🚀 Initializing AndroidWorld...")
            if integration.initialize_androidworld():
                print("✅ AndroidWorld initialized successfully!")
                
                # Get available tasks
                available_tasks = integration.get_available_tasks()
                print(f"\n📋 Available tasks: {len(available_tasks)}")
                
                if available_tasks:
                    # Show first few tasks
                    sample_tasks = available_tasks[:5]
                    for i, task in enumerate(sample_tasks, 1):
                        print(f"  {i}. {task}")
                    
                    # Run a sample task
                    if "RecipeAddMultipleRecipes" in available_tasks:
                        print(f"\n🎯 Running sample task: RecipeAddMultipleRecipes")
                        result = integration.run_benchmark_task("RecipeAddMultipleRecipes")
                        print(f"✅ Task result: {result}")
                    
                    # Run multiple tasks
                    print(f"\n🔄 Running multiple tasks...")
                    multi_result = integration.run_multiple_tasks(available_tasks[:3])
                    print(f"📊 Multi-task results: {multi_result['successful_tasks']}/{multi_result['total_tasks']} successful")
                
            else:
                print("❌ Failed to initialize AndroidWorld")
        else:
            print("❌ Failed to setup GBOX device controller")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        
    finally:
        # Cleanup
        integration.cleanup()
        print("\n🧹 Cleanup completed")


if __name__ == "__main__":
    main()
