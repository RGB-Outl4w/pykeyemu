"""Unit tests for PyKeyEmu module

This module contains comprehensive tests for all functionality in the PyKeyEmu library.
Tests are designed to run without actually sending input to avoid interfering with the system.
"""

import unittest
import time
from unittest.mock import patch, MagicMock

# Import the modules to test
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import constants
import utils
import wininput

class TestConstants(unittest.TestCase):
    """Test the constants module"""
    
    def test_vk_codes_are_integers(self):
        """Test that all VK codes are integers"""
        self.assertIsInstance(constants.VK_A, int)
        self.assertIsInstance(constants.VK_RETURN, int)
        self.assertIsInstance(constants.VK_SHIFT, int)
        self.assertIsInstance(constants.VK_CONTROL, int)
    
    def test_vk_codes_in_valid_range(self):
        """Test that VK codes are in valid range (0-255)"""
        test_codes = [
            constants.VK_A, constants.VK_Z, constants.VK_0, constants.VK_9,
            constants.VK_F1, constants.VK_F12, constants.VK_SHIFT, constants.VK_CONTROL
        ]
        
        for code in test_codes:
            self.assertGreaterEqual(code, 0)
            self.assertLessEqual(code, 255)
    
    def test_char_to_vk_mapping(self):
        """Test character to VK code mapping"""
        self.assertEqual(constants.CHAR_TO_VK['a'], constants.VK_A)
        self.assertEqual(constants.CHAR_TO_VK['z'], constants.VK_Z)
        self.assertEqual(constants.CHAR_TO_VK['0'], constants.VK_0)
        self.assertEqual(constants.CHAR_TO_VK['9'], constants.VK_9)
        self.assertEqual(constants.CHAR_TO_VK[' '], constants.VK_SPACE)
    
    def test_shift_chars_set(self):
        """Test shift characters set"""
        self.assertIn('A', constants.SHIFT_CHARS)
        self.assertIn('Z', constants.SHIFT_CHARS)
        self.assertIn('!', constants.SHIFT_CHARS)
        self.assertIn('@', constants.SHIFT_CHARS)
        self.assertNotIn('a', constants.SHIFT_CHARS)
        self.assertNotIn('1', constants.SHIFT_CHARS)
    
    def test_shift_char_mapping(self):
        """Test shift character mapping"""
        self.assertEqual(constants.SHIFT_CHAR_MAP['!'], '1')
        self.assertEqual(constants.SHIFT_CHAR_MAP['@'], '2')
        self.assertEqual(constants.SHIFT_CHAR_MAP['('], '9')
        self.assertEqual(constants.SHIFT_CHAR_MAP[')'], '0')

class TestUtils(unittest.TestCase):
    """Test the utils module"""
    
    def test_humanize_delay(self):
        """Test humanized delay generation"""
        # Test basic functionality
        delay = utils.humanize_delay(0.1, 0.02)
        self.assertGreaterEqual(delay, 0.08)
        self.assertLessEqual(delay, 0.12)
        
        # Test with zero variance
        delay = utils.humanize_delay(0.1, 0.0)
        self.assertEqual(delay, 0.1)
        
        # Test that result is never negative
        delay = utils.humanize_delay(0.01, 0.1)
        self.assertGreaterEqual(delay, 0.0)
    
    def test_humanize_delay_validation(self):
        """Test humanize_delay input validation"""
        with self.assertRaises(ValueError):
            utils.humanize_delay(-0.1, 0.02)
        
        with self.assertRaises(ValueError):
            utils.humanize_delay(0.1, -0.02)
    
    def test_validate_text(self):
        """Test text validation"""
        # Test valid text
        valid, unsupported = utils.validate_text("Hello World!")
        self.assertTrue(valid)
        self.assertEqual(len(unsupported), 0)
        
        # Test text with unsupported characters
        valid, unsupported = utils.validate_text("Hello 世界")
        self.assertFalse(valid)
        self.assertIn('世', unsupported)
        self.assertIn('界', unsupported)
        
        # Test empty string
        valid, unsupported = utils.validate_text("")
        self.assertTrue(valid)
        self.assertEqual(len(unsupported), 0)
    
    def test_validate_text_validation(self):
        """Test validate_text input validation"""
        with self.assertRaises(ValueError):
            utils.validate_text(123)
    
    def test_split_text_by_support(self):
        """Test text splitting by character support"""
        # Test mixed text
        chunks = utils.split_text_by_support("Hello 世界 World")
        self.assertEqual(len(chunks), 3)
        self.assertEqual(chunks[0], ("Hello ", True))
        self.assertEqual(chunks[1], ("世界", False))
        self.assertEqual(chunks[2], (" World", True))
        
        # Test all supported text
        chunks = utils.split_text_by_support("Hello World")
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0], ("Hello World", True))
        
        # Test empty string
        chunks = utils.split_text_by_support("")
        self.assertEqual(len(chunks), 0)
    
    def test_calculate_typing_time(self):
        """Test typing time calculation"""
        # Test basic calculation
        time_needed = utils.calculate_typing_time("Hello", 0.1)
        self.assertEqual(time_needed, 0.4)  # 4 delays for 5 characters
        
        # Test single character
        time_needed = utils.calculate_typing_time("A", 0.1)
        self.assertEqual(time_needed, 0.0)
        
        # Test empty string
        time_needed = utils.calculate_typing_time("", 0.1)
        self.assertEqual(time_needed, 0.0)
    
    def test_calculate_typing_time_validation(self):
        """Test calculate_typing_time input validation"""
        with self.assertRaises(ValueError):
            utils.calculate_typing_time(123, 0.1)
        
        with self.assertRaises(ValueError):
            utils.calculate_typing_time("Hello", -0.1)
    
    def test_normalize_line_endings(self):
        """Test line ending normalization"""
        # Test Windows to Unix
        result = utils.normalize_line_endings("Line1\r\nLine2\r\nLine3")
        self.assertEqual(result, "Line1\nLine2\nLine3")
        
        # Test Mac to Unix
        result = utils.normalize_line_endings("Line1\rLine2\rLine3")
        self.assertEqual(result, "Line1\nLine2\nLine3")
        
        # Test mixed to Windows
        result = utils.normalize_line_endings("Line1\nLine2\rLine3", "\r\n")
        self.assertEqual(result, "Line1\r\nLine2\r\nLine3")
    
    def test_escape_special_chars(self):
        """Test special character escaping"""
        result = utils.escape_special_chars("Hello\tWorld\n")
        self.assertEqual(result, "Hello\\tWorld\\n")
        
        result = utils.escape_special_chars("Line1\r\nLine2")
        self.assertEqual(result, "Line1\\r\\nLine2")
    
    def test_create_typing_profile(self):
        """Test typing profile creation"""
        # Test fast typist
        profile = utils.create_typing_profile(80)
        self.assertEqual(profile['wpm'], 80)
        self.assertIn('base_delay', profile)
        self.assertIn('variance', profile)
        self.assertGreater(profile['base_delay'], 0)
        
        # Test slow typist
        profile = utils.create_typing_profile(20)
        self.assertEqual(profile['wpm'], 20)
        self.assertGreater(profile['base_delay'], 0)
    
    def test_create_typing_profile_validation(self):
        """Test typing profile validation"""
        with self.assertRaises(ValueError):
            utils.create_typing_profile(0)
        
        with self.assertRaises(ValueError):
            utils.create_typing_profile(-10)
    
    def test_apply_typing_profile(self):
        """Test typing profile application"""
        profile = utils.create_typing_profile(60)
        delays = utils.apply_typing_profile("Hello", profile)
        
        self.assertEqual(len(delays), 5)  # 5 characters
        for delay in delays:
            self.assertGreater(delay, 0)

class TestWinInput(unittest.TestCase):
    """Test the wininput module
    
    Note: These tests mock the Windows API calls to avoid actually sending input.
    """
    
    def setUp(self):
        """Set up test fixtures"""
        # Mock the SendInput function
        self.send_input_patcher = patch('wininput.user32.SendInput')
        self.mock_send_input = self.send_input_patcher.start()
        self.mock_send_input.return_value = 1  # Success
    
    def tearDown(self):
        """Clean up test fixtures"""
        self.send_input_patcher.stop()
    
    def test_press_key(self):
        """Test key press functionality"""
        result = wininput.press_key(constants.VK_A)
        self.assertTrue(result)
        self.mock_send_input.assert_called_once()
    
    def test_press_key_validation(self):
        """Test press_key input validation"""
        with self.assertRaises(ValueError):
            wininput.press_key(-1)
        
        with self.assertRaises(ValueError):
            wininput.press_key(256)
        
        with self.assertRaises(ValueError):
            wininput.press_key("A")
    
    def test_release_key(self):
        """Test key release functionality"""
        result = wininput.release_key(constants.VK_A)
        self.assertTrue(result)
        self.mock_send_input.assert_called_once()
    
    def test_release_key_validation(self):
        """Test release_key input validation"""
        with self.assertRaises(ValueError):
            wininput.release_key(-1)
        
        with self.assertRaises(ValueError):
            wininput.release_key(256)
    
    def test_tap_key(self):
        """Test key tap functionality"""
        result = wininput.tap_key(constants.VK_A)
        self.assertTrue(result)
        self.mock_send_input.assert_called_once()
    
    def test_tap_key_with_modifiers(self):
        """Test key tap with modifiers"""
        result = wininput.tap_key(constants.VK_A, [constants.VK_CONTROL])
        self.assertTrue(result)
        self.mock_send_input.assert_called_once()
    
    def test_tap_key_validation(self):
        """Test tap_key input validation"""
        with self.assertRaises(ValueError):
            wininput.tap_key(-1)
        
        with self.assertRaises(ValueError):
            wininput.tap_key(constants.VK_A, [-1])
    
    @patch('wininput.time.sleep')
    def test_type_string(self, mock_sleep):
        """Test string typing functionality"""
        result = wininput.type_string("Hello", delay=0.1)
        self.assertTrue(result)
        
        # Should call SendInput for each character
        self.assertEqual(self.mock_send_input.call_count, 5)
        
        # Should call sleep for delays
        self.assertEqual(mock_sleep.call_count, 5)
    
    def test_type_string_validation(self):
        """Test type_string input validation"""
        with self.assertRaises(ValueError):
            wininput.type_string(123)
        
        with self.assertRaises(ValueError):
            wininput.type_string("Hello", delay=-0.1)
    
    def test_with_modifiers_context_manager(self):
        """Test with_modifiers context manager"""
        with wininput.with_modifiers([constants.VK_CONTROL]):
            wininput.tap_key(constants.VK_A)
        
        # Should have multiple SendInput calls (press modifier, tap key, release modifier)
        self.assertGreater(self.mock_send_input.call_count, 1)
    
    def test_with_modifiers_validation(self):
        """Test with_modifiers input validation"""
        with self.assertRaises(ValueError):
            with wininput.with_modifiers("invalid"):
                pass
        
        with self.assertRaises(ValueError):
            with wininput.with_modifiers([-1]):
                pass
    
    @patch('wininput.user32.GetAsyncKeyState')
    def test_is_key_pressed(self, mock_get_async_key_state):
        """Test key state checking"""
        # Mock key pressed
        mock_get_async_key_state.return_value = 0x8001
        result = wininput.is_key_pressed(constants.VK_A)
        self.assertTrue(result)
        
        # Mock key not pressed
        mock_get_async_key_state.return_value = 0x0000
        result = wininput.is_key_pressed(constants.VK_A)
        self.assertFalse(result)
    
    def test_is_key_pressed_validation(self):
        """Test is_key_pressed input validation"""
        with self.assertRaises(ValueError):
            wininput.is_key_pressed(-1)
        
        with self.assertRaises(ValueError):
            wininput.is_key_pressed(256)

class TestIntegration(unittest.TestCase):
    """Integration tests for the complete module"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Mock the SendInput function
        self.send_input_patcher = patch('wininput.user32.SendInput')
        self.mock_send_input = self.send_input_patcher.start()
        self.mock_send_input.return_value = 1  # Success
    
    def tearDown(self):
        """Clean up test fixtures"""
        self.send_input_patcher.stop()
    
    def test_import_main_module(self):
        """Test importing the main module"""
        import pykeyemu
        
        # Test that main functions are available
        self.assertTrue(hasattr(pykeyemu, 'press_key'))
        self.assertTrue(hasattr(pykeyemu, 'release_key'))
        self.assertTrue(hasattr(pykeyemu, 'tap_key'))
        self.assertTrue(hasattr(pykeyemu, 'type_string'))
        
        # Test that constants are available
        self.assertTrue(hasattr(pykeyemu, 'VK_A'))
        self.assertTrue(hasattr(pykeyemu, 'VK_RETURN'))
        self.assertTrue(hasattr(pykeyemu, 'VK_CONTROL'))
    
    @patch('wininput.time.sleep')
    def test_complete_workflow(self, mock_sleep):
        """Test a complete typing workflow"""
        import pykeyemu
        
        # Test typing a complete sentence
        result = pykeyemu.type_string("Hello, World!", delay=0.05)
        self.assertTrue(result)
        
        # Test key combination
        result = pykeyemu.tap_key(pykeyemu.VK_A, [pykeyemu.VK_CONTROL])
        self.assertTrue(result)
        
        # Verify SendInput was called multiple times
        self.assertGreater(self.mock_send_input.call_count, 10)

def run_tests():
    """Run all tests"""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_classes = [
        TestConstants,
        TestUtils,
        TestWinInput,
        TestIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()

if __name__ == '__main__':
    # Run tests when script is executed directly
    success = run_tests()
    exit(0 if success else 1)