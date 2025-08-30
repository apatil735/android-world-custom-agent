# 🤖 Custom Agent Framework for AndroidWorld Benchmark

This project implements **Challenge 2: Build a Custom Agent to Run the Benchmark** from the AndroidWorld project. Our custom agent can execute AndroidWorld tasks using either a mock device controller (for testing) or a real GBOX device controller (for actual device control).

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   CustomAgent   │───▶│ DeviceController │───▶│  GBOX/Android  │
│                 │    │                  │    │    Device      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌──────────────────┐
│ TaskExecutor    │    │ MockDeviceCtrl   │
│                 │    │ GBOXDeviceCtrl   │
└─────────────────┘    └──────────────────┘
         │
         ▼
┌─────────────────┐
│ AndroidWorld    │
│ Integration     │
└─────────────────┘
```

## 📁 Project Structure

```
android_world/
├── custom_agent.py              # Core custom agent framework
├── gbox_device_controller.py    # GBOX-based device controller
├── device_registration.py       # Device registration utilities
├── android_world_integration.py # AndroidWorld integration layer
├── test_complete_integration.py # Comprehensive test suite
└── CUSTOM_AGENT_README.md       # This file
```

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8+
- Android SDK with ADB
- Android emulator running with `-grpc 8554` flag
- GBOX API key (optional, for real device control)

### 2. Install Dependencies

```bash
# Install GBOX SDK (for real device control)
pip install gbox-sdk

# Install AndroidWorld dependencies
pip install -r requirements.txt
```

### 3. Set Environment Variables

```bash
# Windows PowerShell
$env:GBOX_API_KEY="your_gbox_api_key_here"

# Windows Command Prompt
set GBOX_API_KEY=your_gbox_api_key_here

# Linux/Mac
export GBOX_API_KEY="your_gbox_api_key_here"
```

### 4. Test the Framework

```bash
# Test custom agent (no GBOX required)
python custom_agent.py

# Test device registration (requires GBOX API key)
python device_registration.py

# Test complete integration
python test_complete_integration.py
```

## 🔧 Components

### 1. CustomAgent (`custom_agent.py`)

The main agent class that orchestrates task execution:

```python
from custom_agent import CustomAgent

# Create agent with default mock controller
agent = CustomAgent()

# Run a task
result = agent.run_task("RecipeAddMultipleRecipes", {
    "recipe_name": "Test Recipe",
    "ingredients": ["ingredient1", "ingredient2"],
    "instructions": "Test instructions"
})

print(f"Task success: {result['success']}")
```

### 2. Device Controllers

#### MockDeviceController (Default)
- Simulates device interactions for testing
- No external dependencies
- Perfect for development and testing

#### GBOXDeviceController
- Real Android device control via GBOX
- Requires GBOX API key
- Supports both cloud and local devices

```python
from gbox_device_controller import GBOXDeviceController

# Cloud device controller
controller = GBOXDeviceController(api_key="your_key")

# Local device controller (for emulator)
controller = GBOXLocalDeviceController("device_id", "your_key")

# Use with custom agent
agent = CustomAgent(device_controller=controller)
```

### 3. Device Registration (`device_registration.py`)

Manages device discovery and registration with GBOX:

```python
from device_registration import GBOXDeviceManager

device_manager = GBOXDeviceManager(adb_path, gbox_api_key)

# Register emulator with GBOX
gbox_device_id = device_manager.setup_emulator_for_gbox("emulator-5554")

# Get device information
devices = device_manager.get_available_devices()
```

### 4. AndroidWorld Integration (`android_world_integration.py`)

Bridges the custom agent with AndroidWorld benchmark:

```python
from android_world_integration import AndroidWorldIntegration

integration = AndroidWorldIntegration(adb_path, gbox_api_key)

# Set up GBOX device
integration.setup_gbox_device()

# Initialize AndroidWorld
integration.initialize_androidworld()

# Run benchmark tasks
result = integration.run_benchmark_task("RecipeAddMultipleRecipes")
```

## 🎯 Running AndroidWorld Tasks

### Basic Task Execution

```python
# Initialize integration
integration = AndroidWorldIntegration(adb_path, gbox_api_key)
integration.setup_gbox_device()
integration.initialize_androidworld()

# Get available tasks
tasks = integration.get_available_tasks()
print(f"Available tasks: {tasks}")

# Run a specific task
result = integration.run_benchmark_task("RecipeAddMultipleRecipes")
print(f"Task result: {result}")

# Run multiple tasks
multi_result = integration.run_multiple_tasks(tasks[:5])
print(f"Success rate: {multi_result['success_rate']:.2%}")
```

### Task Types Supported

Our custom agent supports various AndroidWorld task types:

- **Recipe Management**: `RecipeAddMultipleRecipes`
- **Calendar Operations**: `SimpleCalendarAddOneEvent`
- **Generic Tasks**: Any task from AndroidWorld registry

## 🔍 Testing and Debugging

### 1. Test Individual Components

```bash
# Test custom agent framework
python custom_agent.py

# Test GBOX device controller
python gbox_device_controller.py

# Test device registration
python device_registration.py
```

### 2. Run Complete Test Suite

```bash
python test_complete_integration.py
```

This will test:
- ✅ Custom agent functionality
- ✅ Device registration with GBOX
- ✅ GBOX device controller operations
- ✅ Complete AndroidWorld integration

### 3. Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🚨 Troubleshooting

### Common Issues

#### 1. GBOX API Key Not Set
```
❌ GBOX_API_KEY environment variable not set
```
**Solution**: Set the environment variable with your GBOX API key.

#### 2. Emulator Not Connected
```
❌ No devices found. Make sure emulator is running.
```
**Solution**: 
- Ensure emulator is running with `-grpc 8554` flag
- Check ADB connection: `adb devices`

#### 3. GBOX SDK Not Installed
```
❌ GBOX SDK not installed. Install with: pip install gbox-sdk
```
**Solution**: Install the GBOX SDK: `pip install gbox-sdk`

#### 4. AndroidWorld Import Errors
```
❌ Failed to initialize AndroidWorld
```
**Solution**: 
- Check Python path includes android_world package
- Ensure all dependencies are installed

### Getting Help

1. **Check logs**: All components provide detailed logging
2. **Verify prerequisites**: Ensure emulator, ADB, and dependencies are set up
3. **Test components individually**: Use the test scripts to isolate issues
4. **Check GBOX documentation**: [GBOX Android Documentation](https://docs.gbox.ai/android/real-device)

## 🎉 Success Criteria

Your custom agent is working correctly when:

1. ✅ **Custom Agent**: Can execute tasks with mock device controller
2. ✅ **Device Registration**: Emulator is registered with GBOX
3. ✅ **GBOX Controller**: Can perform real device operations
4. ✅ **AndroidWorld Integration**: Can run benchmark tasks successfully
5. ✅ **Task Execution**: Tasks complete with measurable success rates

## 🔮 Future Enhancements

- **AI-Powered Task Execution**: Integrate with LLMs for intelligent task planning
- **Multi-Device Support**: Control multiple devices simultaneously
- **Performance Metrics**: Track and optimize task execution times
- **Task Templates**: Pre-defined task execution patterns
- **Cloud Integration**: Deploy agent to cloud for remote device control

## 📚 References

- [AndroidWorld Project](https://github.com/google-research/android_world)
- [GBOX Documentation](https://docs.gbox.ai/android/real-device)
- [Android Debug Bridge (ADB)](https://developer.android.com/studio/command-line/adb)
- [Protocol Buffers](https://developers.google.com/protocol-buffers)

## 🤝 Contributing

This framework is designed to be extensible. Key areas for contribution:

- **New Device Controllers**: Support for other device control solutions
- **Task Executors**: Specialized execution logic for specific task types
- **Performance Optimization**: Faster task execution and better resource management
- **Testing**: Additional test cases and edge case handling

---

**🎯 Challenge 2 Complete!** You now have a fully functional custom agent that can run AndroidWorld benchmark tasks with real device control via GBOX.
