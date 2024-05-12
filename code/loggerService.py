import logging

def InitializeLoggingService():
    logFilePath = "../output/logs/automationLog.log"
    
    log_format = "%(asctime)s - %(levelname)s - %(module)s - %(lineno)d - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    logging.basicConfig(format= log_format, datefmt=date_format, filename= logFilePath, level=logging.DEBUG)

    logger = logging.getLogger("appLogger")
    
    return logger;