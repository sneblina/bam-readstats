import unittest
import logging
import os
import shutil
from read_stats.logging_config import setup_logger

# Define a directory for test logs
TEST_LOG_DIR = "test_logs"
DEFAULT_LOG_FILE_BASE = "bamreadstats" # Default from setup_logger

class TestSetupLogger(unittest.TestCase):
    """Test suite for the setup_logger function."""

    def setUp(self):
        """Set up for each test."""
        # Ensure the test log directory is clean before each test
        if os.path.exists(TEST_LOG_DIR):
            shutil.rmtree(TEST_LOG_DIR)
        os.makedirs(TEST_LOG_DIR)
        # Reset logging state for a specific logger to avoid interference between tests
        logging.getLogger("test_logger").handlers = []

    def test_logger_instance(self):
        """Test that setup_logger returns a Logger instance."""
        logger = setup_logger("test_logger", log_dir=TEST_LOG_DIR)
        self.assertIsInstance(logger, logging.Logger)

    def test_log_directory_creation(self):
        """Test that the log directory is created."""
        new_log_dir = os.path.join(TEST_LOG_DIR, "specific_test_dir")
        self.assertFalse(os.path.exists(new_log_dir))
        setup_logger("test_logger", log_dir=new_log_dir)
        self.assertTrue(os.path.exists(new_log_dir))

    def test_log_file_creation_default_name(self):
        """Test log file creation with the default file name."""
        logger_name = "test_logger"
        setup_logger(logger_name, log_dir=TEST_LOG_DIR)
        expected_log_file = os.path.join(TEST_LOG_DIR, f"{DEFAULT_LOG_FILE_BASE}.log")
        self.assertTrue(os.path.exists(expected_log_file))

    def test_log_file_creation_custom_name(self):
        """Test log file creation with a custom file name."""
        logger_name = "custom_test_logger"
        log_file_base = "custom_log"
        setup_logger(logger_name, log_dir=TEST_LOG_DIR, log_file=log_file_base)
        expected_log_file = os.path.join(TEST_LOG_DIR, f"{log_file_base}.log")
        self.assertTrue(os.path.exists(expected_log_file))

    def test_logging_level(self):
        """Test that the logger and handler are set to the specified level."""
        logger = setup_logger("test_logger", log_dir=TEST_LOG_DIR, level=logging.DEBUG)
        self.assertEqual(logger.level, logging.DEBUG)
        self.assertTrue(len(logger.handlers) > 0)
        # Ensure all handlers attached by setup_logger are at the correct level
        for handler in logger.handlers:
            if isinstance(handler, logging.FileHandler): # Check it's the one we added
                self.assertEqual(handler.level, logging.DEBUG)

    def test_log_formatting(self):
        """Test the log message format."""
        logger_name = "test_logger"
        logger = setup_logger(logger_name, log_dir=TEST_LOG_DIR, level=logging.INFO)
        
        test_message = "This is a test log message."
        logger.info(test_message)

        log_file_path = os.path.join(TEST_LOG_DIR, f"{DEFAULT_LOG_FILE_BASE}.log")
        
        # Ensure the log file was actually written to
        self.assertTrue(os.path.exists(log_file_path) and os.path.getsize(log_file_path) > 0)

        with open(log_file_path, 'r') as f:
            log_content = f.read()
        
        # Example: 2023-10-26 10:00:00,123 - test_logger - INFO - This is a test log message.
        # We will check for key components rather than exact time matching.
        self.assertIn(logger_name, log_content)
        self.assertIn("INFO", log_content)
        self.assertIn(test_message, log_content)
        # A more robust check could involve regex for the date-time part
        self.assertRegex(log_content, r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} - .*")


    def test_no_duplicate_handlers(self):
        """Test that calling setup_logger multiple times does not add duplicate handlers."""
        logger_name = "test_logger"
        logger = setup_logger(logger_name, log_dir=TEST_LOG_DIR)
        initial_handler_count = len(logger.handlers)
        # Call setup_logger again for the same logger
        logger_again = setup_logger(logger_name, log_dir=TEST_LOG_DIR)
        self.assertEqual(len(logger_again.handlers), initial_handler_count)
        # Specifically, check that only one FileHandler is present (or the expected number)
        file_handler_count = sum(isinstance(h, logging.FileHandler) for h in logger_again.handlers)
        self.assertEqual(file_handler_count, 1)


    def test_log_propagation_disabled(self):
        """Test that log propagation is disabled."""
        logger = setup_logger("test_logger", log_dir=TEST_LOG_DIR)
        self.assertFalse(logger.propagate)

if __name__ == '__main__':
    unittest.main()
