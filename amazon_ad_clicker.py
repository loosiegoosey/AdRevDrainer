import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException, ElementClickInterceptedException
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

# Set an implicit wait
driver.implicitly_wait(10)

try:
    # Navigate to Amazon and wait for the search box to be present
    driver.get('https://www.amazon.com')

    # Wait for the search box to load
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, 'twotabsearchtextbox'))
    )
    
    search_box = driver.find_element(By.ID, 'twotabsearchtextbox')
    search_box.clear()
    search_box.send_keys('Kellogg')
    search_box.send_keys(Keys.RETURN)

    # Infinite loop to keep the script running
    clicked_ads_count = 0
    while True:
        try:
            # Wait for ads to be located
            ads = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href, 'click-src')]"))
            )
            
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
                    # Wait for the search results to load again
                    WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.ID, 'twotabsearchtextbox'))
                    )
                except (ElementClickInterceptedException, NoSuchElementException, WebDriverException) as e:
                    print(f"Exception occurred while clicking an ad: {str(e)}")
                    driver.back()  # Ensure we go back to search results if an error occurs
                    WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.ID, 'twotabsearchtextbox'))
                    )
                    continue
                
        except TimeoutException:
            print("Ads not found within the time frame. Retrying...")
            driver.refresh()  # Refresh the page to retry finding ads
            
        # Pause before the next iteration
        time.sleep(random.uniform(2, 5))  # Random pause between 2 and 5 seconds

except KeyboardInterrupt:
    print(f"Script terminated by user. Total ads clicked: {clicked_ads_count}")

finally:
    driver.quit()  # Ensure the browser is closed properly