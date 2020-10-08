from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# for waiting for page loads
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re
import json
import time
import parameters
import pandas as pd
import datetime
# from time import strptime

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
        reviewPageElementsIDs = []
        reviewPageElements = driver.find_elements_by_css_selector(".empReview")
        for element in reviewPageElements:
            reviewPageElementsIDs.append(element.get_attribute("id"))
        # fullReviewListHTML = driver.find_element_by_css_selector(".empReviews").get_attribute("innerHTML")
        return reviewPageElements, reviewPageElementsIDs,driver
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
def single_review_element_parser(ReviewID, driver):
    #Takes a single review element and adds each element to a dict with a label
    try: 
        reviewDict = {"Location":None,"Title":None,"Employment Status":None}
        # subratingsDict = {}
        miniRatingsElements = []
        miniRatingsElementsText = []
        #Get the headline
        try:
            reviewDict["Date"] = driver.find_element_by_css_selector(f"#{ReviewID} .date").get_attribute("datetime")
            convertedDate = datetime.datetime.strptime(reviewDict["Date"][0:33], '%a %b %d %Y %H:%M:%S %Z%z')

        except Exception as e:
            print("date not found:"+e)
            reviewDict["Date"] = None
            reviewDict["Day"] = None
            reviewDict["Month"] = None
            reviewDict["Year"] = None
            pass

        reviewDict["PowerBIDate"] = convertedDate.strftime("%m/%d/%Y")
        reviewDict["Time(NOT GMT Adjusted)"] = convertedDate.strftime("%H:%M:%S")
        reviewDict["Headline"]=driver.find_element_by_css_selector(f"#{ReviewID} .reviewLink").text
        reviewDict["Star Rating"]=driver.find_element_by_css_selector(f"#{ReviewID} .v2__EIReviewsRatingsStylesV2__small").text
        # Parse the sub ratings:
        # subratingsElements = driver.find_elements_by_css_selector(f"#{ReviewID} .subRatings__SubRatingsStyles__gdBars.gdBars.gdRatings.med")
        subratingsElements = driver.find_elements_by_css_selector(f"#{ReviewID} .undecorated li")

        # Only Parse Sub ratings if they exist
        if len(subratingsElements)>0:
            for element in subratingsElements:
                reviewDict[element.find_element_by_css_selector("div").get_attribute("innerHTML")] = element.find_element_by_css_selector(".subRatings__SubRatingsStyles__gdBars.gdBars.gdRatings.med").get_attribute("title")

        # Split the current title to get the title and employment status into two categories
        # check the sub header which optionally contains location, title, and employment status
        subheader = driver.find_element_by_css_selector(f"#{ReviewID} .authorJobTitle.middle").text
        # Current Employee - Project Manager in Charlotte, NC
        if " - " and " in " in subheader:
            reviewDict['Employment Status'], afterEmploymentStatus = subheader.split(" - ")
            reviewDict["Title"], reviewDict['Location'] = afterEmploymentStatus.split(" in ")
        
        elif " in " in subheader: 
            reviewDict["Title"], reviewDict['Location'] = afterEmploymentStatus.split(" in ")
        elif " - " in subheader: 
            reviewDict['Employment Status'], reviewDict["Title"] = subheader.split(" - ")
        else:
            reviewDict["Title"]=subheader
  
         miniRatingsElements = driver.find_elements_by_css_selector(f"#{ReviewID} .row.reviewBodyCell.recommends span")

        #There has to be a more pythonic way of doing this:
        if len(miniRatingsElements)>0:
            for element in miniRatingsElements:
                miniRatingsElementsText.append(element.get_attribute("innerHTML"))

            # These attributes are optional, so if they are available, add them to the dict, if not add a placeholder
            for text in miniRatingsElementsText:
                if "Outlook" in text:
                    reviewDict["Positive Outlook"] = text
                elif "Recommend" in text:
                    reviewDict["Recommends"] = text
                elif "CEO" in text:
                    reviewDict["CEO Approval"] = text

        reviewDict["Time working at company"] = driver.find_element_by_css_selector(f"#{ReviewID} .mainText.mb-0").text

        reviewDict["Pros"] = driver.find_element_by_css_selector(f"#{ReviewID} span[data-test='pros']").get_attribute("innerHTML")
        reviewDict["Cons"] = driver.find_element_by_css_selector(f"#{ReviewID} span[data-test='cons']").get_attribute("innerHTML")

        return reviewDict, driver
    except Exception as e:
        print(f"Exception:{e} occured, during the single_review_element_parser function")
        pass
        return reviewDict, driver
    # %%
    # need to pass the driver to keep it alive
def review_one_page_parser(reviewIDList, driver, df):
    # scrapes all reviews on one page, puts in data frame returns frame
    for empReview in reviewIDList:
        data, driver = single_review_element_parser(empReview, driver)
        print(data)
        # data = data.split('\n')
        df2=pd.DataFrame.from_dict([data])
        # print(f"reviewElementsList[empReview]: {empReview} /n \n ")
        # print(empReview.text)
        # [x.split(';') for x in data.split('\n')]
        df = df.append(df2, ignore_index=True)
        print(df)
    return df, driver

def next_page(driver):
    lastPage = False
    try:
        driver.find_element_by_css_selector(".pagination__ArrowStyle__nextArrow").click()
        time.sleep(10)
        wait = WebDriverWait(driver, 25)
        element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.pagination__ArrowStyle__nextArrow  ')))
    except Exception as e:
        print(f"Last Page {e}")
        lastPage = True
    return driver, lastPage

def all_reviews_scraper(driver):
    # takes a driver open to a company review page. Creates an empty dataframe passes frame to review one page parser, then clicks next page and repeats. Returns a full dataframe
    df = pd.DataFrame()
    lastPage = False
    # get review Ids on the given page 
    while lastPage==False:
        reviewElements, reviewIDList, driver = locate_all_reviews_on_page(driver)
        df, driver = review_one_page_parser(reviewIDList, driver, df)
        driver, lastPage = next_page(driver)
    # Scrape the Final Page 
    reviewElements, reviewIDList, driver = locate_all_reviews_on_page(driver)
    df, driver = review_one_page_parser(reviewIDList, driver, df)
    return df, driver



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
    finaldf, driver = all_reviews_scraper(driver)
    print(finaldf.head)
    fileSaveLocation = parameters.parameters.get("outputDirectory")+"/"+parameters.parameters.get("companyUrl")[34:39]+".json"
    print(f"saving to: {fileSaveLocation}")
    finaldf.to_json(fileSaveLocation)

    
    # scrape_one_review(reviewElements)
if __name__ == "__main__":
    main()

# %%
