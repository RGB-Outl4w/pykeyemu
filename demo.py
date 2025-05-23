"""Quick demo of PyKeyEmu functionality

This script demonstrates the basic capabilities of PyKeyEmu.
It will NOT actually send keyboard input - it just shows the API usage.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the module
import __init__ as pykeyemu
from utils import validate_text, create_typing_profile

def demo_basic_usage():
    """Demonstrate basic PyKeyEmu usage"""
    print("=" * 50)
    print("PyKeyEmu Basic Usage Demo")
    print("=" * 50)
    
    print("\n1. Available Virtual Key Codes:")
    print(f"   VK_A = {pykeyemu.VK_A}")
    print(f"   VK_RETURN = {pykeyemu.VK_RETURN}")
    print(f"   VK_SPACE = {pykeyemu.VK_SPACE}")
    print(f"   VK_CONTROL = {pykeyemu.VK_CONTROL}")
    print(f"   VK_SHIFT = {pykeyemu.VK_SHIFT}")
    
    print("\n2. Basic Function Calls (simulated):")
    print("   pykeyemu.tap_key(pykeyemu.VK_A)  # Tap 'A' key")
    print("   pykeyemu.type_string('Hello, World!')  # Type text")
    print("   pykeyemu.tap_key(pykeyemu.VK_C, [pykeyemu.VK_CONTROL])  # Ctrl+C")
    
    print("\n3. Text Validation:")
    test_texts = [
        "Hello, World!",
        "Email: user@example.com",
        "Mixed: Hello 世界",
        "Symbols: !@#$%^&*()"
    ]
    
    for text in test_texts:
        valid, unsupported = validate_text(text)
        status = "✓ Valid" if valid else f"✗ Invalid (unsupported: {unsupported})"
        print(f"   '{text}' -> {status}")
    
    print("\n4. Typing Profiles:")
    for wpm in [30, 60, 90]:
        profile = create_typing_profile(wpm)
        print(f"   {wpm} WPM: base_delay={profile['base_delay']:.3f}s, variance={profile['variance']:.3f}s")
    
    print("\n5. Available Functions:")
    functions = [attr for attr in dir(pykeyemu) if not attr.startswith('_') and callable(getattr(pykeyemu, attr))]
    for func in functions:
        print(f"   - {func}()")
    
    print("\n" + "=" * 50)
    print("Demo completed successfully!")
    print("\nTo actually use PyKeyEmu:")
    print("1. Import the module: import pykeyemu")
    print("2. Use functions like: pykeyemu.type_string('Hello!')")
    print("3. See examples.py for more detailed usage")
    print("=" * 50)

def demo_code_examples():
    """Show code examples"""
    print("\n" + "=" * 50)
    print("Code Examples")
    print("=" * 50)
    
    examples = [
        {
            "title": "Basic Key Tap",
            "code": "pykeyemu.tap_key(pykeyemu.VK_RETURN)  # Press Enter"
        },
        {
            "title": "Type String",
            "code": "pykeyemu.type_string('Hello, World!', delay=0.05)"
        },
        {
            "title": "Key Combination",
            "code": "pykeyemu.tap_key(pykeyemu.VK_S, [pykeyemu.VK_CONTROL])  # Ctrl+S"
        },
        {
            "title": "Multiple Modifiers",
            "code": "pykeyemu.tap_key(pykeyemu.VK_Z, [pykeyemu.VK_CONTROL, pykeyemu.VK_SHIFT])  # Ctrl+Shift+Z"
        },
        {
            "title": "Context Manager",
            "code": """with pykeyemu.with_modifiers([pykeyemu.VK_CONTROL]):
    pykeyemu.tap_key(pykeyemu.VK_A)  # Ctrl+A
    pykeyemu.tap_key(pykeyemu.VK_C)  # Ctrl+C"""
        },
        {
            "title": "Manual Press/Release",
            "code": """pykeyemu.press_key(pykeyemu.VK_SHIFT)   # Hold Shift
pykeyemu.tap_key(pykeyemu.VK_A)         # Tap A (types 'A')
pykeyemu.release_key(pykeyemu.VK_SHIFT) # Release Shift"""
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. {example['title']}:")
        for line in example['code'].split('\n'):
            print(f"   {line}")

def main():
    """Run the demo"""
    try:
        demo_basic_usage()
        demo_code_examples()
        
        print("\n🎉 PyKeyEmu is ready to use!")
        print("\nNext steps:")
        print("- Run 'python examples.py' for interactive examples")
        print("- Check README.md for complete documentation")
        print("- Run 'python simple_test.py' to verify installation")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)