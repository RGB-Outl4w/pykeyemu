"""Windows-specific keyboard input simulation using ctypes and Win32 API

This module provides the core functionality for simulating keyboard input on Windows
using the SendInput API for reliable and modern input simulation.
"""

import ctypes
import time
from ctypes import wintypes
from contextlib import contextmanager
from typing import List, Union, Optional

# Define ULONG_PTR if not available (for older Python versions)
if not hasattr(wintypes, 'ULONG_PTR'):
    if ctypes.sizeof(ctypes.c_void_p) == 8:
        wintypes.ULONG_PTR = ctypes.c_uint64
    else:
        wintypes.ULONG_PTR = ctypes.c_uint32

from constants import (
    INPUT_KEYBOARD, KEYEVENTF_KEYUP, KEYEVENTF_EXTENDEDKEY,
    CHAR_TO_VK, SHIFT_CHARS, SHIFT_CHAR_MAP, VK_SHIFT
)

# Load user32.dll
user32 = ctypes.WinDLL('user32', use_last_error=True)

# Define Windows structures
class KEYBDINPUT(ctypes.Structure):
    """Keyboard input structure for SendInput API"""
    _fields_ = [
        ("wVk", wintypes.WORD),         # Virtual key code
        ("wScan", wintypes.WORD),       # Scan code
        ("dwFlags", wintypes.DWORD),    # Flags
        ("time", wintypes.DWORD),       # Timestamp (0 for current time)
        ("dwExtraInfo", wintypes.ULONG_PTR),  # Extra info
    ]

class INPUT(ctypes.Structure):
    """Input structure for SendInput API"""
    class _INPUT(ctypes.Union):
        _fields_ = [
            ("ki", KEYBDINPUT),
        ]
    
    _fields_ = [
        ("type", wintypes.DWORD),
        ("_input", _INPUT),
    ]
    
    @property
    def ki(self):
        return self._input.ki
    
    @ki.setter
    def ki(self, value):
        self._input.ki = value

# Define SendInput function
user32.SendInput.argtypes = [
    wintypes.UINT,                    # Number of inputs
    ctypes.POINTER(INPUT),            # Array of inputs
    ctypes.c_int                      # Size of INPUT structure
]
user32.SendInput.restype = wintypes.UINT

def _create_keyboard_input(vk_code: int, flags: int = 0) -> INPUT:
    """Create a keyboard INPUT structure
    
    Args:
        vk_code: Virtual key code
        flags: Keyboard event flags
        
    Returns:
        INPUT structure ready for SendInput
    """
    input_struct = INPUT()
    input_struct.type = INPUT_KEYBOARD
    input_struct.ki = KEYBDINPUT(
        wVk=vk_code,
        wScan=0,
        dwFlags=flags,
        time=0,
        dwExtraInfo=0
    )
    return input_struct

def _send_input(inputs: List[INPUT]) -> bool:
    """Send input events to the system
    
    Args:
        inputs: List of INPUT structures
        
    Returns:
        True if successful, False otherwise
    """
    if not inputs:
        return True
        
    input_array = (INPUT * len(inputs))(*inputs)
    result = user32.SendInput(
        len(inputs),
        input_array,
        ctypes.sizeof(INPUT)
    )
    
    return result == len(inputs)

def press_key(vk_code: int) -> bool:
    """Press a key down (without releasing it)
    
    Args:
        vk_code: Virtual key code to press
        
    Returns:
        True if successful, False otherwise
        
    Example:
        press_key(VK_SHIFT)  # Press and hold Shift
    """
    if not isinstance(vk_code, int) or vk_code < 0 or vk_code > 255:
        raise ValueError(f"Invalid virtual key code: {vk_code}")
        
    input_down = _create_keyboard_input(vk_code, 0)
    return _send_input([input_down])

def release_key(vk_code: int) -> bool:
    """Release a key that was previously pressed
    
    Args:
        vk_code: Virtual key code to release
        
    Returns:
        True if successful, False otherwise
        
    Example:
        release_key(VK_SHIFT)  # Release Shift key
    """
    if not isinstance(vk_code, int) or vk_code < 0 or vk_code > 255:
        raise ValueError(f"Invalid virtual key code: {vk_code}")
        
    input_up = _create_keyboard_input(vk_code, KEYEVENTF_KEYUP)
    return _send_input([input_up])

def tap_key(vk_code: int, modifiers: Optional[List[int]] = None) -> bool:
    """Press and immediately release a key
    
    Args:
        vk_code: Virtual key code to tap
        modifiers: Optional list of modifier keys to hold during tap
        
    Returns:
        True if successful, False otherwise
        
    Example:
        tap_key(VK_A)                    # Tap 'A'
        tap_key(VK_C, [VK_CONTROL])     # Tap Ctrl+C
    """
    if not isinstance(vk_code, int) or vk_code < 0 or vk_code > 255:
        raise ValueError(f"Invalid virtual key code: {vk_code}")
        
    inputs = []
    
    # Press modifiers
    if modifiers:
        for mod in modifiers:
            if not isinstance(mod, int) or mod < 0 or mod > 255:
                raise ValueError(f"Invalid modifier key code: {mod}")
            inputs.append(_create_keyboard_input(mod, 0))
    
    # Press and release main key
    inputs.append(_create_keyboard_input(vk_code, 0))
    inputs.append(_create_keyboard_input(vk_code, KEYEVENTF_KEYUP))
    
    # Release modifiers (in reverse order)
    if modifiers:
        for mod in reversed(modifiers):
            inputs.append(_create_keyboard_input(mod, KEYEVENTF_KEYUP))
    
    return _send_input(inputs)

def type_string(text: str, delay: float = 0.05) -> bool:
    """Type a string of text
    
    Args:
        text: String to type
        delay: Delay between keystrokes in seconds (default: 0.05)
        
    Returns:
        True if successful, False otherwise
        
    Example:
        type_string("Hello, World!")           # Type with default delay
        type_string("Fast typing", delay=0.01) # Type faster
    """
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
        
    if delay < 0:
        raise ValueError("Delay must be non-negative")
    
    success = True
    
    for char in text:
        char_success = _type_character(char)
        if not char_success:
            success = False
            
        if delay > 0:
            time.sleep(delay)
    
    return success

def _type_character(char: str) -> bool:
    """Type a single character
    
    Args:
        char: Single character to type
        
    Returns:
        True if successful, False otherwise
    """
    if len(char) != 1:
        raise ValueError("Must provide exactly one character")
    
    # Handle special shift characters
    if char in SHIFT_CHARS:
        if char.isupper():
            # Uppercase letter
            vk_code = CHAR_TO_VK.get(char.lower())
            if vk_code:
                return tap_key(vk_code, [VK_SHIFT])
        else:
            # Special character requiring shift
            base_char = SHIFT_CHAR_MAP.get(char)
            if base_char:
                vk_code = CHAR_TO_VK.get(base_char)
                if vk_code:
                    return tap_key(vk_code, [VK_SHIFT])
    
    # Handle regular characters
    vk_code = CHAR_TO_VK.get(char)
    if vk_code:
        return tap_key(vk_code)
    
    # Character not supported
    print(f"Warning: Character '{char}' (ord: {ord(char)}) not supported")
    return False

@contextmanager
def with_modifiers(modifiers: List[int]):
    """Context manager for holding modifier keys
    
    Args:
        modifiers: List of modifier key codes to hold
        
    Example:
        with with_modifiers([VK_CONTROL, VK_SHIFT]):
            tap_key(VK_A)  # Types Ctrl+Shift+A
    """
    if not isinstance(modifiers, list):
        raise ValueError("Modifiers must be a list")
    
    # Press all modifiers
    for mod in modifiers:
        if not isinstance(mod, int) or mod < 0 or mod > 255:
            raise ValueError(f"Invalid modifier key code: {mod}")
        press_key(mod)
    
    try:
        yield
    finally:
        # Release all modifiers (in reverse order)
        for mod in reversed(modifiers):
            release_key(mod)

def is_key_pressed(vk_code: int) -> bool:
    """Check if a key is currently pressed
    
    Args:
        vk_code: Virtual key code to check
        
    Returns:
        True if key is pressed, False otherwise
    """
    if not isinstance(vk_code, int) or vk_code < 0 or vk_code > 255:
        raise ValueError(f"Invalid virtual key code: {vk_code}")
        
    # Use GetAsyncKeyState to check key state
    user32.GetAsyncKeyState.argtypes = [ctypes.c_int]
    user32.GetAsyncKeyState.restype = wintypes.SHORT
    
    state = user32.GetAsyncKeyState(vk_code)
    # Check if the most significant bit is set (key is pressed)
    return (state & 0x8000) != 0