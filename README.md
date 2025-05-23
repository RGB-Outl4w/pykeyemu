# PyKeyEmu - Python Key Input Emulation for Windows

A lightweight and powerful Python module for programmatically emulating keyboard input on Windows OS. PyKeyEmu provides a simple yet comprehensive API for simulating key presses, releases, and complex key combinations.

## Features

- ✨ **Simple API**: Easy-to-use functions for common keyboard operations
- 🎯 **Precise Control**: Press, release, and tap individual keys with exact timing
- 🔧 **Modifier Support**: Full support for Ctrl, Shift, Alt, and other modifier keys
- 📝 **String Typing**: Efficiently type complete strings with customizable delays
- ⚡ **High Performance**: Uses modern Windows SendInput API for reliable input simulation
- 🛡️ **Safe & Reliable**: Comprehensive input validation and error handling
- 🧪 **Well Tested**: Extensive unit test coverage
- 📚 **Well Documented**: Clear documentation with practical examples

## Requirements

- **Operating System**: Windows 7 or later
- **Python**: 3.8 or later
- **Dependencies**: None (uses only standard library)

## Installation

### Option 1: Direct Usage
Since PyKeyEmu has no external dependencies, you can simply copy the module to your project:

```bash
# Clone or download the pykeyemu folder to your project
cp -r pykeyemu/ /path/to/your/project/
```

### Option 2: Add to Python Path
```python
import sys
sys.path.append('/path/to/pykeyemu')
import pykeyemu
```

## Quick Start

```python
import pykeyemu

# Tap a single key
pykeyemu.tap_key(pykeyemu.VK_RETURN)  # Press Enter

# Type a string
pykeyemu.type_string("Hello, World!")  # Type text

# Use key combinations
pykeyemu.tap_key(pykeyemu.VK_C, [pykeyemu.VK_CONTROL])  # Ctrl+C

# Press and hold keys
pykeyemu.press_key(pykeyemu.VK_SHIFT)   # Press Shift
pykeyemu.tap_key(pykeyemu.VK_A)         # Tap A (types "A")
pykeyemu.release_key(pykeyemu.VK_SHIFT) # Release Shift
```

## API Reference

### Core Functions

#### `press_key(vk_code)`
Press a key down (without releasing it).

```python
pykeyemu.press_key(pykeyemu.VK_SHIFT)  # Hold Shift
```

#### `release_key(vk_code)`
Release a previously pressed key.

```python
pykeyemu.release_key(pykeyemu.VK_SHIFT)  # Release Shift
```

#### `tap_key(vk_code, modifiers=None)`
Press and immediately release a key, optionally with modifiers.

```python
# Simple key tap
pykeyemu.tap_key(pykeyemu.VK_A)

# Key combination
pykeyemu.tap_key(pykeyemu.VK_S, [pykeyemu.VK_CONTROL])  # Ctrl+S

# Multiple modifiers
pykeyemu.tap_key(pykeyemu.VK_Z, [pykeyemu.VK_CONTROL, pykeyemu.VK_SHIFT])  # Ctrl+Shift+Z
```

#### `type_string(text, delay=0.05)`
Type a string of text with optional delay between characters.

```python
# Basic typing
pykeyemu.type_string("Hello, World!")

# Faster typing
pykeyemu.type_string("Quick message", delay=0.01)

# Slower, more human-like typing
pykeyemu.type_string("Careful typing", delay=0.15)
```

#### `with_modifiers(modifiers)`
Context manager for holding modifier keys.

```python
# Hold Ctrl while performing multiple actions
with pykeyemu.with_modifiers([pykeyemu.VK_CONTROL]):
    pykeyemu.tap_key(pykeyemu.VK_A)  # Ctrl+A (Select All)
    pykeyemu.tap_key(pykeyemu.VK_C)  # Ctrl+C (Copy)
```

#### `is_key_pressed(vk_code)`
Check if a key is currently pressed.

```python
if pykeyemu.is_key_pressed(pykeyemu.VK_SHIFT):
    print("Shift is currently pressed")
```

### Virtual Key Codes

PyKeyEmu provides constants for all common virtual key codes:

#### Letters and Numbers
```python
pykeyemu.VK_A, pykeyemu.VK_B, ..., pykeyemu.VK_Z
pykeyemu.VK_0, pykeyemu.VK_1, ..., pykeyemu.VK_9
```

#### Special Keys
```python
pykeyemu.VK_RETURN      # Enter
pykeyemu.VK_ESCAPE      # Escape
pykeyemu.VK_SPACE       # Space
pykeyemu.VK_TAB         # Tab
pykeyemu.VK_BACK        # Backspace
pykeyemu.VK_DELETE      # Delete
```

#### Modifier Keys
```python
pykeyemu.VK_SHIFT       # Shift
pykeyemu.VK_CONTROL     # Ctrl
pykeyemu.VK_MENU        # Alt
```

#### Arrow Keys
```python
pykeyemu.VK_LEFT        # Left Arrow
pykeyemu.VK_RIGHT       # Right Arrow
pykeyemu.VK_UP          # Up Arrow
pykeyemu.VK_DOWN        # Down Arrow
```

#### Function Keys
```python
pykeyemu.VK_F1, pykeyemu.VK_F2, ..., pykeyemu.VK_F12
```

#### Navigation Keys
```python
pykeyemu.VK_HOME        # Home
pykeyemu.VK_END         # End
pykeyemu.VK_PRIOR       # Page Up
pykeyemu.VK_NEXT        # Page Down
pykeyemu.VK_INSERT      # Insert
```

## Advanced Usage

### Realistic Typing Simulation

```python
from pykeyemu import utils

# Create a typing profile for 60 WPM
profile = utils.create_typing_profile(60)

# Generate realistic delays
text = "This is realistic typing"
delays = utils.apply_typing_profile(text, profile)

# Type with realistic timing
for i, char in enumerate(text):
    if utils._is_char_supported(char):
        # Type character (simplified - actual implementation in type_string)
        delay = delays[i] if i < len(delays) else 0
        time.sleep(delay)
```

### Text Validation

```python
from pykeyemu import utils

# Check if text can be typed
text = "Hello 世界!"  # Mixed English and Chinese
valid, unsupported = utils.validate_text(text)

if not valid:
    print(f"Unsupported characters: {unsupported}")
    # Handle unsupported characters
```

### Complex Key Sequences

```python
# Simulate Ctrl+Alt+Delete (be careful with this!)
pykeyemu.press_key(pykeyemu.VK_CONTROL)
pykeyemu.press_key(pykeyemu.VK_MENU)  # Alt
pykeyemu.tap_key(pykeyemu.VK_DELETE)
pykeyemu.release_key(pykeyemu.VK_MENU)
pykeyemu.release_key(pykeyemu.VK_CONTROL)

# Or use the context manager
with pykeyemu.with_modifiers([pykeyemu.VK_CONTROL, pykeyemu.VK_MENU]):
    pykeyemu.tap_key(pykeyemu.VK_DELETE)
```

### Gaming Applications

```python
# WASD movement simulation
def move_forward():
    pykeyemu.press_key(pykeyemu.VK_W)

def stop_moving():
    pykeyemu.release_key(pykeyemu.VK_W)

# Simulate key combo for gaming
def cast_spell():
    pykeyemu.tap_key(pykeyemu.VK_Q)  # Spell hotkey
    time.sleep(0.1)
    pykeyemu.tap_key(pykeyemu.VK_R)  # Follow-up ability
```

## Utility Functions

PyKeyEmu includes several utility functions for advanced use cases:

### Text Processing
```python
from pykeyemu import utils

# Normalize line endings
text = utils.normalize_line_endings("Line1\r\nLine2\rLine3\n")

# Calculate typing time
time_needed = utils.calculate_typing_time("Hello World", delay=0.1)

# Split text by character support
chunks = utils.split_text_by_support("Hello 世界 World")
# Returns: [('Hello ', True), ('世界', False), (' World', True)]
```

### Timing and Delays
```python
from pykeyemu import utils

# Generate humanized delays
delay = utils.humanize_delay(0.1, 0.02)  # Base ± variance

# Create typing profiles
fast_profile = utils.create_typing_profile(80)    # 80 WPM
slow_profile = utils.create_typing_profile(30)    # 30 WPM
```

## Testing

Run the comprehensive test suite:

```python
# Run all tests
from pykeyemu.test_pykeyemu import run_tests
success = run_tests()

# Or run specific test classes
import unittest
from pykeyemu.test_pykeyemu import TestConstants, TestUtils

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestConstants))
suite.addTest(unittest.makeSuite(TestUtils))

runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)
```

## Common Use Cases

### 1. Automation Scripts
```python
# Automate form filling
pykeyemu.type_string("john.doe@example.com")
pykeyemu.tap_key(pykeyemu.VK_TAB)  # Move to next field
pykeyemu.type_string("SecurePassword123")
pykeyemu.tap_key(pykeyemu.VK_RETURN)  # Submit
```

### 2. Testing Applications
```python
# Test keyboard shortcuts
pykeyemu.tap_key(pykeyemu.VK_N, [pykeyemu.VK_CONTROL])  # Ctrl+N (New)
time.sleep(1)
pykeyemu.type_string("Test document content")
pykeyemu.tap_key(pykeyemu.VK_S, [pykeyemu.VK_CONTROL])  # Ctrl+S (Save)
```

### 3. Game Automation
```python
# Simulate player actions
def auto_attack():
    pykeyemu.tap_key(pykeyemu.VK_SPACE)  # Attack
    time.sleep(0.5)
    pykeyemu.tap_key(pykeyemu.VK_1)      # Use skill 1
    time.sleep(2.0)
    pykeyemu.tap_key(pykeyemu.VK_2)      # Use skill 2
```

### 4. Accessibility Tools
```python
# Create custom keyboard shortcuts
def quick_copy_paste():
    # Select all, copy, and paste
    pykeyemu.tap_key(pykeyemu.VK_A, [pykeyemu.VK_CONTROL])
    time.sleep(0.1)
    pykeyemu.tap_key(pykeyemu.VK_C, [pykeyemu.VK_CONTROL])
    time.sleep(0.1)
    pykeyemu.tap_key(pykeyemu.VK_V, [pykeyemu.VK_CONTROL])
```

## Limitations and Considerations

### Security and Detection
- Some applications may detect simulated input as automation
- Antivirus software might flag input simulation as suspicious
- Games with anti-cheat systems may block or detect synthetic input

### Character Support
- Currently supports standard ASCII characters and common symbols
- Unicode characters (like Chinese, Arabic, etc.) are not directly supported
- Keyboard layout dependencies may affect some special characters

### System State
- Caps Lock, Num Lock, and Scroll Lock states are not automatically handled
- Current keyboard layout affects character mapping
- Focus must be on the target application window

### Performance
- Very rapid input may be ignored by some applications
- Network latency can affect remote desktop scenarios
- System load may impact timing accuracy

## Best Practices

### 1. Always Add Delays
```python
# Good: Realistic timing
pykeyemu.type_string("Hello", delay=0.05)
time.sleep(0.5)
pykeyemu.tap_key(pykeyemu.VK_RETURN)

# Avoid: Too fast, may be ignored
pykeyemu.type_string("Hello", delay=0.001)
pykeyemu.tap_key(pykeyemu.VK_RETURN)
```

### 2. Handle Errors Gracefully
```python
try:
    result = pykeyemu.type_string("Test input")
    if not result:
        print("Failed to send input")
except ValueError as e:
    print(f"Invalid input: {e}")
```

### 3. Validate Input
```python
from pykeyemu import utils

text = "User input text"
valid, unsupported = utils.validate_text(text)
if valid:
    pykeyemu.type_string(text)
else:
    print(f"Cannot type characters: {unsupported}")
```

### 4. Use Context Managers
```python
# Good: Automatic cleanup
with pykeyemu.with_modifiers([pykeyemu.VK_CONTROL]):
    pykeyemu.tap_key(pykeyemu.VK_A)
    pykeyemu.tap_key(pykeyemu.VK_C)

# Avoid: Manual management (error-prone)
pykeyemu.press_key(pykeyemu.VK_CONTROL)
pykeyemu.tap_key(pykeyemu.VK_A)
# If error occurs here, Ctrl might stay pressed!
pykeyemu.release_key(pykeyemu.VK_CONTROL)
```

## Troubleshooting

### Input Not Working
1. **Check target application focus**: Ensure the target window is active
2. **Verify permissions**: Some applications require administrator privileges
3. **Test with simple input**: Try basic key taps before complex sequences
4. **Check timing**: Add delays between operations

### Characters Not Typing Correctly
1. **Verify keyboard layout**: Ensure US English layout for best compatibility
2. **Check character support**: Use `utils.validate_text()` to verify
3. **Test modifier keys**: Ensure Shift, Ctrl, Alt are working correctly

### Performance Issues
1. **Reduce input speed**: Increase delays between keystrokes
2. **Batch operations**: Use `type_string()` instead of individual `tap_key()` calls
3. **Check system resources**: High CPU usage may affect timing

## Contributing

Contributions are welcome! Please ensure:

1. **Code Quality**: Follow existing code style and patterns
2. **Testing**: Add tests for new functionality
3. **Documentation**: Update README and docstrings
4. **Compatibility**: Maintain Windows 7+ compatibility

## License

This project is released under the MIT License. See LICENSE file for details.

## Support

If you find this project useful, consider supporting it by donating or becoming a sponsor. Your support helps keep the project alive and continuously improved.

[![Donate](https://img.shields.io/badge/Donate-Boosty-orange.svg)](https://boosty.to/rgboutlaw/donate)

---

**Note**: This tool is intended for legitimate automation, testing, and accessibility purposes. Please use responsibly and in accordance with applicable laws and terms of service.