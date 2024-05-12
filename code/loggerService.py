import logging
from datetime import date 




def InitializeLoggingService():

    logFilePath = f"../output/logs/automationLog_{date.today()}.log"
    
    log_format = "%(asctime)s - %(levelname)s - %(module)s - %(lineno)d - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    logging.basicConfig(format= log_format, datefmt=date_format, filename= logFilePath, level=logging.DEBUG)

    logger = logging.getLogger("appLogger")
    
    return logger;