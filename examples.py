"""Example usage of PyKeyEmu module

This script demonstrates various features and use cases of the PyKeyEmu library.
Run this script to see the module in action.

WARNING: This script will actually send keyboard input to your system.
Make sure you have a text editor or notepad open to see the results.
"""

import time
import pykeyemu
from pykeyemu import utils

def example_basic_typing():
    """Demonstrate basic string typing"""
    print("Example 1: Basic typing")
    print("Switch to a text editor and press Enter to continue...")
    input()
    
    # Type a simple message
    pykeyemu.type_string("Hello, World! This is PyKeyEmu in action.", delay=0.08)
    time.sleep(1)
    
    # Press Enter to create a new line
    pykeyemu.tap_key(pykeyemu.VK_RETURN)
    time.sleep(0.5)
    
    print("Basic typing example completed.\n")

def example_key_combinations():
    """Demonstrate key combinations and shortcuts"""
    print("Example 2: Key combinations")
    print("Make sure you have text selected in your editor...")
    input("Press Enter to continue...")
    
    # Simulate Ctrl+C (Copy)
    print("Copying selected text...")
    pykeyemu.tap_key(pykeyemu.VK_C, [pykeyemu.VK_CONTROL])
    time.sleep(0.5)
    
    # Move to end of line
    pykeyemu.tap_key(pykeyemu.VK_END)
    pykeyemu.tap_key(pykeyemu.VK_RETURN)
    
    # Simulate Ctrl+V (Paste)
    print("Pasting copied text...")
    pykeyemu.tap_key(pykeyemu.VK_V, [pykeyemu.VK_CONTROL])
    time.sleep(0.5)
    
    print("Key combinations example completed.\n")

def example_modifier_context():
    """Demonstrate using modifier context manager"""
    print("Example 3: Modifier context manager")
    input("Press Enter to continue...")
    
    # Type some text first
    pykeyemu.type_string("This text will be selected and replaced.", delay=0.05)
    time.sleep(1)
    
    # Select all text using context manager
    with pykeyemu.with_modifiers([pykeyemu.VK_CONTROL]):
        pykeyemu.tap_key(pykeyemu.VK_A)  # Ctrl+A (Select All)
    
    time.sleep(0.5)
    
    # Replace with new text
    pykeyemu.type_string("Text replaced using modifier context!", delay=0.05)
    
    print("Modifier context example completed.\n")

def example_special_keys():
    """Demonstrate special keys and navigation"""
    print("Example 4: Special keys and navigation")
    input("Press Enter to continue...")
    
    # Type a multi-line text
    lines = [
        "Line 1: First line of text",
        "Line 2: Second line of text", 
        "Line 3: Third line of text"
    ]
    
    for line in lines:
        pykeyemu.type_string(line, delay=0.03)
        pykeyemu.tap_key(pykeyemu.VK_RETURN)
        time.sleep(0.3)
    
    # Navigate using arrow keys
    print("Navigating with arrow keys...")
    
    # Go to beginning of document
    pykeyemu.tap_key(pykeyemu.VK_HOME, [pykeyemu.VK_CONTROL])
    time.sleep(0.5)
    
    # Move down two lines
    pykeyemu.tap_key(pykeyemu.VK_DOWN)
    pykeyemu.tap_key(pykeyemu.VK_DOWN)
    time.sleep(0.5)
    
    # Go to end of line
    pykeyemu.tap_key(pykeyemu.VK_END)
    time.sleep(0.5)
    
    # Add text at end of line
    pykeyemu.type_string(" <- Modified!", delay=0.05)
    
    print("Special keys example completed.\n")

def example_realistic_typing():
    """Demonstrate realistic typing with human-like delays"""
    print("Example 5: Realistic typing simulation")
    input("Press Enter to continue...")
    
    # Create a typing profile for 45 WPM (average typist)
    profile = utils.create_typing_profile(45)
    
    text = "This text is being typed with realistic human-like timing and occasional pauses."
    
    print(f"Typing at {profile['wpm']} WPM with realistic delays...")
    
    # Generate realistic delays
    delays = utils.apply_typing_profile(text, profile)
    
    # Type with realistic timing
    for i, char in enumerate(text):
        if utils._is_char_supported(char):
            # Get the VK code for the character
            if char.isupper():
                vk_code = pykeyemu.constants.CHAR_TO_VK.get(char.lower())
                if vk_code:
                    pykeyemu.tap_key(vk_code, [pykeyemu.VK_SHIFT])
            elif char in pykeyemu.constants.SHIFT_CHARS:
                base_char = pykeyemu.constants.SHIFT_CHAR_MAP.get(char)
                if base_char:
                    vk_code = pykeyemu.constants.CHAR_TO_VK.get(base_char)
                    if vk_code:
                        pykeyemu.tap_key(vk_code, [pykeyemu.VK_SHIFT])
            else:
                vk_code = pykeyemu.constants.CHAR_TO_VK.get(char)
                if vk_code:
                    pykeyemu.tap_key(vk_code)
            
            # Apply realistic delay
            if i < len(delays):
                time.sleep(delays[i])
    
    print("Realistic typing example completed.\n")

def example_text_validation():
    """Demonstrate text validation features"""
    print("Example 6: Text validation")
    
    test_texts = [
        "Hello, World!",
        "Mixed text with 数字 and symbols!",
        "Email: user@example.com",
        "Special chars: !@#$%^&*()",
        "Unsupported: 你好世界 🌍"
    ]
    
    for text in test_texts:
        valid, unsupported = utils.validate_text(text)
        print(f"Text: '{text}'")
        print(f"  Valid: {valid}")
        if not valid:
            print(f"  Unsupported chars: {unsupported}")
        
        # Show text chunks
        chunks = utils.split_text_by_support(text)
        print(f"  Chunks: {chunks}")
        print()
    
    print("Text validation example completed.\n")

def example_gaming_simulation():
    """Demonstrate gaming-style input simulation"""
    print("Example 7: Gaming simulation (WASD movement)")
    print("This will simulate game controls. Make sure a game or text editor is focused.")
    input("Press Enter to continue...")
    
    # Simulate WASD movement pattern
    movements = [
        (pykeyemu.VK_W, "Moving forward"),
        (pykeyemu.VK_D, "Moving right"),
        (pykeyemu.VK_S, "Moving backward"),
        (pykeyemu.VK_A, "Moving left"),
    ]
    
    for vk_code, description in movements:
        print(f"  {description}...")
        pykeyemu.press_key(vk_code)  # Press and hold
        time.sleep(1.0)  # Hold for 1 second
        pykeyemu.release_key(vk_code)  # Release
        time.sleep(0.5)  # Pause between movements
    
    # Simulate spell casting (Q -> R combo)
    print("  Casting spell combo...")
    pykeyemu.tap_key(pykeyemu.VK_Q)
    time.sleep(0.2)
    pykeyemu.tap_key(pykeyemu.VK_R)
    
    print("Gaming simulation example completed.\n")

def example_function_keys():
    """Demonstrate function key usage"""
    print("Example 8: Function keys")
    input("Press Enter to continue...")
    
    # Demonstrate various function keys
    function_keys = [
        (pykeyemu.VK_F1, "F1 - Help"),
        (pykeyemu.VK_F5, "F5 - Refresh"),
        (pykeyemu.VK_F11, "F11 - Fullscreen toggle"),
        (pykeyemu.VK_F12, "F12 - Developer tools")
    ]
    
    for vk_code, description in function_keys:
        print(f"  Pressing {description}")
        pykeyemu.tap_key(vk_code)
        time.sleep(1.0)
    
    print("Function keys example completed.\n")

def main():
    """Run all examples"""
    print("=" * 60)
    print("PyKeyEmu Examples")
    print("=" * 60)
    print()
    print("This script will demonstrate various features of PyKeyEmu.")
    print("Make sure you have a text editor (like Notepad) open and focused.")
    print()
    print("WARNING: This will send actual keyboard input to your system!")
    print("Press Ctrl+C at any time to stop.")
    print()
    
    try:
        # Run examples
        example_basic_typing()
        example_key_combinations()
        example_modifier_context()
        example_special_keys()
        example_realistic_typing()
        example_text_validation()
        example_gaming_simulation()
        example_function_keys()
        
        print("=" * 60)
        print("All examples completed successfully!")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n\nExamples interrupted by user.")
    except Exception as e:
        print(f"\n\nError occurred: {e}")
        print("Make sure you have the proper permissions and a text editor is focused.")

if __name__ == "__main__":
    main()