# Purpose

Scrape information from a Glassdoor company reviews page for employee sentiment analysis. 

# Usage

Create a file called "parameters.py" in the main directory. Use this template for passing parameters to the scraper script:
```parameters = {"username": "","password": "","companyUrl": "",}```


# Todo
- [ ] Replace ```time.sleep``` with a more robust solution to wait for page load
- [ ] add All Reviews to Dataframe
- [ ] Break out location from title when parsing
- [ ] next page support
- [ ] visualize the data