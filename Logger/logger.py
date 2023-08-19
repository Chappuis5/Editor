import logging

class Logger:
    def __init__(self, log_file_name: str, log_level: int = logging.INFO):
        """
        Initialize the logger with file and console handlers.
        
        :param log_file_name: Name of the file to write logs to.
        :type log_file_name: str
        :param log_level: Logging level, defaults to logging.INFO.
        :type log_level: int
        """
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)

        # File Handler
        handler = logging.FileHandler(log_file_name)
        handler.setLevel(log_level)

        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)

        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add Handlers
        self.logger.addHandler(handler)
        self.logger.addHandler(console_handler)

    def write(self, message: str, level: str):
        """
        Write a log message at the specified log level.
        
        :param message: The message to log.
        :type message: str
        :param level: The logging level ('debug', 'info', 'warning', 'error', 'critical').
        :type level: str
        """
        if level.lower() == 'debug':
            self.logger.debug(message)
        elif level.lower() == 'info':
            self.logger.info(message)
        elif level.lower() == 'warning':
            self.logger.warning(message)
        elif level.lower() == 'error':
            self.logger.error(message)
        elif level.lower() == 'critical':
            self.logger.critical(message)
