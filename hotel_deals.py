from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import TimeoutException
import time
import os

def get_home_page_links():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 20)
    url = "https://www.hotelinvestmenttoday.com/deals/transactions"
    driver.get(url)
    time.sleep(7)
    
    if driver.find_element(By.ID, 'olyticsModal'):
        modal = driver.find_element(By.ID, 'olyticsModal')
        close_button = modal.find_element(By.CLASS_NAME, 'close-olyticsmodal')
        close_button.click()
        print("Modal closed.")
    
    if driver.find_element(By.ID, 'onetrust-accept-btn-handler'):
        close_cookie = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
        close_cookie.click()
        print("Cookie closed")
        
    href_list = []
    
    while True:
        list_view_div = driver.find_element(By.CLASS_NAME, 'list-view')
        item_divs = list_view_div.find_elements(By.CLASS_NAME,'item')
        
        for item_div in item_divs:
            a_tag = item_div.find_element(By.TAG_NAME, 'a')
            href = a_tag.get_attribute('href')
            
            if href not in href_list:
                href_list.append(href)
        try:
            more_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'show-more')))
            more_button.click()
            time.sleep(2)
        except NoSuchElementException:
            print("No more 'More' button found.")
            break
        except TimeoutException:
            print("Reached end")
            break
    
    with open('links.txt', 'w') as file:
        for href in href_list:
            file.write(href + '\n')

    print(f"Total hrefs found: {len(href_list)}")
    print("Links have been written to hrefs.txt")

def download_links():
    driver = webdriver.Chrome()
    with open('links.txt') as file:
        for href in file:
            driver.get(href)
            time.sleep(3)
            try:
                download_links = driver.find_elements(By.PARTIAL_LINK_TEXT, 'here')
                
                if download_links:
                    true_link = download_links[-1]
                    true_link.click()
                    time.sleep(5)

            except Exception as e:
                print(f"Cant find link:{href}")

get_home_page_links()
download_links()
