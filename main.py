
from selenium import webdriver;
# we will be using the this chrome service to be able to initialize the web browser 
from selenium.webdriver.chrome.service import Service;
from selenium.webdriver.common.by import By;
from selenium.webdriver.support.ui import WebDriverWait;
from selenium.webdriver.support import expected_conditions as expectedConditions;
import time;


service = Service(executable_path="/usr/bin/chromedriver");
# the following driver is the piece of software which will be going to control the chrome 
# this will not work until and unless the chrom Web driver is not installed for this purpose 
# and this will act as a real user 
# to make the following driver code works make sure to download the chrome driver 
driver = webdriver.Chrome(service=service);


# now we will grab the website 
driver.get("https://www.udemy.com/course/snowflake-masterclass/?couponCode=KEEPLEARNING");

# WRITING THE AUTOMATION CODE TO FETCH THE LAST UPDATED VALUE OF THE COURSE 
# first we have to wait for the element to get loaded first and then we will try to fetch the value for this purpose 
WebDriverWait(driver, 10).until(
    expectedConditions.presence_of_element_located((By.CLASS_NAME, "last-update-date"))
);

lastUpdatedCourseDate = driver.find_element(By.CLASS_NAME, "last-update-date").text;
print("The value of the last-update-date is " + lastUpdatedCourseDate, "\n\n");




driver.quit();



