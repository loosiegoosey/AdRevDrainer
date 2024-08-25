import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from fake_useragent import UserAgent
import random
from webdriver_manager.chrome import ChromeDriverManager
import logging

# Configure logging to write only the click counter to a file
logging.basicConfig(filename='ad_clicks.log', level=logging.INFO, format='%(message)s')

# Set up Chrome options with user agent
chrome_options = Options()
chrome_options.add_argument(f"user-agent={UserAgent().random}")
chrome_options.add_argument('--start-maximized')  # Start maximized for better visibility
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)

# Set up WebDriver with the configured options
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Add a delay to allow WebDriver to start up properly
time.sleep(5)

# Set an implicit wait
driver.implicitly_wait(10)

# Navigate to Amazon and wait for the search box to be present
driver.get('https://www.amazon.com')

try:
    # Additional wait to ensure the page is fully loaded
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, 'twotabsearchtextbox'))
    )
    
    search_box = driver.find_element(By.ID, 'twotabsearchtextbox')
    
    if search_box.is_displayed() and search_box.is_enabled():
        search_box.clear()
        search_box.send_keys('Kellogg')
        search_box.send_keys(Keys.RETURN)
    else:
        print("Search box is not interactable.")
        print(driver.page_source)
        driver.quit()
        
except TimeoutException:
    print("Search box not found or not interactable. Exiting script.")
    print(driver.page_source)  # Print page source for debugging
    driver.quit()

# Infinite loop to keep the script running
try:
    clicked_ads_count = 0
    while True:
        ads = None
        try:
            # Find and click on ads that match the provided XPath
            ads = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.XPATH, '//*[@id="adLink"]'))
            )
            if ads:
                for ad in ads:
                    try:
                        time.sleep(random.uniform(2, 5))  # Random pause before clicking
                        
                        # Smooth scroll to the ad (like a human)
                        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth'});", ad)
                        time.sleep(random.uniform(1, 3))
                        
                        ad.click()
                        clicked_ads_count += 1  # Increment the counter
                        logging.info(f"{clicked_ads_count}")  # Log only the click counter
                        
                        time.sleep(random.uniform(5, 10))  # Pause after clicking ad
                        
                        # Go back to search results
                        driver.back()
                    except WebDriverException as e:
                        print(f"WebDriverException occurred: {str(e)}")
                    
        except TimeoutException:
            print("Ads not found within the time frame.")
            
        except WebDriverException as e:
            print(f"WebDriverException occurred: {str(e)}")
            break
        
        # Pause before the next iteration
        time.sleep(random.uniform(2, 5))  # Random pause between 2 and 5 seconds

except KeyboardInterrupt:
    print(f"Script terminated by user. Total ads clicked: {clicked_ads_count}")

# Note: No driver.quit() to keep the browser open
