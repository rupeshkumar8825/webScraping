import pandas as pd


def ReadExcelSheet():
    filePath = "../data/Template_competition_analytics.xlsx"
    df = pd.read_excel(filePath)
    return df;



def PrintDataFrameValue(dataFrame):
    for row in dataFrame.iterrows():
        print(row);



def StoreResultIntoExcel(dataFrame):
    dataFrame.to_excel("../output/OutputFile.xlsx", index = False)
    # say everything went fine 
    return;
