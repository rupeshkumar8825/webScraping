import os
import logging
from datetime import datetime



def InitializeLoggingService():
    currDateTime = datetime.now();
    formatted_date = currDateTime.strftime("%Y-%m-%d_%H-%M-%S")
    
    output_dir = "../output/logs";
    os.makedirs(output_dir, exist_ok=True)
    logFilePath = os.path.join(output_dir, f"Competition_analytics_logs_{formatted_date}.log");

    log_format = "%(asctime)s - %(levelname)s - %(module)s - %(lineno)d - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    logging.info("root") # call to info too early
    logging.basicConfig(format= log_format, datefmt=date_format, filename= logFilePath, level=logging.INFO, force=True)

    logger = logging.getLogger("appLogger")
    
    return logger;