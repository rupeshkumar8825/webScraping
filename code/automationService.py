import undetected_chromedriver as uc;
from selenium.webdriver.chrome.service import Service;
from selenium.webdriver.common.by import By;
from selenium.webdriver.support.ui import WebDriverWait;
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as expectedConditions;
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
import stringConstants as stringConstants
import loggerService as loggerService
from enum import Enum
from datetime import datetime



# Define the enumeration for months
class Month(Enum):
    Jan = 1
    Feb = 2
    Mar = 3
    Apr = 4
    May = 5
    Jun = 6
    Jul = 7
    Aug = 8
    Sep = 9
    Oct = 10
    Nov = 11
    Dec = 12


# Define a function to get the month name from the month number
def get_month_name(month_number):
    try:
        return Month(month_number).name
    except ValueError:
        return "Invalid month number"


def InitializeChromeDriver(logger):
    logger.info("Driver Initialization -- Started")

    # service = Service(executable_path="/usr/bin/chromedriver");
    # uc.TARGET_VERSION = 124
    driver = uc.Chrome(version_main=124);

    logger.info("Driver Initialization -- Done")
    return driver;



def InitializeAutomationResultDict(logger):
    
    automationResultDict = {}
    automationResultDict[stringConstants.CourseUpdateDate] = None
    automationResultDict[stringConstants.CourseSaleCount] = None
    automationResultDict[stringConstants.CourseReviewCount] = None
    automationResultDict[stringConstants.CourseRating] = None
    automationResultDict[stringConstants.CourseLength] = None
    automationResultDict[stringConstants.CourseLastUpdatedDate] = None

    logger.info('automationResultDict Initialization Done');

    return automationResultDict;






def UpdateAutomationResultInDataFrame(dataFrame, automationResultDict, currIndex):
    for column in dataFrame.columns:
        if(column == stringConstants.CourseURL or column == stringConstants.CourseType or column == "#" or column == stringConstants.InstructorName or column == stringConstants.CourseName):
            continue;
        dataFrame.at[currIndex, column] = automationResultDict[column]
    
    # print("the finale value of the automation result is as follows \n\n\n",automationResultDict);
    # print("\n\n\n");
    return;





def FetchDataByAutomation(wait, driver, automationResultDict, courseLink, currCourseName, logger):
    logger.info(f"Automation Started for {currCourseName}\n\n")

    driver.get(courseLink[0]);
    courseType = courseLink[1].strip();
    

    # WRITING THE AUTOMATION CODE TO FETCH THE LAST UPDATED VALUE OF THE COURSE 
    try:

        logger.info(f"GET {stringConstants.CourseLastUpdatedDate} -- STARTED\n")        
        wait.until(
            expectedConditions.presence_of_element_located((By.CLASS_NAME, "last-update-date"))
        );
        lastUpdatedCourseDate = driver.find_element(By.CLASS_NAME, "last-update-date").text;
        # parsing the result for this purpose 
        splitLastUpdatedCourseDate = lastUpdatedCourseDate.split(" ")[2];
        monthInNumber = splitLastUpdatedCourseDate.split("/")[0];
        year = splitLastUpdatedCourseDate.split("/")[1];
        monthInString = get_month_name(int(monthInNumber));
        lastUpdatedCourseDate = "01-" + monthInString + f"-{year}";
        automationResultDict[stringConstants.CourseLastUpdatedDate] = lastUpdatedCourseDate;
        logger.info(f"GET  {stringConstants.CourseLastUpdatedDate} -- SUCCESS\n\n")

    except NoSuchElementException as e:
        logger.error("An NoSuchEelementException occurred : %s", str(e), exc_info=True)
    except TimeoutException as e:
        logger.exception("An TimeoutException occurred : %s", str(e), exc_info=True)
    except Exception as e:
        logger.error("An unknown Exception occurred %s", str(e), exc_info=True)




    #WRITING THE CODE TO FETCH THE VALUE OF COURSE SALE COUNT 
    try:
        logger.info(f"GET {stringConstants.CourseSaleCount} -- STARTED\n")
        wait.until(
            expectedConditions.presence_of_element_located((By.CLASS_NAME, "enrollment"))
        );
        courseSaleCount = driver.find_element(By.CLASS_NAME, "enrollment").text;
        # parsing the result here for this purpose (removing the comma into this for this purpose)
        parsedStringArray = courseSaleCount.split(" ");
        courseSaleCount = parsedStringArray[0];
        automationResultDict[stringConstants.CourseSaleCount] = courseSaleCount;

        logger.info(f"GET {stringConstants.CourseSaleCount} -- SUCCESS\n\n")

    except NoSuchElementException as e:
        logger.error("An NoSuchEelementException occurred : %s", str(e), exc_info=True)
    except TimeoutException as e:
        logger.exception("An TimeoutException occurred : %s", str(e), exc_info=True)
    except Exception as e:
        logger.error("An unknown Exception occurred %s", str(e), exc_info=True)




    #WRITING THE CODE TO FETCH THE COURSE REVIEW COUNT 
    try:
        logger.info(f"GET {stringConstants.CourseReviewCount} -- STARTED\n")
        
        wait.until(
            expectedConditions.presence_of_element_located((By.XPATH, "//div[contains(@class, 'clp-lead__element-item--row')]/a/span[2]"))
        );
        courseReviewCounts = driver.find_element(By.XPATH, "//div[contains(@class, 'clp-lead__element-item--row')]/a/span[2]").text;
        parseString = courseReviewCounts.split(" ")[0];
        courseReviewCounts = parseString.split("(")[1];
        automationResultDict[stringConstants.CourseReviewCount] = courseReviewCounts;

        logger.info(f"GET  {stringConstants.CourseReviewCount} -- SUCCESS\n\n")

    except NoSuchElementException as e:
        logger.error("An NoSuchEelementException occurred : %s", str(e), exc_info=True)
    except TimeoutException as e:
        logger.exception("An TimeoutException occurred : %s", str(e), exc_info=True)
    except Exception as e:
        logger.error("An unknown Exception occurred %s", str(e), exc_info=True)




    #WRITING THE CODE TO FETCH THE COURSE RATING 
    try:
        logger.info(f"GET {stringConstants.CourseRating} -- STARTED\n")

        wait.until(
            expectedConditions.presence_of_element_located((By.XPATH, "//div[contains(@class, 'clp-lead__element-item--row')]/a/span[1]/span[2]"))
        );
        courseRatings = driver.find_element(By.XPATH, "//div[contains(@class, 'clp-lead__element-item--row')]/a/span[1]/span[2]").text;
        automationResultDict[stringConstants.CourseRating] = courseRatings;

        logger.info(f"GET  {stringConstants.CourseRating} -- SUCCESS\n\n")

    except NoSuchElementException as e:
        logger.error("An NoSuchEelementException occurred : %s", str(e), exc_info=True)
    except TimeoutException as e:
        logger.exception("An TimeoutException occurred : %s", str(e), exc_info=True)
    except Exception as e:
        logger.error("An unknown Exception occurred %s", str(e), exc_info=True)




    #CODE TO FETCH THE COURSEDURATION OR TOTAL NUMBER OF TESTS FOR THIS PURPOSE 
    try : 

        logger.info(f"GET {stringConstants.CourseLength} -- STARTED\n")

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

        logger.info(f"GET  {stringConstants.CourseLength} -- SUCCESS\n\n")

    except NoSuchElementException as e:
        logger.error("An NoSuchEelementException occurred : %s", str(e), exc_info=True)
    except TimeoutException as e:
        logger.exception("An TimeoutException occurred : %s", str(e), exc_info=True)
    except Exception as e:
        logger.error("An unknown Exception occurred %s", str(e), exc_info=True)

    currDateTime = datetime.now().date();
    currDate = currDateTime.day;
    currMonthInNumbers = currDateTime.month;
    currYear = currDateTime.year;
    currMonthInWords = get_month_name(int(currMonthInNumbers));
    automationResultDict[stringConstants.CourseUpdateDate] =  f"{currDate}-{currMonthInWords}-{currYear}"

    logger.info(f"Automation Ended for {currCourseName}\n\n\n")
    return;





