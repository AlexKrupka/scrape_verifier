from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import re

from TermsOfServiceParser import check_terms_of_service, format_url


class TermsOfServiceFinder:
    TOS_PATTERNS = [r"terms.*", r"conditions.*", r"terms of service.*", r"terms and conditions.*", r"legal.*", r"privacy.*"]

    def find_terms_of_service_link(self, url):
        safe_url = format_url(url)
        options = Options()
        options.headless = True

        # Use Chrome in headless mode; replace with Firefox or another browser if preferred
        with webdriver.Firefox(options=options) as browser:
            browser.get(safe_url)
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            links = [link for link in soup.find_all('a', href=True) if link]
            links.reverse()
            for link in links:
                href = link['href']
                link_text = link.get_text().lower()
                if any(re.match(pattern, link_text) for pattern in self.TOS_PATTERNS):
                    return href if href.startswith('http') else f'{url.rstrip("/")}/{href.lstrip("/")}'
        return None



# Usage example
if __name__ == "__main__":
    tos_finder = TermsOfServiceFinder()
    user_input_url = input("Enter the URL of the website: ")

    tos_link = tos_finder.find_terms_of_service_link(user_input_url)

    if tos_link:
        print(f"Terms of Service link found: {tos_link}. Checking legality")
        legality = check_terms_of_service(tos_link)
        print(legality)
    else:
        print("Terms of Service link not found.")



