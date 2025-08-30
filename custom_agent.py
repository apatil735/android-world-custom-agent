#!/usr/bin/env python3
"""
Custom Agent for AndroidWorld Benchmark
This agent will be able to execute tasks using the AndroidWorld framework.
"""

import time
import logging
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DeviceController(ABC):
    """Abstract base class for device control operations."""
    
    @abstractmethod
    def click(self, x: int, y: int) -> bool:
        """Click at specific coordinates."""
        pass
    
    @abstractmethod
    def swipe(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: int = 500) -> bool:
        """Swipe from start to end coordinates."""
        pass
    
    @abstractmethod
    def type_text(self, text: str) -> bool:
        """Type text on the device."""
        pass
    
    @abstractmethod
    def press_key(self, key: str) -> bool:
        """Press a specific key."""
        pass
    
    @abstractmethod
    def get_screen_info(self) -> Dict[str, Any]:
        """Get current screen information."""
        pass


class MockDeviceController(DeviceController):
    """Mock device controller for testing without actual device connection."""
    
    def click(self, x: int, y: int) -> bool:
        logger.info(f"Mock: Clicking at coordinates ({x}, {y})")
        return True
    
    def swipe(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: int = 500) -> bool:
        logger.info(f"Mock: Swiping from ({start_x}, {start_y}) to ({end_x}, {end_y}) over {duration}ms")
        return True
    
    def type_text(self, text: str) -> bool:
        logger.info(f"Mock: Typing text: '{text}'")
        return True
    
    def press_key(self, key: str) -> bool:
        logger.info(f"Mock: Pressing key: {key}")
        return True
    
    def get_screen_info(self) -> Dict[str, Any]:
        return {
            "width": 1080,
            "height": 2400,
            "orientation": "portrait",
            "timestamp": time.time()
        }


class TaskExecutor:
    """Handles task execution logic."""
    
    def __init__(self, device_controller: DeviceController):
        self.device_controller = device_controller
        self.task_history = []
    
    def execute_task(self, task_name: str, task_params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific task with given parameters."""
        logger.info(f"Executing task: {task_name}")
        
        start_time = time.time()
        success = False
        error_message = None
        
        try:
            if task_name == "RecipeAddMultipleRecipes":
                success = self._execute_recipe_task(task_params)
            elif task_name == "SimpleCalendarAddOneEvent":
                success = self._execute_calendar_task(task_params)
            else:
                success = self._execute_generic_task(task_name, task_params)
                
        except Exception as e:
            error_message = str(e)
            logger.error(f"Task execution failed: {error_message}")
        
        execution_time = time.time() - start_time
        
        result = {
            "task_name": task_name,
            "success": success,
            "execution_time": execution_time,
            "error_message": error_message,
            "timestamp": start_time
        }
        
        self.task_history.append(result)
        return result
    
    def _execute_recipe_task(self, params: Dict[str, Any]) -> bool:
        """Execute recipe-related tasks."""
        logger.info("Executing recipe task...")
        
        # Mock recipe task execution
        # In real implementation, this would use the device controller
        self.device_controller.click(500, 1200)  # Click on add recipe button
        time.sleep(1)
        self.device_controller.type_text("Test Recipe")
        time.sleep(1)
        self.device_controller.click(500, 1400)  # Click save button
        
        return True
    
    def _execute_calendar_task(self, params: Dict[str, Any]) -> bool:
        """Execute calendar-related tasks."""
        logger.info("Executing calendar task...")
        
        # Mock calendar task execution
        self.device_controller.click(500, 1200)  # Click on add event button
        time.sleep(1)
        self.device_controller.type_text("Test Event")
        time.sleep(1)
        self.device_controller.click(500, 1400)  # Click save button
        
        return True
    
    def _execute_generic_task(self, task_name: str, params: Dict[str, Any]) -> bool:
        """Execute generic tasks."""
        logger.info(f"Executing generic task: {task_name}")
        
        # Generic task execution logic
        # This would be customized based on the specific task
        return True


class CustomAgent:
    """Main custom agent class that integrates with AndroidWorld."""
    
    def __init__(self, device_controller: Optional[DeviceController] = None):
        self.device_controller = device_controller or MockDeviceController()
        self.task_executor = TaskExecutor(self.device_controller)
        self.agent_id = f"custom_agent_{int(time.time())}"
        
        logger.info(f"Custom Agent initialized with ID: {self.agent_id}")
    
    def run_task(self, task_name: str, task_params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Run a specific task."""
        if task_params is None:
            task_params = {}
        
        logger.info(f"Agent {self.agent_id} starting task: {task_name}")
        
        # Execute the task
        result = self.task_executor.execute_task(task_name, task_params)
        
        # Log the result
        if result["success"]:
            logger.info(f"Task {task_name} completed successfully in {result['execution_time']:.2f}s")
        else:
            logger.error(f"Task {task_name} failed: {result['error_message']}")
        
        return result
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status."""
        return {
            "agent_id": self.agent_id,
            "status": "active",
            "tasks_executed": len(self.task_executor.task_history),
            "device_connected": True,
            "timestamp": time.time()
        }
    
    def get_task_history(self) -> list:
        """Get history of executed tasks."""
        return self.task_executor.task_history


def main():
    """Main function to demonstrate the custom agent."""
    print("🤖 Custom Agent for AndroidWorld Benchmark")
    print("=" * 50)
    
    # Initialize the custom agent
    agent = CustomAgent()
    
    # Example task execution
    print("\n📱 Executing sample tasks...")
    
    # Test recipe task
    recipe_result = agent.run_task("RecipeAddMultipleRecipes", {
        "recipe_name": "Test Recipe",
        "ingredients": ["ingredient1", "ingredient2"],
        "instructions": "Test instructions"
    })
    
    # Test calendar task
    calendar_result = agent.run_task("SimpleCalendarAddOneEvent", {
        "event_title": "Test Event",
        "event_date": "2025-08-30"
    })
    
    # Show results
    print(f"\n✅ Recipe Task Result: {recipe_result['success']}")
    print(f"✅ Calendar Task Result: {calendar_result['success']}")
    
    # Show agent status
    status = agent.get_status()
    print(f"\n🤖 Agent Status: {status['status']}")
    print(f"📊 Tasks Executed: {status['tasks_executed']}")
    
    print("\n🎯 Custom Agent is ready for AndroidWorld integration!")


if __name__ == "__main__":
    main()
