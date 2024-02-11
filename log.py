import logging

FORMAT = "%(message)s"
logging.basicConfig(
    filename="log.txt",
    filemode="w",
    level="NOTSET", 
    format=FORMAT, 
    datefmt="[%X]", 
)

log = logging.getLogger("main")
