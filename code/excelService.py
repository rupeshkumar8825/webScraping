import pandas as pd
import loggerService as loggerService

def ReadExcelSheet():
    filePath = "../data/Template_competition_analytics.xlsx"
    df = pd.read_excel(filePath)
    return df;



def PrintDataFrameValue(dataFrame):
    for row in dataFrame.iterrows():
        print(row);



def StoreResultIntoExcel(dataFrame, logger):
    logger.info("Store result in Excel -- Started");

    dataFrame.to_excel("../output/OutputFile.xlsx", index = False)

    logger.info("Store result in Excel -- Done");
    # say everything went fine 
    return;
