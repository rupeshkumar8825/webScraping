import logging
from datetime import datetime




def InitializeLoggingService():

    logFilePath = f"../output/logs/automationLog_{datetime.now()}.log"
    
    log_format = "%(asctime)s - %(levelname)s - %(module)s - %(lineno)d - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    logging.basicConfig(format= log_format, datefmt=date_format, filename= logFilePath, level=logging.INFO)

    logger = logging.getLogger("appLogger")
    
    return logger;