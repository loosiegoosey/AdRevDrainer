import time
import random
import logging
from playwright.sync_api import sync_playwright

# Configure logging to write only the click counter to a file
logging.basicConfig(filename='ad_clicks.log', level=logging.INFO, format='%(message)s')

# Function to run the Playwright script
def run(playwright):
    browser = playwright.chromium.launch(headless=False)  # Set headless=True to run without UI
    context = browser.new_context(user_agent=playwright.devices['iPhone 12'].user_agent)
    page = context.new_page()
    
    # Navigate to Amazon
    page.goto('https://www.amazon.com')

    # Wait for the search box and input search term
    try:
        page.wait_for_selector('#twotabsearchtextbox', timeout=30000)
        search_box = page.locator('#twotabsearchtextbox')
        search_box.fill('Kellogg')
        search_box.press('Enter')
    except Exception as e:
        print(f"Search box not found or not interactable: {str(e)}")
        page.screenshot(path="error_screenshot.png")
        browser.close()
        return

    # Infinite loop to keep the script running
    clicked_ads_count = 0
    try:
        while True:
            try:
                ads = page.locator('//*[@id="adLink"]')
                ad_count = ads.count()
                if ad_count > 0:
                    for i in range(ad_count):
                        try:
                            ad = ads.nth(i)
                            ad.scroll_into_view_if_needed()
                            time.sleep(random.uniform(1, 3))  # Random pause before clicking
                            ad.click()
                            clicked_ads_count += 1  # Increment the counter
                            logging.info(f"{clicked_ads_count}")  # Log only the click counter
                            
                            time.sleep(random.uniform(5, 10))  # Pause after clicking ad
                            
                            # Go back to search results
                            page.go_back()
                        except Exception as ad_exception:
                            print(f"Error clicking ad: {str(ad_exception)}")
                    
            except Exception as e:
                print(f"Ads not found or another error occurred: {str(e)}")
            
            # Pause before the next iteration
            time.sleep(random.uniform(2, 5))  # Random pause between 2 and 5 seconds

    except KeyboardInterrupt:
        print(f"Script terminated by user. Total ads clicked: {clicked_ads_count}")

    # No need to close the browser here since we want to keep it open

# Run the Playwright script
with sync_playwright() as playwright:
    run(playwright)
