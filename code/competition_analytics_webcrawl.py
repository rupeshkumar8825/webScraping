
# from selenium import webdriver;
import undetected_chromedriver as uc;
from selenium.webdriver.chrome.service import Service;
from selenium.webdriver.common.by import By;
from selenium.webdriver.support.ui import WebDriverWait;
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as expectedConditions;
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
import automationService as automationService;
import excelService as excelService;
import pandas as pd;
import stringConstants as stringConstants;
import loggerService as loggerService
from datetime import date
from enum import Enum


from random import randrange;


logger = None;



def GetAllCourseLinks(currDataFrame):
    courseLinkList = []

    for currIndex, currRow in currDataFrame.iterrows():
        for column in currDataFrame.columns:
            if(column == stringConstants.CourseURL):
                courseLinkList.append([currRow[column], currRow[stringConstants.CourseType]]);

    return courseLinkList;




def GetAllCourseNames(currDataFrame):
    courseNameList = []
    for currIndex, currRow in currDataFrame.iterrows():
        for column in currDataFrame.columns:
            if(column == stringConstants.CourseName):
                courseNameList.append(currRow[column])

    return courseNameList;






def main():
    try:
        print("started ")
        logger = loggerService.InitializeLoggingService();
        driver = automationService.InitializeChromeDriver(logger)
        dataFrame = excelService.ReadExcelSheet()
        dataFrame[stringConstants.CourseUpdateDate] = dataFrame[stringConstants.CourseUpdateDate].astype(str)
        dataFrame[stringConstants.CourseSaleCount] = dataFrame[stringConstants.CourseSaleCount].astype(str)
        dataFrame[stringConstants.CourseReviewCount] = dataFrame[stringConstants.CourseReviewCount].astype(str)
        dataFrame[stringConstants.CourseRating] = dataFrame[stringConstants.CourseRating].astype(str)
        dataFrame[stringConstants.CourseLength] = dataFrame[stringConstants.CourseLength].astype(str)
        dataFrame[stringConstants.CourseLastUpdatedDate] = dataFrame[stringConstants.CourseLastUpdatedDate].astype(str)


        courseLinkList = GetAllCourseLinks(dataFrame)
        courseNameList = GetAllCourseNames(dataFrame)
        # print("the value of the list of courseName is as follows \n", courseNameList)
        wait = WebDriverWait(driver, 15);


        for currIndex,  courseLink in enumerate(courseLinkList):
            automationResultDict = automationService.InitializeAutomationResultDict(logger)
            currCourseName = courseNameList[currIndex];
            # if(currCourseName == None or courseLink == None):
            #     continue;
            try:
                automationService.FetchDataByAutomation(wait, driver, automationResultDict, courseLink, currCourseName, logger)
            except Exception as e:
                logger.error("An Unknown Exception occurred %s", str(e), exc_info=True);
                logger.info(f"Automation Ended for {currCourseName}\n\n\n")
                continue;    
            automationService.UpdateAutomationResultInDataFrame(dataFrame, automationResultDict, currIndex)

        # the final value of the dataframe is as follows : 
        excelService.StoreResultIntoExcel(dataFrame, logger);
    except WebDriverException as e:
        logger.error("An WebDriverException occurred %s", str(e), exc_info=True)
    except Exception as e:
        logger.error("An Unknown Exception occurred %s", str(e), exc_info=True)
    finally : 
        logger.info("Quiting the chrome driver.")
        driver.quit();

    return;


if __name__ == "__main__":
    main()

