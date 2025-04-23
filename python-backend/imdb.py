from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
import json
import time

url = "http://www.imdb.com"

def join_content(jc):
    return ','.join(jc)

def iterate_actors(iter_actors):
    m = []
    for item in iter_actors:
        m.append(item['name'])
    return ','.join(m)

def prepare_content(json_content):
    d = {}
    d['image'] = json_content['image']
    d['name'] = json_content['name']
    d['url_content'] = url + json_content['url']
    d['genre'] = join_content(json_content['genre'])
    d['actors'] = iterate_actors(json_content['actor'])
    d['description'] = json_content['description']
    d['trailer'] = url + json_content['trailer']['embedUrl']
    return d

def setup_driver():
    chrome_options = Options()
    #chrome_options.add_argument("--no-sandbox")
    #chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Comment the line below if you want to see the browser window
    # chrome_options.add_argument("--headless=new")
    
    #service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def imdb_searchbox(search_term):
    driver = setup_driver()
    driver.get(url)
    time.sleep(1)
    searchbox = driver.find_element(By.ID, "suggestion-search").send_keys(search_term)
    time.sleep(1)
    searchbox = driver.find_element(By.ID, "react-autowhatever-navSuggestionSearch--item-0").click()
    # print(search_term)
    # searchbox.send_keys(search_term)
    time.sleep(1)
    # driver.find_element(By.ID, "react-autowhatever-1--item-0").click()
    json_content = json.loads(driver.find_element(By.CSS_SELECTOR, 'script[type="application/ld+json"]').get_attribute("innerText"))
    return prepare_content(json_content)

def imdb_search(search_term):
    driver = setup_driver()
    try:
        s = imdb_searchbox(search_term)
        driver.get_screenshot_as_file("capture.png")
        return s
    finally:
        driver.quit()  # Make sure to close the browser