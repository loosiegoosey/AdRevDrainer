from playwright.sync_api import sync_playwright
import time
import random

# Function to log the number of ads clicked
def log_click_count(click_count):
    with open('click_log.txt', 'w') as log_file:
        log_file.write(str(click_count))

def run(playwright):
    # Launch the browser in non-headless mode to see the actions
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    
    # Navigate to Amazon
    page.goto('https://www.amazon.com')

    # Check for CAPTCHA and wait for manual resolution if found
    if page.locator('text=Enter the characters you see below').is_visible():
        print("CAPTCHA detected. Please solve it manually.")
        page.pause()  # Pause the script and allow manual CAPTCHA resolution
    
    # Wait for the search box to be available
    try:
        page.wait_for_selector("#twotabsearchtextbox", timeout=10000)
        search_box = page.locator("#twotabsearchtextbox")
        search_box.fill('Kellogg')  # Enter the search term
        search_box.press("Enter")  # Press Enter to search
    except Exception as e:
        print(f"Search box not found or not interactable: {e}")
        browser.close()
        return

    # Initialize click counter
    click_count = 0
    
    # Infinite loop to keep the script running
    while True:
        try:
            # Wait for ads to load
            ads = page.locator('//a[@id="adLink"]')
            
            if ads.count() == 0:
                print("No ads found.")
                time.sleep(random.uniform(2, 5))  # Random pause before retrying
                continue
            
            # Click on each ad found
            for i in range(ads.count()):
                ad = ads.nth(i)
                
                # Scroll to ad smoothly
                page.evaluate("arguments[0].scrollIntoView({behavior: 'smooth'});", ad)
                time.sleep(random.uniform(1, 3))  # Random delay before clicking

                # Click the ad
                ad.click()
                click_count += 1
                log_click_count(click_count)  # Update the log file

                time.sleep(random.uniform(5, 10))  # Pause after clicking ad

                # Navigate back to the search results
                page.go_back()

        except Exception as e:
            print(f"An error occurred: {e}")
            break

        # Random pause before the next iteration
        time.sleep(random.uniform(2, 5))  # Random pause between 2 and 5 seconds

    # Close the browser (if you ever break out of the loop)
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
