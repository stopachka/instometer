import logging
from logging.handlers import RotatingFileHandler

FORMAT = "%(message)s"


log_file_path = "log.txt"
max_file_size_bytes = 10 * 1024 * 1024 # 10 MB
backup_count = 2 
rotating_handler = RotatingFileHandler(
    log_file_path, 
    maxBytes=max_file_size_bytes, 
    backupCount=backup_count
)

logging.basicConfig(
    level="NOTSET", 
    format=FORMAT, 
    datefmt="[%X]", 
    handlers=[rotating_handler]
)

log = logging.getLogger("main")
