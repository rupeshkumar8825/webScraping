import undetected_chromedriver as uc;
from selenium.webdriver.chrome.service import Service;
from selenium.webdriver.common.by import By;
from selenium.webdriver.support.ui import WebDriverWait;
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as expectedConditions;
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
import stringConstants as stringConstants




def InitializeChromeDriver():
    service = Service(executable_path="/usr/bin/chromedriver");
    driver = uc.Chrome(service=service);
    return driver;



def InitializeAutomationResultDict():
    automationResultDict = {}
    automationResultDict[stringConstants.CourseUpdateDate] = None
    automationResultDict[stringConstants.CourseSaleCount] = None
    automationResultDict[stringConstants.CourseReviewCount] = None
    automationResultDict[stringConstants.CourseRating] = None
    automationResultDict[stringConstants.CourseLength] = None
    automationResultDict[stringConstants.CourseLastUpdatedDate] = None

    return automationResultDict;






def UpdateAutomationResultInDataFrame(dataFrame, automationResultDict, currIndex):
    for column in dataFrame.columns:
        if(column == stringConstants.CourseURL or column == stringConstants.CourseType or column == "#" or column == stringConstants.InstructorName or column == stringConstants.CourseName):
            continue;
        dataFrame.at[currIndex, column] = automationResultDict[column]
   
    return;





def FetchDataByAutomation(wait, driver, automationResultDict, courseLink):
    driver.get(courseLink[0]);
    courseType = courseLink[1].strip();
    

    try: 
            
        # WRITING THE AUTOMATION CODE TO FETCH THE LAST UPDATED VALUE OF THE COURSE 
        wait.until(
            expectedConditions.presence_of_element_located((By.CLASS_NAME, "last-update-date"))
        );
        lastUpdatedCourseDate = driver.find_element(By.CLASS_NAME, "last-update-date").text;
        # parsing the result for this purpose 
        lastUpdatedCourseDate = "01/" + lastUpdatedCourseDate.split(" ")[2];
        automationResultDict[stringConstants.CourseLastUpdatedDate] = lastUpdatedCourseDate;
    except NoSuchElementException:
        print("ELEMENT NOT FOUND \n\n\n\n");
    except TimeoutException:
        print("TimeOut Occurred");

    try:
            
        #WRITING THE CODE TO FETCH THE VALUE OF COURSE SALE COUNT 
        wait.until(
            expectedConditions.presence_of_element_located((By.CLASS_NAME, "enrollment"))
        );
        courseSaleCount = driver.find_element(By.CLASS_NAME, "enrollments").text;
        # parsing the result here for this purpose (removing the comma into this for this purpose)
        parsedStringArray = courseSaleCount.split(" ");
        courseSaleCount = parsedStringArray[0];
        automationResultDict[stringConstants.CourseSaleCount] = courseSaleCount;
    except NoSuchElementException:
        print("ELEMENT NOT FOUND \n\n\n\n");
    except TimeoutException:
        print("TimeOut Occurred");


    try:
        
        #WRITING THE CODE TO FETCH THE COURSE REVIEW COUNT 
        wait.until(
            expectedConditions.presence_of_element_located((By.XPATH, "//div[contains(@class, 'clp-lead__element-item--row')]/a/span[2]"))
        );
        courseReviewCounts = driver.find_element(By.XPATH, "//div[contains(@class, 'clp-lead__element-item--row')]/a/span[2]").text;
        parseString = courseReviewCounts.split(" ")[0];
        courseReviewCounts = parseString.split("(")[1];
        automationResultDict[stringConstants.CourseReviewCount] = courseReviewCounts;
    except NoSuchElementException:
        print("ELEMENT NOT FOUND\n\n");
    except TimeoutException:
        print("TimeOut Occurred");

    try:

        #WRITING THE CODE TO FETCH THE COURSE RATING 
        wait.until(
            expectedConditions.presence_of_element_located((By.XPATH, "//div[contains(@class, 'clp-lead__element-item--row')]/a/span[1]/span[2]"))
        );
        courseRatings = driver.find_element(By.XPATH, "//div[contains(@class, 'clp-lead__element-item--row')]/a/span[1]/span[2]").text;
        automationResultDict[stringConstants.CourseRating] = courseRatings;
    except NoSuchElementException:
        print("ELEMENT NOT FOUND \n\n\n\n");
    except TimeoutException:
        print("TimeOut Occurred");



    try : 

        #CODE TO FETCH THE COURSEDURATION OR TOTAL NUMBER OF TESTS FOR THIS PURPOSE 
        if(courseType == stringConstants.PracticeTest):
            # then we have to fetch the value of the total number of questions in the test 
            wait.until(
                expectedConditions.presence_of_element_located((By.XPATH, "//div[contains(@data-purpose, 'curriculum-stats')]/span[1]"))
            );
            courseDuration = driver.find_element(By.XPATH, "//div[contains(@data-purpose, 'curriculum-stats')]/span[1]").text;
        elif(courseType == stringConstants.VideoCourse): 
            wait.until(
                expectedConditions.presence_of_element_located((By.XPATH, "//div[contains(@data-purpose, 'curriculum-stats')]/span[1]/span[1]"))
            );
            courseDuration = driver.find_element(By.XPATH, "//div[contains(@data-purpose, 'curriculum-stats')]/span[1]/span[1]").text;
        parsedStringArray = courseDuration.split(" ");
        courseDuration = parsedStringArray[0] + " " + parsedStringArray[1];
        automationResultDict[stringConstants.CourseLength] = courseDuration;
    except NoSuchElementException:
        print("ELEMENT NOT FOUND \n\n\n\n");
    except TimeoutException:
        print("TimeOut Occurred");