from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import re
import json
import time
import parameters
import pandas as pd
# from bs4 import BeautifulSoup

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
# %%
def locate_all_reviews_on_page(driver):
    print("looking for elements")
    #This function looks for all the reviews on just one page and returns a list of elements corresponding to them. 
    try:
        reviewPageElements = []
        reviewPageElements = driver.find_elements_by_css_selector(".empReview")
        fullReviewListHTML = driver.find_element_by_css_selector(".empReviews").get_attribute("innerHTML")
        return reviewPageElements, fullReviewListHTML
    except Exception as e:
        print(f"Exception:{e} occured, during the locate_all_reviews_on_page function")

#Dont use this, BS4 will slow things down. Scrape directly from the page
# def soupify(rawHTML):
#     soup = BeautifulSoup(rawHTML, "html.parser")
#     print(soup.prettify())


# %%
# def scrape_one_review(driver, reviewElementsList, dataframe=None):
#     # print(reviewElementsList[1].text)
#     # print(reviewElementsList)
#     for empReview in reviewElementsList:
#         # print(f"reviewElementsList[empReview]: {empReview} /n \n ")
#         # print(empReview.text)
#         data = empReview.text
#         df = pd.DataFrame([x.split(';') for x in data.split('\n')])
#         print(df)
#     return df
# %%
def single_review_element_parser(driver, reviewElement):
    #Takes a single review element and adds each element to a dict with a label
    reviewDict = {}
    subratingsList = []
    #Get the headline
    reviewDict["Date"] = reviewElement.find_element_by_class_name("date").get_attribute("datetime")
    reviewDict["Headline"]=reviewElement.find_element_by_class_name("reviewLink").text
    reviewDict["starRating"]=reviewElement.find_element_by_class_name("v2__EIReviewsRatingsStylesV2__ratingNum v2__EIReviewsRatingsStylesV2__small").text
    # Parse the sub ratings:
    subratingsElements = reviewElement.find_elements_by_class("minor")
    
    for element in subratingsElements:
        subratingsList.append(element.find_element_by_class_name("subRatings__SubRatingsStyles__gdBars gdBars gdRatings med").get_attribute("title"))
    # Add each sub rating in the list to the dict:
    reviewDict["Work/Life Balance"] = subratingsList[0]
    reviewDict["Culture & Values"] = subratingsList[1]
    reviewDict["Career Opportunities"] = subratingsList[2]
    reviewDict["Compensation and Benefits"] =subratingsList[3]
    reviewDict["Senior Management"] = subratingsList[4]
    # Split the current title to get the title and employment status into two categories
    # !!! Will need to break out Title in future
    reviewDict["Employment Status"], reviewDict["Location"] = reviewElement.find_element_by_class_name("authorJobTitle middle").text.split(" - ")
    reviewDict["Recommends"], reviewDict["Positive Outlook"], reviewDict["CEO Approval"]=reviewElement.find_element_by_class_name("row reviewBodyCell recommends").find_elements_by_css_selector("span").text
    reviewDict["Time working at company"]=reviewElement.find_element_by_class_name("mainText mb-0").text
    reviewDict["Pros"] = reviewElement.find_element_by_css_selector("span[data-test='pros']").text
    reviewDict["Cons"] = reviewElement.find_element_by_css_selector("span[data-test='cons']").text

    return reviewDict, driver


    # %%
    # need to pass the driver to keep it alive
def review_one_page_parser(reviewElementsList, driver, dataframe=None):
    if dataframe == None:
        df = pd.DataFrame()

    for empReview in reviewElementsList:
        data,driver = single_review_element_parser(driver, empReview)
        print(data)
        # data = data.split('\n')
        df2=pd.DataFrame(data)
        # print(f"reviewElementsList[empReview]: {empReview} /n \n ")
        # print(empReview.text)
        # [x.split(';') for x in data.split('\n')]
        df = df.append(df2, ignore_index=True)
        print(df)
    return df

# def next_glassdoor_page (driver):
#     # Selects the next page at the bottom of the reviews list. will also need to check for the last page in the doc

#     return driver

# %%
def main():
    #Start The Driver
    driver = initialize_driver(True)
    # Navigate to Login Page
    navigate_to_url(driver, "https://www.glassdoor.com/profile/login_input.htm?userOriginHook=HEADER_SIGNIN_LINK")
    #Login to glassdoor using credentials
    glassdoor_login_procedure(driver)
    #Navigate to company Reviews page
    time.sleep(10)
    navigate_to_url(driver, parameters.parameters.get("companyUrl"), True)
    #locate all of the reviews on the page
    time.sleep(8)
    reviewElementsList, fullReviewListHTML = locate_all_reviews_on_page(driver)
    reviewsDataframe = review_one_page_parser(reviewElementsList, driver)
    print(reviewsDataframe.head)
    
    # scrape_one_review(reviewElements)
if __name__ == "__main__":
    main()

# %%
