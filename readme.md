# Purpose

Scrape information from a Glassdoor company reviews page for employee sentiment analysis. All information from the review is scraped if available including: Date, Location, Rating, Sub-ratings, Recommender Status, CEO Approval, Company Outlook, Pros, and Cons. A glassdoor account is required to use the script.

# Usage

Create a file called "parameters.py" in the main directory. Use this template for passing parameters to the scraper script:
```parameters = {"username": "GlassdoorEmail","password": "GlassdoorPassword","companyUrl": "https://www.glassdoor.com/Reviews/CompanyXYZ-Reviews-E23412.htm", outputDirectory: "C:/documents/companyData.json" }```


# Todo
- [ ] Replace ```time.sleep``` with a more robust solution to wait for page load
- [x] Add All Reviews to Dataframe
- [ ] Break out location from title when parsing
- [x] Next page support
- [x] Visualize the data (PowerBI)
- [ ] trim the time working at company or break out a full time, part time columns.
- [ ] Clean up & comment out sections.
- [ ] Add DataVis Example to Readme
- [ ] Create Requirements.txt