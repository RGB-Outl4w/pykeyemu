"""Utility functions for PyKeyEmu

This module provides helper functions for string processing, delays,
and other common operations used throughout the library.
"""

import time
import random
from typing import List, Tuple, Optional

from constants import CHAR_TO_VK, SHIFT_CHARS, SHIFT_CHAR_MAP, VK_SHIFT

def humanize_delay(base_delay: float = 0.05, variance: float = 0.02) -> float:
    """Generate a humanized delay with random variance
    
    Args:
        base_delay: Base delay in seconds
        variance: Maximum variance to add/subtract from base delay
        
    Returns:
        Randomized delay value
        
    Example:
        delay = humanize_delay(0.1, 0.03)  # Returns 0.07 to 0.13 seconds
    """
    if base_delay < 0:
        raise ValueError("Base delay must be non-negative")
    if variance < 0:
        raise ValueError("Variance must be non-negative")
        
    variation = random.uniform(-variance, variance)
    return max(0, base_delay + variation)

def validate_text(text: str) -> Tuple[bool, List[str]]:
    """Validate if text can be typed and return unsupported characters
    
    Args:
        text: Text to validate
        
    Returns:
        Tuple of (is_valid, list_of_unsupported_chars)
        
    Example:
        valid, unsupported = validate_text("Hello 世界!")
        # Returns (False, ['世', '界'])
    """
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    
    unsupported = []
    
    for char in text:
        if not _is_char_supported(char):
            if char not in unsupported:
                unsupported.append(char)
    
    return len(unsupported) == 0, unsupported

def _is_char_supported(char: str) -> bool:
    """Check if a single character is supported
    
    Args:
        char: Single character to check
        
    Returns:
        True if character can be typed, False otherwise
    """
    if len(char) != 1:
        return False
    
    # Check if it's a direct mapping
    if char in CHAR_TO_VK:
        return True
    
    # Check if it's an uppercase letter
    if char.isupper() and char.lower() in CHAR_TO_VK:
        return True
    
    # Check if it's a shift character
    if char in SHIFT_CHARS:
        base_char = SHIFT_CHAR_MAP.get(char)
        if base_char and base_char in CHAR_TO_VK:
            return True
    
    return False

def split_text_by_support(text: str) -> List[Tuple[str, bool]]:
    """Split text into chunks of supported and unsupported characters
    
    Args:
        text: Text to split
        
    Returns:
        List of tuples (text_chunk, is_supported)
        
    Example:
        chunks = split_text_by_support("Hello 世界 World")
        # Returns [('Hello ', True), ('世界', False), (' World', True)]
    """
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    
    if not text:
        return []
    
    chunks = []
    current_chunk = ""
    current_supported = _is_char_supported(text[0])
    
    for char in text:
        char_supported = _is_char_supported(char)
        
        if char_supported == current_supported:
            current_chunk += char
        else:
            if current_chunk:
                chunks.append((current_chunk, current_supported))
            current_chunk = char
            current_supported = char_supported
    
    if current_chunk:
        chunks.append((current_chunk, current_supported))
    
    return chunks

def calculate_typing_time(text: str, delay: float = 0.05) -> float:
    """Calculate estimated time to type text
    
    Args:
        text: Text to calculate timing for
        delay: Delay between keystrokes
        
    Returns:
        Estimated time in seconds
        
    Example:
        time_needed = calculate_typing_time("Hello World", 0.1)
        # Returns approximately 1.1 seconds (11 chars * 0.1)
    """
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if delay < 0:
        raise ValueError("Delay must be non-negative")
    
    # Count characters that will actually be typed
    typeable_chars = sum(1 for char in text if _is_char_supported(char))
    
    # Estimate time (last character doesn't have delay after it)
    if typeable_chars <= 1:
        return 0
    
    return (typeable_chars - 1) * delay

def normalize_line_endings(text: str, target: str = '\n') -> str:
    """Normalize line endings in text
    
    Args:
        text: Text to normalize
        target: Target line ending ('\n', '\r\n', or '\r')
        
    Returns:
        Text with normalized line endings
        
    Example:
        normalized = normalize_line_endings("Line1\r\nLine2\rLine3\n")
        # Returns "Line1\nLine2\nLine3\n"
    """
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    
    if target not in ['\n', '\r\n', '\r']:
        raise ValueError("Target must be '\\n', '\\r\\n', or '\\r'")
    
    # Replace all line ending variations with target
    text = text.replace('\r\n', '\n')  # Windows -> Unix
    text = text.replace('\r', '\n')    # Mac -> Unix
    
    if target != '\n':
        text = text.replace('\n', target)
    
    return text

def escape_special_chars(text: str) -> str:
    """Escape special characters for display purposes
    
    Args:
        text: Text to escape
        
    Returns:
        Text with escaped special characters
        
    Example:
        escaped = escape_special_chars("Hello\tWorld\n")
        # Returns "Hello\\tWorld\\n"
    """
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    
    escape_map = {
        '\n': '\\n',
        '\r': '\\r',
        '\t': '\\t',
        '\b': '\\b',
        '\f': '\\f',
        '\v': '\\v',
        '\0': '\\0'
    }
    
    result = text
    for char, escaped in escape_map.items():
        result = result.replace(char, escaped)
    
    return result

def create_typing_profile(wpm: int = 60) -> dict:
    """Create a typing profile with realistic delays
    
    Args:
        wpm: Words per minute (average typing speed)
        
    Returns:
        Dictionary with typing parameters
        
    Example:
        profile = create_typing_profile(80)  # Fast typist
        # Returns {'base_delay': 0.025, 'variance': 0.01, ...}
    """
    if wpm <= 0:
        raise ValueError("WPM must be positive")
    
    # Calculate base delay from WPM
    # Assuming average word length of 5 characters
    chars_per_minute = wpm * 5
    chars_per_second = chars_per_minute / 60
    base_delay = 1.0 / chars_per_second
    
    # Calculate variance based on typing speed
    # Slower typists have more variance
    if wpm >= 80:  # Fast typist
        variance_ratio = 0.2
    elif wpm >= 40:  # Average typist
        variance_ratio = 0.3
    else:  # Slow typist
        variance_ratio = 0.4
    
    variance = base_delay * variance_ratio
    
    return {
        'wpm': wpm,
        'base_delay': base_delay,
        'variance': variance,
        'pause_chance': 0.05,  # 5% chance of longer pause
        'pause_duration': base_delay * 3,  # 3x longer pause
    }

def apply_typing_profile(text: str, profile: dict) -> List[float]:
    """Generate delay sequence based on typing profile
    
    Args:
        text: Text to generate delays for
        profile: Typing profile from create_typing_profile()
        
    Returns:
        List of delays for each character
        
    Example:
        profile = create_typing_profile(60)
        delays = apply_typing_profile("Hello", profile)
        # Returns [0.18, 0.21, 0.19, 0.17, 0.20]
    """
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not isinstance(profile, dict):
        raise ValueError("Profile must be a dictionary")
    
    required_keys = ['base_delay', 'variance', 'pause_chance', 'pause_duration']
    for key in required_keys:
        if key not in profile:
            raise ValueError(f"Profile missing required key: {key}")
    
    delays = []
    
    for i, char in enumerate(text):
        if not _is_char_supported(char):
            continue
            
        # Check for random pause
        if random.random() < profile['pause_chance']:
            delay = profile['pause_duration']
        else:
            delay = humanize_delay(profile['base_delay'], profile['variance'])
        
        delays.append(delay)
    
    return delays