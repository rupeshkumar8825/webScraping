
# from selenium import webdriver;
import undetected_chromedriver as uc;
from selenium.webdriver.chrome.service import Service;
from selenium.webdriver.common.by import By;
from selenium.webdriver.support.ui import WebDriverWait;
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as expectedConditions;
from selenium.webdriver.common.keys import Keys

import time;
import pandas as pd;
from random import randrange;


def InitializeChromeDriver():

    # options = Options()
    # options.add_argument("start-maximized")
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # options.add_experimental_option('useAutomationExtension', False)
    # options.add_argument('--disable-blink-features=AutomationControlled')
    service = Service(executable_path="/usr/bin/chromedriver");
    driver = uc.Chrome(service=service);
    return driver;


def ReadExcelSheet():
    filePath = "Template_competition_analytics.xlsx"
    df = pd.read_excel(filePath)
    return df;


def GetAllCourseLinks(currDataFrame):
    courseLinkList = []

    for currIndex, currRow in currDataFrame.iterrows():
        for column in currDataFrame.columns:
            if(column == "Course URL"):
                courseLinkList.append([currRow[column], currRow["Course Type"]]);

    return courseLinkList;



def InitializeAutomationResultDict():
    automationResultDict = {}
    automationResultDict["Update Date"] = ""
    automationResultDict["Course Sale Count"] = ""
    automationResultDict["Course Review Count"] = ""
    automationResultDict["Course Rating"] = ""
    automationResultDict["Course Length"] = ""
    automationResultDict["Course Last Updated Date"] = ""

    return automationResultDict;



def FetchDataByAutomation(wait, driver, automationResultDict, courseLink):
    # driver.find_element_b('body').send_keys(Keys.COMMAND + 't') 
    driver.get(courseLink[0]);
    courseType = courseLink[1].strip();
    print("The course type is \n", courseType);
    


    # WRITING THE AUTOMATION CODE TO FETCH THE LAST UPDATED VALUE OF THE COURSE 
    wait.until(
        expectedConditions.presence_of_element_located((By.CLASS_NAME, "last-update-date"))
    );
    lastUpdatedCourseDate = driver.find_element(By.CLASS_NAME, "last-update-date").text;
    print("The value of the last-update-date is " + lastUpdatedCourseDate, "\n\n");
    automationResultDict["Course Last Updated Date"] = lastUpdatedCourseDate;



    #WRITING THE CODE TO FETCH THE VALUE OF COURSE SALE COUNT 
    wait.until(
        expectedConditions.presence_of_element_located((By.CLASS_NAME, "enrollment"))
    );
    courseSaleCount = driver.find_element(By.CLASS_NAME, "enrollment").text;
    print("The value of the courseSaleCount is " + courseSaleCount, "\n\n");
    automationResultDict["Course Sale Count"] = courseSaleCount;

   
    #WRITING THE CODE TO FETCH THE COURSE REVIEW COUNT 
    wait.until(
        expectedConditions.presence_of_element_located((By.XPATH, "//div[contains(@class, 'clp-lead__element-item--row')]/a/span[2]"))
    );
    courseReviewCounts = driver.find_element(By.XPATH, "//div[contains(@class, 'clp-lead__element-item--row')]/a/span[2]").text;
    print("The value of the courseReviewCounts is " + courseReviewCounts, "\n\n\n\n");
    automationResultDict["Course Review Count"] = courseReviewCounts;



    #WRITING THE CODE TO FETCH THE COURSE RATING 
    wait.until(
        expectedConditions.presence_of_element_located((By.XPATH, "//div[contains(@class, 'clp-lead__element-item--row')]/a/span[1]/span[2]"))
    );
    courseRatings = driver.find_element(By.XPATH, "//div[contains(@class, 'clp-lead__element-item--row')]/a/span[1]/span[2]").text;
    print("The value of courseRatings is: " + courseRatings, "\n\n\n\n");
    automationResultDict["Course Rating"] = courseRatings;




    #CODE TO FETCH THE COURSEDURATION OR TOTAL NUMBER OF TESTS FOR THIS PURPOSE 
    if(courseType == "Practice Test"):
        # then we have to fetch the value of the total number of questions in the test 
        wait.until(
            expectedConditions.presence_of_element_located((By.XPATH, "//div[contains(@data-purpose, 'curriculum-stats')]/span[1]"))
        );
        courseDuration = driver.find_element(By.XPATH, "//div[contains(@data-purpose, 'curriculum-stats')]/span[1]").text;
    elif(courseType == "Video Course"): 
        wait.until(
            expectedConditions.presence_of_element_located((By.XPATH, "//div[contains(@data-purpose, 'curriculum-stats')]/span[1]/span[1]"))
        );
        courseDuration = driver.find_element(By.XPATH, "//div[contains(@data-purpose, 'curriculum-stats')]/span[1]/span[1]").text;

    # driver.close();
    print("The value of courseDuration is " + courseDuration);
    automationResultDict["Course Length"] = courseDuration;




def UpdateAutomationResultInDataFrame(dataFrame, automationResultDict, currIndex):
    print("The value of the currentIndex is as follows \n\n", currIndex);
    # using the for loop for this purpose 
    for column in dataFrame.columns:
        if(column == "Course URL" or column == "Course Type" or column == "#" or column == "Name" or column == "Course Name"):
            continue;
        dataFrame.at[currIndex, column] = automationResultDict[column]
    # for column in dataFrame.columns:
    #     print(column);

    # say everything went fine 
    return;



def PrintDataFrameValue(dataFrame):
    # using the for loop for this purpose 
    for row in dataFrame.iterrows():
        print(row);



def StoreResultIntoExcel(dataFrame):
    dataFrame.to_excel("OutputFile.xlsx", index = False)
    # say everything went fine 
    return;


def main():
    driver = InitializeChromeDriver()
    dataFrame = ReadExcelSheet()
    courseLinkList = GetAllCourseLinks(dataFrame)
    wait = WebDriverWait(driver, 10);


    for currIndex,  courseLink in enumerate(courseLinkList):
        automationResultDict = InitializeAutomationResultDict()
        waitTime = randrange(10);
        print("Waiting for ", waitTime);
        time.sleep(waitTime);
        FetchDataByAutomation(wait, driver, automationResultDict, courseLink)
        waitTime = randrange(10);
        print("Waiting for ", waitTime);
        time.sleep(waitTime);
        print("The final result of the automation runned for courseLink is as follows: \n\n", automationResultDict);
        # driver.close();

        # here we have to update the value of the dataFrame with whatever results we have got for this purpose 
        UpdateAutomationResultInDataFrame(dataFrame, automationResultDict, currIndex)
        # print("PRINTING THE UPDATED VALUE OF THE DATAFRAME FOR THIS PURPOSE \n\n");
        # PrintDataFrameValue(dataFrame);
        # break;

    # after this we have to store these values inside the new excel sheet for this purpose 
    StoreResultIntoExcel(dataFrame);
    driver.quit();
    return;



if __name__ == "__main__":
    main()