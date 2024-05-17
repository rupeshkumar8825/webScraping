import logging
from datetime import datetime



def InitializeLoggingService():
    currDateTime = datetime.now();
    currDateTime = currDateTime.isoformat(sep="_")
    logFilePath = f"../output/logs/automationLog_{currDateTime}.log"
    
    log_format = "%(asctime)s - %(levelname)s - %(module)s - %(lineno)d - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    logging.info("root") # call to info too early
    logging.basicConfig(format= log_format, datefmt=date_format, filename= logFilePath, level=logging.INFO)

    logger = logging.getLogger("appLogger")
    
    return logger;