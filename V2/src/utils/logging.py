import logging
import sys
from pathlib import Path
from typing import Optional
from logging.handlers import RotatingFileHandler

class ColorFormatter(logging.Formatter):
    """Custom formatter adding colors to levelname field"""
    
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record):
        # Add colors to levelname
        record.levelname = (
            f"{self.COLORS.get(record.levelname, self.RESET)}"
            f"{record.levelname}{self.RESET}"
        )
        return super().format(record)

class LogManager:
    _instance: Optional['LogManager'] = None
    _logger: Optional[logging.Logger] = None
    
    def __init__(self):
        self._logger = logging.getLogger('L-oIRC-V2')
        self._setup_logging()
    
    def _setup_logging(self):
        # Set base logging level
        self._logger.setLevel(logging.DEBUG)
        
        # Create logs directory
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        
        # Console Handler
        console = logging.StreamHandler(sys.stdout)
        console.setLevel(logging.DEBUG)
        console_formatter = ColorFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console.setFormatter(console_formatter)
        
        # File Handler with rotation
        file_handler = RotatingFileHandler(
            log_dir / 'bot.log',
            maxBytes=10_000_000,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        
        # Add handlers
        self._logger.addHandler(console)
        self._logger.addHandler(file_handler)
    
    @classmethod
    def get_instance(cls) -> 'LogManager':
        if cls._instance is None:
            cls._instance = LogManager()
        return cls._instance
    
    def get_logger(self) -> logging.Logger:
        return self._logger

import traceback
from io import StringIO
def getTB():
    tb_stream = StringIO()
    traceback.print_exc(file=tb_stream)
    return tb_stream.getvalue()

# Global convenience function
def log(message: str, level: str = 'info') -> None:
    logger = LogManager.get_instance().get_logger()
    
    level_map = {
        'debug': logger.debug,
        'info': logger.info,
        'warning': logger.warning,
        'error': logger.error,
        'critical': logger.critical
    }
    
    log_func = level_map.get(level.lower(), logger.info)
    log_func(message)
