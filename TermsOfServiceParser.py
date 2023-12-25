from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def check_terms_of_service(url):

    prohibited_terms = [
    "scraping",
    "automated access",
    "data mining",
    "crawling",
    "harvesting",
    "data collection",
    "data gathering",
    "unauthorized use",
    "unauthorized access",
    "intellectual property",
    "API use",
    "robots",
    "bandwidth usage",
    "extraction tools",
    "commercial purpose"
    ]

    options = Options()
    options.headless = True

    with webdriver.Firefox(options=options) as browser:
        browser.get(format_url(url))
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        text = soup.get_text().lower()
        terms = []
        for term in prohibited_terms:
            if term in text:
                terms.append(term)

        if any(terms):
            return f"The following terms were found '{ terms }' Scraping is prohibited."
        return "No specific prohibitions on scraping found in the Terms of Service."

def format_url(user_input):
    if not user_input.startswith("https://www."):
        # Check if it starts with 'http://' or 'https://'
        if user_input.startswith("http://"):
            user_input = "https://" + user_input[len("http://"):]
        elif user_input.startswith("https://"):
            user_input = "https://www." + user_input[len("https://"):]
        elif user_input.startswith("www."):
            user_input = "https://" + user_input
        else:
            user_input = "https://www." + user_input
    return user_input