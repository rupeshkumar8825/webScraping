
# from selenium import webdriver;
import undetected_chromedriver as uc;
from selenium.webdriver.chrome.service import Service;
from selenium.webdriver.common.by import By;
from selenium.webdriver.support.ui import WebDriverWait;
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as expectedConditions;
from selenium.webdriver.common.keys import Keys
import automationService as automationService;
import excelService as excelService;
import pandas as pd;
import stringConstants as stringConstants;

from random import randrange;




def GetAllCourseLinks(currDataFrame):
    courseLinkList = []

    for currIndex, currRow in currDataFrame.iterrows():
        for column in currDataFrame.columns:
            if(column == stringConstants.CourseURL):
                courseLinkList.append([currRow[column], currRow[stringConstants.CourseType]]);

    return courseLinkList;








def main():
    driver = automationService.InitializeChromeDriver()
    dataFrame = excelService.ReadExcelSheet()

    dataFrame[stringConstants.CourseUpdateDate] = dataFrame[stringConstants.CourseUpdateDate].astype(str)
    dataFrame[stringConstants.CourseSaleCount] = dataFrame[stringConstants.CourseSaleCount].astype(str)
    dataFrame[stringConstants.CourseReviewCount] = dataFrame[stringConstants.CourseReviewCount].astype(str)
    dataFrame[stringConstants.CourseRating] = dataFrame[stringConstants.CourseRating].astype(str)
    dataFrame[stringConstants.CourseLength] = dataFrame[stringConstants.CourseLength].astype(str)
    dataFrame[stringConstants.CourseLastUpdatedDate] = dataFrame[stringConstants.CourseLastUpdatedDate].astype(str)



    courseLinkList = GetAllCourseLinks(dataFrame)
    wait = WebDriverWait(driver, 10);


    for currIndex,  courseLink in enumerate(courseLinkList):
        automationResultDict = automationService.InitializeAutomationResultDict()
        automationService.FetchDataByAutomation(wait, driver, automationResultDict, courseLink)
        automationService.UpdateAutomationResultInDataFrame(dataFrame, automationResultDict, currIndex)
        print("the final result after running the automation is as follows \n", automationResultDict);


    excelService.StoreResultIntoExcel(dataFrame);

    driver.quit();

    return;



if __name__ == "__main__":
    main()