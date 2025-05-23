"""Simple test script to verify PyKeyEmu basic functionality"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        import constants
        print("✓ constants module imported successfully")
        print(f"  VK_A = {constants.VK_A}")
        print(f"  VK_RETURN = {constants.VK_RETURN}")
    except Exception as e:
        print(f"✗ Failed to import constants: {e}")
        return False
    
    try:
        import utils
        print("✓ utils module imported successfully")
    except Exception as e:
        print(f"✗ Failed to import utils: {e}")
        return False
    
    try:
        import wininput
        print("✓ wininput module imported successfully")
    except Exception as e:
        print(f"✗ Failed to import wininput: {e}")
        return False
    
    return True

def test_constants():
    """Test constants module"""
    print("\nTesting constants...")
    
    import constants
    
    # Test VK codes are integers
    assert isinstance(constants.VK_A, int), "VK_A should be an integer"
    assert isinstance(constants.VK_RETURN, int), "VK_RETURN should be an integer"
    
    # Test VK codes are in valid range
    assert 0 <= constants.VK_A <= 255, "VK_A should be in range 0-255"
    assert 0 <= constants.VK_RETURN <= 255, "VK_RETURN should be in range 0-255"
    
    # Test character mapping
    assert constants.CHAR_TO_VK['a'] == constants.VK_A, "Character 'a' should map to VK_A"
    assert constants.CHAR_TO_VK[' '] == constants.VK_SPACE, "Space should map to VK_SPACE"
    
    print("✓ Constants tests passed")
    return True

def test_utils():
    """Test utils module"""
    print("\nTesting utils...")
    
    import utils
    
    # Test text validation
    valid, unsupported = utils.validate_text("Hello World")
    assert valid == True, "'Hello World' should be valid"
    assert len(unsupported) == 0, "'Hello World' should have no unsupported chars"
    
    # Test humanize delay
    delay = utils.humanize_delay(0.1, 0.02)
    assert isinstance(delay, float), "Delay should be a float"
    assert delay >= 0, "Delay should be non-negative"
    
    # Test typing time calculation
    time_needed = utils.calculate_typing_time("Hello", 0.1)
    assert isinstance(time_needed, float), "Typing time should be a float"
    assert time_needed >= 0, "Typing time should be non-negative"
    
    print("✓ Utils tests passed")
    return True

def test_wininput_structures():
    """Test that wininput structures can be created"""
    print("\nTesting wininput structures...")
    
    import wininput
    
    # Test that we can create the structures without errors
    try:
        input_struct = wininput._create_keyboard_input(65, 0)  # VK_A
        assert input_struct.type == wininput.INPUT_KEYBOARD
        assert input_struct.ki.wVk == 65
        print("✓ Keyboard input structure created successfully")
    except Exception as e:
        print(f"✗ Failed to create keyboard input structure: {e}")
        return False
    
    return True

def test_main_module():
    """Test the main module import"""
    print("\nTesting main module...")
    
    try:
        # Import the __init__ module directly since we're not in a package
        import __init__ as pykeyemu
        
        # Check that key functions are available
        assert hasattr(pykeyemu, 'press_key'), "press_key function should be available"
        assert hasattr(pykeyemu, 'release_key'), "release_key function should be available"
        assert hasattr(pykeyemu, 'tap_key'), "tap_key function should be available"
        assert hasattr(pykeyemu, 'type_string'), "type_string function should be available"
        
        # Check that constants are available
        assert hasattr(pykeyemu, 'VK_A'), "VK_A constant should be available"
        assert hasattr(pykeyemu, 'VK_RETURN'), "VK_RETURN constant should be available"
        
        print("✓ Main module imported successfully")
        print(f"  Available functions: {[f for f in dir(pykeyemu) if not f.startswith('_') and callable(getattr(pykeyemu, f))]}")
        print(f"  VK_A = {pykeyemu.VK_A}")
        print(f"  VK_RETURN = {pykeyemu.VK_RETURN}")
        
        return True
        
    except Exception as e:
        print(f"✗ Failed to import main module: {e}")
        return False

def main():
    """Run all tests"""
    print("PyKeyEmu Simple Test Suite")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_constants,
        test_utils,
        test_wininput_structures,
        test_main_module,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} failed with exception: {e}")
    
    print("\n" + "=" * 40)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! PyKeyEmu is working correctly.")
        return True
    else:
        print("❌ Some tests failed. Please check the output above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)