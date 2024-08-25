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

# Set up Chrome options with user agent
chrome_options = Options()
chrome_options.add_argument(f"user-agent={UserAgent().random}")
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--allow-running-insecure-content')
# Remove the '--headless' option to see the browser window
# chrome_options.add_argument('--headless')
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
    search_box = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, 'twotabsearchtextbox'))
    )
    search_box.send_keys('Kellogg')
    search_box.send_keys(Keys.RETURN)
except TimeoutException:
    print("Search box not found.")
    print(driver.page_source)

# Infinite loop to keep the script running
try:
    while True:
        ads = None
        try:
            # Find and click on ads that match the given pattern
            ads = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@href, "/dp/") and contains(@style, "position:absolute")]'))
            )
            if not ads:
                print("No ads found.")
            else:
                print(f"Found {len(ads)} ads.")
                for ad in ads:
                    print(f"Ad href: {ad.get_attribute('href')}, Ad style: {ad.get_attribute('style')}")
                    time.sleep(random.uniform(5, 15))  # Random pause before clicking
                    
                    # Smooth scroll to the ad (like a human)
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth'});", ad)
                    time.sleep(random.uniform(1, 3))
                    
                    ad.click()
                    print(f"Clicked on ad: {ad.get_attribute('href')}")
                    
                    time.sleep(random.uniform(5, 10))  # Pause after clicking ad
                    
                    # Go back to search results
                    driver.back()
                    print("Returned to search results.")
                    
        except TimeoutException:
            print("Ads not found within the time frame.")
            print(driver.page_source)  # Log the page source for debugging
            
        except WebDriverException:
            print("Browser closed or unreachable. Exiting loop.")
            break
        
        # Pause before the next iteration
        time.sleep(random.uniform(2, 5))  # Random pause between 2 and 5 seconds

except KeyboardInterrupt:
    print("Script terminated by user.")

# Note: No driver.quit() to keep the browser open
