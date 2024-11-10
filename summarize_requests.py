# -*- coding: utf-8 -*-


import pandas as pd
from selenium import webdriver
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pickle
import time

# Set up Firefox options
options = Options()
options.add_argument('--no-sandbox')
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--window-size=1920,1080")
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.set_preference("general.useragent.override", 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0')

def initialize_model(Username,Password) :
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get("https://wordcount.com/login")
    
    username = driver.find_element(By.CSS_SELECTOR, 'input[name="username"]')
    password = driver.find_element(By.CSS_SELECTOR, 'input[name="Password"]')

    username.send_keys("JdaKung@gmail.com")
    password.send_keys("3xp{Kz7r2(rK")

    time.sleep(1)

    login_button = driver.find_elements(By.CLASS_NAME, "css-1oynujq-button")
    login_button[1].click()

    time.sleep(1)
    # Find the span element by its class name
    driver.get("https://wordcount.com/th/text-summarizer")

    input("Press Enter to close the browser...")

def summarize(Username,Password,content) :
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)

    driver.get("https://wordcount.com/login")
    
    username = driver.find_element(By.CSS_SELECTOR, 'input[name="username"]')
    password = driver.find_element(By.CSS_SELECTOR, 'input[name="Password"]')

    username.send_keys(Username)
    password.send_keys(Password)

    time.sleep(1)

    login_button = driver.find_elements(By.CLASS_NAME, "css-1oynujq-button")
    login_button[1].click()

    time.sleep(1)
    # Find the span element by its class name
    driver.get("https://wordcount.com/th/text-summarizer")

    print("Summarize model ready!")
    textarea = driver.find_element(By.CSS_SELECTOR, 'textarea[class="css-1stoj7k-textarea"]')

    # Enter text into the textarea
    textarea.send_keys(content)

    buttons = driver.find_elements(By.TAG_NAME, 'button')
    
    buttons[2].click()

    print("Summarizing text...")

    time.sleep(15)

    textarea = driver.find_elements(By.CLASS_NAME, "css-1stoj7k-textarea")

    if(len(textarea) > 1 and not (textarea[1].text.isspace() or textarea[1].text == "")) :
        summary = textarea[1].text
    else :
        summary = textarea[0].text
    
    print(summary)

    driver.get("https://wordcount.com/th/text-summarizer")

    time.sleep(2)

    delete = driver.find_elements(By.CSS_SELECTOR, 'button[class="css-1oynujq-button css-7xt92p-buttonIcon css-1cvsyjy"]')
    pre = len(delete)
    while(len(delete) > 0) :
        delete[0].click()
        time.sleep(1)
        delete = driver.find_elements(By.CSS_SELECTOR, 'button[class="css-1oynujq-button css-7xt92p-buttonIcon css-1cvsyjy"]')
        if(len(delete) == pre) : break
        pre = len(delete)

    return summary
    # while(True):
    #     pass

    # summarize = driver.find_elements(By.CLASS_NAME, "css-1oynujq-button")
    # summarize[3].click()

    # username.clear()
    # password.clear()

    # username.send_keys(Username)
    # password.send_keys(Password)

    # agreeterm = driver.find_element(By.ID,"checky")
    # agreeterm.click()

    # getin = driver.find_element(By.CSS_SELECTOR,'input[type = "submit"]')

    # getin.click()

    # cookies = driver.get_cookies()

    # session = requests.Session()  # Create a requests session
    # for cookie in cookies:
    #     session.cookies.set(cookie['name'], cookie['value'])

    # search = driver.find_element(By.CSS_SELECTOR, 'li[class = "c-header__item c-header__item--padding c-header__item--pipe"]')
    # search.click()

    # search_text = driver.find_element(By.ID, 'keywords')
    # search_text.clear()
    # search_text.send_keys('Deep Learning')

    # search_text.send_keys(u'\ue007')

    # # Year Range
    # startingyear = 2024
    # endingyear = 2024

    # while(startingyear <= endingyear) :

    #     dismiss_cookie = driver.find_elements(By.CSS_SELECTOR, 'button[class = "c-cookie-banner__dismiss"]')
    #     if(len(dismiss_cookie) != 0) : 
    #         dismiss_cookie[0].click()

    #     date = driver.find_element(By.CSS_SELECTOR, 'button[data-track-action = "date filter"]')
    #     date.click()

    #     date_range = driver.find_element(By.CSS_SELECTOR, 'a[data-test = "advance-search-link-date"]')
    #     date_range.click()

    #     start_year = driver.find_element(By.CSS_SELECTOR, 'select[name = "start_year"]')
    #     select = Select(start_year)
    #     select.select_by_visible_text(str(startingyear))

    #     end_year = driver.find_element(By.CSS_SELECTOR, 'select[name = "end_year"]')
    #     select = Select(end_year)
    #     select.select_by_visible_text(str(startingyear))

    #     search_button = driver.find_element(By.CSS_SELECTOR, 'button[class = "c-search__button c-search__button--width-auto"]')
    #     search_button.click()

    #     article_type = driver.find_element(By.CSS_SELECTOR, 'button[data-track-action = "article type filter"]')
    #     article_type.click()

    #     research_type = driver.find_element(By.ID, 'article-type-research')
    #     research_type.click()

    #     apply_filter = driver.find_element(By.CSS_SELECTOR, 'button.c-facet__submit')
    #     apply_filter.submit()

    #     latest = driver.find_element(By.ID, 'sort-by-date_desc')
    #     latest.click()

    #     count = 1

    #     while(True) :
    #         all_link = driver.find_elements(By.CSS_SELECTOR, 'a[data-track-action = "view article"]')

    #         if len(all_link) == 0 :
    #             search_return = driver.find_element(By.CSS_SELECTOR, 'button[class = "c-search__button"]')
    #             search_return.click()

    #             break

    #         for link in all_link :
    #             URL = link.get_attribute('href')
    #             soup = fetch_data(URL,cache_path,session)
    #             title = soup.find('h1', class_='c-article-title')
    #             subjects = [subject.get_text(strip=True) for subject in soup.find_all('li', class_='c-article-subject-list__subject')]
    #             authors = [author.get_text(strip=True) for author in soup.find_all('a', attrs={'data-test': 'author-name'})]
    #             publish_date = parse_time(soup.find('time'))
                
    #             if title is not None and len(subjects) != 0 and len(authors) != 0 :
    #                 data = { 
    #                     'title' : title.text.strip(), 
    #                     'subjects' : subjects, 
    #                     'authors' : authors, 
    #                     'publish-date' : publish_date
    #                     }
    #                 yield data

    #             count += 1
            
    #         try:
    #             next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'li[data-page="next"]')))
    #             next_button.click()
    #         except:
    #             search_return = driver.find_element(By.CSS_SELECTOR, 'button[class = "c-search__button"]')
    #             search_return.click()

    #             break
            
    #     startingyear += 1

# if __name__ == "__main__" :
#     # initialize_model(1,1)
#     summarize(1,2,3)