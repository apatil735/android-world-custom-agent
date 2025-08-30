#!/usr/bin/env python3
"""
Challenge Verification Script
This script verifies that both Challenge 1 and Challenge 2 are working correctly.
"""

import sys
import os
import time

def print_header(title):
    """Print a formatted header."""
    print("\n" + "="*60)
    print(f"🎯 {title}")
    print("="*60)

def print_section(title):
    """Print a formatted section."""
    print(f"\n📋 {title}")
    print("-" * 40)

def verify_challenge_1():
    """Verify Challenge 1: Environment Setup."""
    print_header("CHALLENGE 1 VERIFICATION: Environment Setup")
    
    results = {}
    
    # Test 1: Python environment
    print_section("Python Environment")
    try:
        import sys
        python_version = sys.version
        print(f"✅ Python Version: {python_version}")
        results['python'] = True
    except Exception as e:
        print(f"❌ Python Environment: {e}")
        results['python'] = False
    
    # Test 2: Dependencies
    print_section("Dependencies")
    try:
        import absl
        print("✅ absl-py: Available")
        results['absl'] = True
    except ImportError:
        print("❌ absl-py: Not available")
        results['absl'] = False
    
    try:
        import google.protobuf
        print("✅ protobuf: Available")
        results['protobuf'] = True
    except ImportError:
        print("❌ protobuf: Not available")
        results['protobuf'] = False
    
    # Test 3: AndroidWorld imports
    print_section("AndroidWorld Framework")
    try:
        from android_world import registry
        print("✅ AndroidWorld registry: Imported successfully")
        results['registry'] = True
    except Exception as e:
        print(f"❌ AndroidWorld registry: {e}")
        results['registry'] = False
    
    try:
        from android_world.env import env_launcher
        print("✅ AndroidWorld env_launcher: Imported successfully")
        results['env_launcher'] = True
    except Exception as e:
        print(f"❌ AndroidWorld env_launcher: {e}")
        results['env_launcher'] = False
    
    # Test 4: Task registry
    print_section("Task Registry")
    try:
        task_registry = registry.TaskRegistry()
        aw_registry = task_registry.get_registry(task_registry.ANDROID_WORLD_FAMILY)
        task_count = len(aw_registry)
        print(f"✅ Task Registry: {task_count} tasks available")
        results['task_registry'] = True
    except Exception as e:
        print(f"❌ Task Registry: {e}")
        results['task_registry'] = False
    
    # Test 5: ADB connection
    print_section("ADB Connection")
    try:
        import subprocess
        adb_path = r"C:\Users\aney4\AppData\Local\Android\Sdk\platform-tools\adb.exe"
        if os.path.exists(adb_path):
            print(f"✅ ADB Path: {adb_path}")
            results['adb_path'] = True
        else:
            print(f"❌ ADB Path: Not found at {adb_path}")
            results['adb_path'] = False
    except Exception as e:
        print(f"❌ ADB Check: {e}")
        results['adb_path'] = False
    
    return results

def verify_challenge_2():
    """Verify Challenge 2: Custom Agent Framework."""
    print_header("CHALLENGE 2 VERIFICATION: Custom Agent Framework")
    
    results = {}
    
    # Test 1: Custom agent imports
    print_section("Custom Agent Components")
    try:
        from custom_agent import CustomAgent, DeviceController, MockDeviceController
        print("✅ Custom Agent Classes: Imported successfully")
        results['agent_classes'] = True
    except Exception as e:
        print(f"❌ Custom Agent Classes: {e}")
        results['agent_classes'] = False
    
    # Test 2: Device controller interface
    print_section("Device Controller Interface")
    try:
        from custom_agent import DeviceController, MockDeviceController
        mock_controller = MockDeviceController()
        print("✅ Mock Device Controller: Created successfully")
        results['mock_controller'] = True
    except Exception as e:
        print(f"❌ Mock Device Controller: {e}")
        results['mock_controller'] = False
    
    # Test 3: Task executor
    print_section("Task Executor")
    try:
        from custom_agent import TaskExecutor
        task_executor = TaskExecutor(mock_controller)
        print("✅ Task Executor: Created successfully")
        results['task_executor'] = True
    except Exception as e:
        print(f"❌ Task Executor: {e}")
        results['task_executor'] = False
    
    # Test 4: Custom agent functionality
    print_section("Custom Agent Functionality")
    try:
        agent = CustomAgent()
        print("✅ Custom Agent: Created successfully")
        results['agent_creation'] = True
    except Exception as e:
        print(f"❌ Custom Agent Creation: {e}")
        results['agent_creation'] = False
    
    # Test 5: Task execution
    print_section("Task Execution")
    try:
        agent = CustomAgent()
        result = agent.run_task("RecipeAddMultipleRecipes", {
            "recipe_name": "Test Recipe",
            "ingredients": ["ingredient1", "ingredient2"],
            "instructions": "Test instructions"
        })
        if result['success']:
            print("✅ Task Execution: RecipeAddMultipleRecipes completed successfully")
            results['task_execution'] = True
        else:
            print(f"❌ Task Execution: Failed - {result.get('error_message', 'Unknown error')}")
            results['task_execution'] = False
    except Exception as e:
        print(f"❌ Task Execution: {e}")
        results['task_execution'] = False
    
    # Test 6: Agent status
    print_section("Agent Status")
    try:
        agent = CustomAgent()
        status = agent.get_status()
        print(f"✅ Agent Status: {status['status']}")
        print(f"✅ Tasks Executed: {status['tasks_executed']}")
        results['agent_status'] = True
    except Exception as e:
        print(f"❌ Agent Status: {e}")
        results['agent_status'] = False
    
    return results

def print_results(challenge_name, results):
    """Print verification results."""
    print_section(f"{challenge_name} Results")
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    failed_tests = total_tests - passed_tests
    
    print(f"📊 Total Tests: {total_tests}")
    print(f"✅ Passed: {passed_tests}")
    print(f"❌ Failed: {failed_tests}")
    print(f"📈 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if failed_tests > 0:
        print("\n❌ Failed Tests:")
        for test_name, result in results.items():
            if not result:
                print(f"   - {test_name}")
    
    return passed_tests == total_tests

def main():
    """Main verification function."""
    print("🧪 AndroidWorld Challenge Verification")
    print("=" * 60)
    print("Verifying both Challenge 1 and Challenge 2 completion...")
    
    # Verify Challenge 1
    challenge_1_results = verify_challenge_1()
    challenge_1_success = print_results("Challenge 1", challenge_1_results)
    
    # Verify Challenge 2
    challenge_2_results = verify_challenge_2()
    challenge_2_success = print_results("Challenge 2", challenge_2_results)
    
    # Overall summary
    print_header("OVERALL VERIFICATION SUMMARY")
    
    if challenge_1_success and challenge_2_success:
        print("🎉 CONGRATULATIONS! Both challenges are working correctly!")
        print("✅ Challenge 1: Environment Setup - COMPLETE")
        print("✅ Challenge 2: Custom Agent Framework - COMPLETE")
        print("\n🚀 You're ready for Challenge 3: AI-Powered Task Execution!")
    elif challenge_1_success:
        print("⚠️  PARTIAL SUCCESS")
        print("✅ Challenge 1: Environment Setup - COMPLETE")
        print("❌ Challenge 2: Custom Agent Framework - NEEDS ATTENTION")
    elif challenge_2_success:
        print("⚠️  PARTIAL SUCCESS")
        print("❌ Challenge 1: Environment Setup - NEEDS ATTENTION")
        print("✅ Challenge 2: Custom Agent Framework - COMPLETE")
    else:
        print("❌ BOTH CHALLENGES NEED ATTENTION")
        print("❌ Challenge 1: Environment Setup - NEEDS ATTENTION")
        print("❌ Challenge 2: Custom Agent Framework - NEEDS ATTENTION")
    
    # Next steps
    print("\n📋 Next Steps:")
    if challenge_1_success and challenge_2_success:
        print("1. 🎯 Get GBOX API key for real device control")
        print("2. 🧠 Begin Challenge 3: AI integration")
        print("3. 📊 Run performance benchmarks on all 116 tasks")
        print("4. 🏆 Submit results to AndroidWorld leaderboard")
    else:
        print("1. 🔧 Fix any failed verification tests")
        print("2. 📚 Review challenge documentation")
        print("3. 🧪 Re-run verification after fixes")
    
    print("\n🎯 Verification completed!")

if __name__ == "__main__":
    main()
