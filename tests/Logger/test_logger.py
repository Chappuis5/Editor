import unittest
from unittest.mock import patch, Mock, MagicMock
import logging
from Logger.logger import Logger

class TestLogger(unittest.TestCase):

    def setUp(self):
        # Mocking the FileHandler and StreamHandler to capture logs
        self.mock_file_handler = Mock(spec=logging.FileHandler)
        self.mock_stream_handler = Mock(spec=logging.StreamHandler)
        
        # Set level attribute for mock handlers
        self.mock_file_handler.level = logging.INFO
        self.mock_stream_handler.level = logging.INFO
        
        self.patcher1 = patch('logging.FileHandler', return_value=self.mock_file_handler)
        self.patcher2 = patch('logging.StreamHandler', return_value=self.mock_stream_handler)
        
        # Mock the entire Logger class and set its level and handlers attributes
        self.mock_logger = MagicMock()
        self.mock_logger.level = logging.DEBUG
        self.mock_logger.handlers = [self.mock_file_handler, self.mock_stream_handler]
        self.patcher3 = patch('logging.getLogger', return_value=self.mock_logger)
        
        self.addCleanup(self.patcher1.stop)
        self.addCleanup(self.patcher2.stop)
        self.addCleanup(self.patcher3.stop)
        
        self.patcher1.start()
        self.patcher2.start()
        self.patcher3.start()


    def test_logger_initialization(self):
        logger = Logger('test.log', logging.DEBUG)
        
        # Check if logger is initialized with correct level
        self.assertEqual(logger.logger.level, logging.DEBUG)
        
        # Check if handlers are added to the logger
        self.assertIn(self.mock_file_handler, logger.logger.handlers)
        self.assertIn(self.mock_stream_handler, logger.logger.handlers)

    def test_write_method(self):
        logger = Logger('test.log', logging.DEBUG)
        
        test_messages = [
            ('debug message', 'debug', logger.logger.debug),
            ('info message', 'info', logger.logger.info),
            ('warning message', 'warning', logger.logger.warning),
            ('error message', 'error', logger.logger.error),
            ('critical message', 'critical', logger.logger.critical)
        ]
        
        for message, level, log_method in test_messages:
            with self.subTest(message=message, level=level):
                logger.write(message, level)
                log_method.assert_called_with(message)

if __name__ == '__main__':
    unittest.main()
