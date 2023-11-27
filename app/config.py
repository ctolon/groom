from pathlib import Path
import logging
from enum import Enum

from utils import grpc_service_conf_generator

PARRENT_DIR = Path(__file__).parent
"""Top Level Directory of the project."""

class SingletonType(type):
    """Singleton Type Class."""
    
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class GRPCServerTypes(str, Enum):
    """GRPC Server Types."""
    
    SYNC = 'SYNC'
    ASYNC = 'ASYNC'

class Settings:
    """GRPC Server Settings"""
    
    PROJECT_NAME = "gRPC"
    GRPC_HOST="[::]"
    GRPC_PORT="50049"
    WORKER=20
    GRPC_SERVER_OPTS=[
        ('grpc.max_send_message_length', 100 * 1024 * 1024),
        ('grpc.max_receive_message_length', 100 * 1024 * 1024),
        ('grpc.service_config', grpc_service_conf_generator())
        ]
    LOG_LEVEL="INFO"
    LOG_DATEFMT="%Y-%m-%d %H:%M:%S"
    LOG_FORMAT="[%(levelname)s] %(asctime)s - %(message)s"
    TF_CPP_MIN_LOG_LEVEL="3" # 0,1,2,3
    
class GRPCLogger(object, metaclass=SingletonType):
    """GRPC Server Logger Configuration."""
    
    _logger = None
    
    def __init__(
        self,
        logger_name="ner_grpc",
        add_file_handler=False,
        add_stream_handler=True
        ):
    
        self._logger = logging.getLogger(logger_name)
        self._logger.setLevel(settings.LOG_LEVEL)
        formatter = logging.Formatter(settings.LOG_FORMAT, settings.LOG_DATEFMT)
        
        # Add File Handler
        if add_file_handler:
            log_path = PARRENT_DIR / "logs"
            if not Path(log_path).exists():
                Path(log_path).mkdir(exist_ok=True)
            log_file_path = str(log_path / logger_name + ".log")
            fileHandler = logging.FileHandler(filename=log_file_path, mode="a", encoding="utf-8")
            fileHandler.setFormatter(formatter)
            self._logger.addHandler(fileHandler)
        
        # Add Stream Handler
        if add_stream_handler:
            streamHandler = logging.StreamHandler()
            streamHandler.setFormatter(formatter)
            self._logger.addHandler(streamHandler)
        
        self._logger.info("{} Logger initialized as singleton.".format(logger_name))
        
    @property
    def get_logger(self) -> logging.Logger:
        logger = self._logger
        if logger is None:
            raise Exception("Logger not initialized yet.")
        
        return logger
    
# Initialize Settings and Logger as Singleton
settings = Settings()
logger = GRPCLogger().get_logger