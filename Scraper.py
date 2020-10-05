from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import re
import json
import time
import parameters

def initialize_driver(debugMode=False):
    try:
        chrome_options = Options()
        if debugMode == True:
            # chrome_options.add_argument("--log-level=3")
            # When driver is global it is prevented from being garbage collected, so the chrome window stays open
            global driver 

        else:
            chrome_options.add_argument("--headless")

        driver = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)
        return driver

        # #chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--disable-gpu")
        # #may fix odd crashing bug
        # chrome_options.add_argument("--no-sandbox")
        # #disables most logging
        # chrome_options.add_argument("--log-level=3")
        # chrome_options.add_argument("--allow-running-insecure-content")
        # #chrome_options.add_argument("--remote-debugging-port=9222") #http://localhost:9222
        # prefs = {"profile.managed_default_content_settings.images": 2}
        # chrome_options.add_experimental_option("prefs", prefs)
        # driver = webdriver.Chrome(executable_path="chromedriver.exe",options=chrome_options)
    except Exception as e:
        print(f"Exception:{e} occured, unable to initialize chrome")
        #input("press enter to exit")
        pass

def navigate_to_url(driver, url, debugMode=False):
    try: 
        print(f"navigating to url: {url}")
        #size and position the window appropriately
        # driver.set_window_size(300,1050)
        # driver.set_window_position(0,0)
        driver.get(url)
        return driver
    except Exception as e:
            print(f"Exception:{e} occured, unable to initialize user window")
            pass


def glassdoor_login_procedure(driver):
    driver.find_element_by_id("userEmail").send_keys(parameters.parameters.get("username"))
    driver.find_element_by_id("userPassword").send_keys(parameters.parameters.get("password"))
    driver.find_element_by_name("submit").click()

def locate_all_reviews_on_page(driver):
    print("looking for elements")
    #This function looks for all the reviews on just one page and returns a list of elements corresponding to them. 
    try:
        reviewPageElements = []
        reviewPageElements = driver.find_elements_by_css_selector(".empReview")
        return reviewPageElements
    except Exception as e:
        print(f"Exception:{e} occured, during the locate_all_reviews_on_page function")

def scrape_one_review(driver, reviewElementsList):
    for each review in reviewElementsList:


def main():
    #Start The Driver
    driver = initialize_driver(True)
    #Navigate to Login Page
    navigate_to_url(driver, "https://www.glassdoor.com/profile/login_input.htm?userOriginHook=HEADER_SIGNIN_LINK")
    #Login to glassdoor using credentials
    glassdoor_login_procedure(driver)
    #Navigate to company Reviews page
    time.sleep(10)
    navigate_to_url(driver, parameters.parameters.get("companyUrl"), True)
    #locate all of the reviews on the page
    time.sleep(8)
    reviewElements = locate_all_reviews_on_page(driver)
    print(reviewElements)
    scrape_one_review()
if __name__ == "__main__":
    main()
