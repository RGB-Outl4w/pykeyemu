"""PyKeyEmu - Python Key Input Emulation Module for Windows

A lightweight Python module for programmatically emulating keyboard input on Windows OS.
Supports key press/release events, modifier keys, special keys, and string typing.

Example usage:
    import pykeyemu
    
    # Tap Enter key
    pykeyemu.tap_key(pykeyemu.VK_RETURN)
    
    # Type a string
    pykeyemu.type_string("Hello, world!", delay=0.1)
    
    # Press Ctrl+C
    pykeyemu.press_key(pykeyemu.VK_CONTROL)
    pykeyemu.tap_key(pykeyemu.VK_C)
    pykeyemu.release_key(pykeyemu.VK_CONTROL)
"""

try:
    # Try relative imports first (when used as a package)
    from .wininput import press_key, release_key, tap_key, type_string, with_modifiers
    from .constants import *
except ImportError:
    # Fall back to absolute imports (when used as standalone modules)
    from wininput import press_key, release_key, tap_key, type_string, with_modifiers
    from constants import *

__version__ = "1.0.0"
__author__ = "OutlawRGB"
__description__ = "Python Key Input Emulation Module for Windows"

# Public API
__all__ = [
    'press_key',
    'release_key', 
    'tap_key',
    'type_string',
    'with_modifiers',
    # Virtual Key Codes
    'VK_RETURN',
    'VK_ESCAPE',
    'VK_SPACE',
    'VK_SHIFT',
    'VK_CONTROL',
    'VK_MENU',
    'VK_TAB',
    'VK_BACK',
    'VK_DELETE',
    'VK_LEFT',
    'VK_RIGHT',
    'VK_UP',
    'VK_DOWN',
    'VK_HOME',
    'VK_END',
    'VK_PRIOR',
    'VK_NEXT',
    'VK_INSERT',
    'VK_F1', 'VK_F2', 'VK_F3', 'VK_F4', 'VK_F5', 'VK_F6',
    'VK_F7', 'VK_F8', 'VK_F9', 'VK_F10', 'VK_F11', 'VK_F12',
    'VK_A', 'VK_B', 'VK_C', 'VK_D', 'VK_E', 'VK_F', 'VK_G',
    'VK_H', 'VK_I', 'VK_J', 'VK_K', 'VK_L', 'VK_M', 'VK_N',
    'VK_O', 'VK_P', 'VK_Q', 'VK_R', 'VK_S', 'VK_T', 'VK_U',
    'VK_V', 'VK_W', 'VK_X', 'VK_Y', 'VK_Z',
    'VK_0', 'VK_1', 'VK_2', 'VK_3', 'VK_4', 'VK_5',
    'VK_6', 'VK_7', 'VK_8', 'VK_9'
]