import pandas as pd
import os 
import loggerService as loggerService
from datetime import datetime

def ReadExcelSheet():
    filePath = "../data/Template_competition_analytics.xlsx"
    df = pd.read_excel(filePath)
    return df;



def PrintDataFrameValue(dataFrame):
    for row in dataFrame.iterrows():
        print(row);



def StoreResultIntoExcel(dataFrame, logger):
    logger.info("Store result in Excel -- Started");
    currDateTime = datetime.now();
    formatted_date = currDateTime.strftime("%Y-%m-%d_%H-%M-%S")
    output_dir = "../output";
    os.makedirs(output_dir, exist_ok=True)
    excelFilePath = os.path.join(output_dir, f"Competition_analytics_result_{formatted_date}.xlsx");
    dataFrame.to_excel(excelFilePath, index = False)

    logger.info("Store result in Excel -- Done");
    # say everything went fine 
    return;
