import logging
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from proxy_manager import ProxyManager
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("ad_clicker.log"),
        logging.StreamHandler()
    ]
)

def setup_browser(proxy, driver_path):
    chrome_options = Options()
    chrome_options.add_argument(f'--proxy-server={proxy}')
    user_agent = random.choice([
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36"
    ])
    chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    service = Service(driver_path)
    browser = webdriver.Chrome(service=service, options=chrome_options)
    browser.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": user_agent})
    return browser

def human_like_interaction(browser):
    actions = ActionChains(browser)
    actions.move_by_offset(random.randint(10, 100), random.randint(10, 100)).perform()
    actions.click()
    time.sleep(random.uniform(0.5, 2.5))

def click_ads(browser, num_ads):
    ad_count = 0
    ad_companies = []
    while ad_count < num_ads:
        try:
            ads = browser.find_elements(By.CLASS_NAME, 'ad-class-name')  # Update this selector
            if ads:
                for ad in ads:
                    human_like_interaction(browser)
                    ad.click()
                    ad_companies.append(ad.get_attribute("data-company"))  # Adjust based on ad element attributes
                    ad_count += 1
                    logging.info(f'Clicked on ad for {ad_companies[-1]}')
                    time.sleep(random.uniform(5, 10))  # Wait between clicks
                    if ad_count >= num_ads:
                        break
            else:
                logging.warning('No ads found, scrolling down')
                browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
                time.sleep(random.uniform(2, 5))
        except Exception as e:
            logging.error(f'Error clicking ads: {e}')
            break
    return ad_companies

def main():
    proxy_manager = ProxyManager()
    total_ads_to_click = int(input("Enter the number of ads to click: "))
    start_time = datetime.now()
    clicked_ads = 0
    ad_companies = []

    while clicked_ads < total_ads_to_click:
        valid_proxy = proxy_manager.get_next_proxy()
        if not valid_proxy:
            logging.error("No valid proxies available")
            break

        try:
            browser = setup_browser(valid_proxy, driver_path='C:\\Users\\Yuriy\\Documents\\GitHub\\AmazonAdRevDrainer\\chromedriver.exe')
            logging.info(f'Using proxy: {valid_proxy}')
            ad_companies += click_ads(browser, total_ads_to_click - clicked_ads)
            clicked_ads = len(ad_companies)
            browser.quit()
        except Exception as e:
            logging.error(f'Error during browser setup or ad clicking: {e}')
            proxy_manager.invalidate_proxy(valid_proxy)
            time.sleep(random.uniform(5, 10))
            continue

    end_time = datetime.now()
    total_time = end_time - start_time

    logging.info(f'Total ads clicked: {clicked_ads}')
    logging.info(f'Companies: {ad_companies}')
    logging.info(f'Total time taken: {total_time}')

if __name__ == "__main__":
    main()
