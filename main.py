# hi this is sample project for webscraping and basically this is for my first freelancing project 

from selenium import webdriver;
# we will be using the this chrome service to be able to initialize the web browser 
from selenium.webdriver.chrome.service import Service;
from selenium.webdriver.common.by import By;
import time;


service = Service(executable_path="/usr/bin/chromedriver");
# the following driver is the piece of software which will be going to control the chrome 
# this will not work until and unless the chrom Web driver is not installed for this purpose 
# and this will act as a real user 
# to make the following driver code works make sure to download the chrome driver 
driver = webdriver.Chrome(service=service);


# now we will grab the website 
driver.get("https://www.udemy.com/course/snowflake-masterclass/?couponCode=KEEPLEARNING");

time.sleep(10); 

driver.quit();



