import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class ScrapeWebPage:
    """Scrapes the Web page and processes it as required.
    """
    def __init__(self, url) -> None:
        self.url = url
        self.driver = None
        self.setup_driver()
    
    def setup_driver(self):
        """Sets up the Selenium WebDriver with appropriate options."""
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run in headless mode
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        
        self.driver = webdriver.Chrome(options=chrome_options)
    
    @staticmethod
    def extract_base_url(url:str)->str:
        """Extracts the base url from a long url."""
        pattern = r'^.+?[^\/:](?=[?\/]|$)'
        match = re.match(pattern, url)
        if match:
            return match.group(0)
        else: 
            raise Exception("Invalid URL.")
    
    def get_url(self):
        base_url = ScrapeWebPage.extract_base_url(self.url)
        print(f"BASE URL:{base_url}")
        
        try:
            self.driver.get(self.url)
            # Wait for page to load
            time.sleep(5)
            
            # Wait for elements to be present
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Get page source after JavaScript execution
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, "html.parser")
            
            urls = []
            for link in soup.find_all("a"):
                urls.append(link.get("href"))
                
            if self.url not in urls:
                urls.append(self.url)
            elif base_url not in urls:
                urls.append(base_url)
                
            urls = list(set(urls))
            urls = list(filter(None, urls))
            print(urls)
            return urls, base_url
            
        except Exception as e:
            print(f"Error during URL extraction: {e}")
            return [], base_url
        
    def process_urls(self, url_list:list, base_url:str)->list:
        """Processes unnecessary urls in the list and adds the base url if required."""
        new_url_list = [url for url in url_list if "#" not in url]
        for index, item in enumerate(new_url_list):
            if item.startswith("/"):
                new_url_list[index] = f"{self.url.rstrip('/')}{item}"
        new_url_list = [url for url in new_url_list if base_url in url]
        return new_url_list
    
    def get_page_contents(self, url_list:list):
        pages = []
        for link in url_list:
            try:
                print(f"Processing link: {link}")
                self.driver.get(link)
                time.sleep(3)  # Wait for JavaScript to load
                
                # Wait for content to be present
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                
                page_source = self.driver.page_source
                scraped_data = BeautifulSoup(page_source, "html.parser")
                filtered_text = scraped_data.text
                cleaned_text = ScrapeWebPage.remove_whitespace(filtered_text)
                pages.append({
                    "text": cleaned_text,
                    "source": link
                })
                print(f"filtered: {filtered_text}")
            except Exception as e:
                print(f"Error processing {link}: {e}")
                continue
        return pages
    
    @staticmethod
    def remove_whitespace(text:str):
        pattern = r"\s+"
        s = re.sub(pattern, " ", text)
        return s
    
    def __del__(self):
        """Clean up the WebDriver when the object is destroyed."""
        if self.driver:
            self.driver.quit()

# Example usage:
# scraper = ScrapeWebPage("https://help.twitter.com/en/rules-and-policies/ban-evasion.html")
# url_list, base_url = scraper.get_url()
# processed_url = scraper.process_urls(url_list=[scraper.url], base_url=base_url)
# content = scraper.get_page_contents(url_list=set(processed_url))
# print(content)