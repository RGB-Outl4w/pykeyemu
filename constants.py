"""Constants for Windows Virtual Key Codes and Input Flags

This module contains all the virtual key codes and flags used by the Windows API
for keyboard input simulation.
"""

# Input types
INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2

# Keyboard event flags
KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_UNICODE = 0x0004
KEYEVENTF_SCANCODE = 0x0008

# Virtual Key Codes - Special Keys
VK_BACK = 0x08          # Backspace
VK_TAB = 0x09           # Tab
VK_RETURN = 0x0D        # Enter
VK_SHIFT = 0x10         # Shift
VK_CONTROL = 0x11       # Ctrl
VK_MENU = 0x12          # Alt
VK_PAUSE = 0x13         # Pause
VK_CAPITAL = 0x14       # Caps Lock
VK_ESCAPE = 0x1B        # Escape
VK_SPACE = 0x20         # Space
VK_PRIOR = 0x21         # Page Up
VK_NEXT = 0x22          # Page Down
VK_END = 0x23           # End
VK_HOME = 0x24          # Home
VK_LEFT = 0x25          # Left Arrow
VK_UP = 0x26            # Up Arrow
VK_RIGHT = 0x27         # Right Arrow
VK_DOWN = 0x28          # Down Arrow
VK_SELECT = 0x29        # Select
VK_PRINT = 0x2A         # Print
VK_EXECUTE = 0x2B       # Execute
VK_SNAPSHOT = 0x2C      # Print Screen
VK_INSERT = 0x2D        # Insert
VK_DELETE = 0x2E        # Delete
VK_HELP = 0x2F          # Help

# Virtual Key Codes - Numbers
VK_0 = 0x30
VK_1 = 0x31
VK_2 = 0x32
VK_3 = 0x33
VK_4 = 0x34
VK_5 = 0x35
VK_6 = 0x36
VK_7 = 0x37
VK_8 = 0x38
VK_9 = 0x39

# Virtual Key Codes - Letters
VK_A = 0x41
VK_B = 0x42
VK_C = 0x43
VK_D = 0x44
VK_E = 0x45
VK_F = 0x46
VK_G = 0x47
VK_H = 0x48
VK_I = 0x49
VK_J = 0x4A
VK_K = 0x4B
VK_L = 0x4C
VK_M = 0x4D
VK_N = 0x4E
VK_O = 0x4F
VK_P = 0x50
VK_Q = 0x51
VK_R = 0x52
VK_S = 0x53
VK_T = 0x54
VK_U = 0x55
VK_V = 0x56
VK_W = 0x57
VK_X = 0x58
VK_Y = 0x59
VK_Z = 0x5A

# Virtual Key Codes - Windows Keys
VK_LWIN = 0x5B          # Left Windows key
VK_RWIN = 0x5C          # Right Windows key
VK_APPS = 0x5D          # Applications key

# Virtual Key Codes - Numpad
VK_NUMPAD0 = 0x60
VK_NUMPAD1 = 0x61
VK_NUMPAD2 = 0x62
VK_NUMPAD3 = 0x63
VK_NUMPAD4 = 0x64
VK_NUMPAD5 = 0x65
VK_NUMPAD6 = 0x66
VK_NUMPAD7 = 0x67
VK_NUMPAD8 = 0x68
VK_NUMPAD9 = 0x69
VK_MULTIPLY = 0x6A      # Numpad *
VK_ADD = 0x6B           # Numpad +
VK_SEPARATOR = 0x6C     # Numpad separator
VK_SUBTRACT = 0x6D      # Numpad -
VK_DECIMAL = 0x6E       # Numpad .
VK_DIVIDE = 0x6F        # Numpad /

# Virtual Key Codes - Function Keys
VK_F1 = 0x70
VK_F2 = 0x71
VK_F3 = 0x72
VK_F4 = 0x73
VK_F5 = 0x74
VK_F6 = 0x75
VK_F7 = 0x76
VK_F8 = 0x77
VK_F9 = 0x78
VK_F10 = 0x79
VK_F11 = 0x7A
VK_F12 = 0x7B
VK_F13 = 0x7C
VK_F14 = 0x7D
VK_F15 = 0x7E
VK_F16 = 0x7F
VK_F17 = 0x80
VK_F18 = 0x81
VK_F19 = 0x82
VK_F20 = 0x83
VK_F21 = 0x84
VK_F22 = 0x85
VK_F23 = 0x86
VK_F24 = 0x87

# Virtual Key Codes - Lock Keys
VK_NUMLOCK = 0x90       # Num Lock
VK_SCROLL = 0x91        # Scroll Lock

# Virtual Key Codes - Shift Keys
VK_LSHIFT = 0xA0        # Left Shift
VK_RSHIFT = 0xA1        # Right Shift
VK_LCONTROL = 0xA2      # Left Control
VK_RCONTROL = 0xA3      # Right Control
VK_LMENU = 0xA4         # Left Alt
VK_RMENU = 0xA5         # Right Alt

# Virtual Key Codes - OEM Keys
VK_OEM_1 = 0xBA         # ';:' for US
VK_OEM_PLUS = 0xBB      # '+' any country
VK_OEM_COMMA = 0xBC     # ',' any country
VK_OEM_MINUS = 0xBD     # '-' any country
VK_OEM_PERIOD = 0xBE    # '.' any country
VK_OEM_2 = 0xBF         # '/?' for US
VK_OEM_3 = 0xC0         # '`~' for US
VK_OEM_4 = 0xDB         # '[{' for US
VK_OEM_5 = 0xDC         # '\|' for US
VK_OEM_6 = 0xDD         # ']}' for US
VK_OEM_7 = 0xDE         # '"\'' for US
VK_OEM_8 = 0xDF

# Character to VK code mapping for common characters
CHAR_TO_VK = {
    'a': VK_A, 'b': VK_B, 'c': VK_C, 'd': VK_D, 'e': VK_E, 'f': VK_F,
    'g': VK_G, 'h': VK_H, 'i': VK_I, 'j': VK_J, 'k': VK_K, 'l': VK_L,
    'm': VK_M, 'n': VK_N, 'o': VK_O, 'p': VK_P, 'q': VK_Q, 'r': VK_R,
    's': VK_S, 't': VK_T, 'u': VK_U, 'v': VK_V, 'w': VK_W, 'x': VK_X,
    'y': VK_Y, 'z': VK_Z,
    '0': VK_0, '1': VK_1, '2': VK_2, '3': VK_3, '4': VK_4,
    '5': VK_5, '6': VK_6, '7': VK_7, '8': VK_8, '9': VK_9,
    ' ': VK_SPACE, '\t': VK_TAB, '\n': VK_RETURN, '\r': VK_RETURN,
    ';': VK_OEM_1, '=': VK_OEM_PLUS, ',': VK_OEM_COMMA, '-': VK_OEM_MINUS,
    '.': VK_OEM_PERIOD, '/': VK_OEM_2, '`': VK_OEM_3, '[': VK_OEM_4,
    '\\': VK_OEM_5, ']': VK_OEM_6, "'": VK_OEM_7
}

# Characters that require shift key
SHIFT_CHARS = {
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+',
    '{', '}', '|', ':', '"', '<', '>', '?', '~'
}

# Shift character mappings
SHIFT_CHAR_MAP = {
    '!': '1', '@': '2', '#': '3', '$': '4', '%': '5', '^': '6',
    '&': '7', '*': '8', '(': '9', ')': '0', '_': '-', '+': '=',
    '{': '[', '}': ']', '|': '\\', ':': ';', '"': "'",
    '<': ',', '>': '.', '?': '/', '~': '`'
}