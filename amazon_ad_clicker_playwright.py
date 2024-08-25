import time
import random
from playwright.sync_api import sync_playwright

def run(playwright):
    # Launch browser
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    )
    
    # Open a new page
    page = context.new_page()
    
    # Navigate to Amazon
    page.goto('https://www.amazon.com')
    
    try:
        # Wait for the page to fully load
        page.wait_for_load_state('networkidle')
        
        # Wait for the search box to be available and interact with it
        search_box = page.locator('#twotabsearchtextbox')
        search_box.wait_for(state='visible', timeout=10000)  # Wait for up to 10 seconds for the search box to appear

        if search_box.is_visible():
            search_box.fill('Kellogg')  # Type 'Kellogg' into the search box
            search_box.press('Enter')  # Press Enter to search
        else:
            print("Search box not found or not interactable. Exiting script.")
            context.close()
            browser.close()
            return
    
    except Exception as e:
        print(f"Search box not found or not interactable: {e}")
        context.close()
        browser.close()
        return
    
    # Initialize ad click counter
    ad_click_counter = 0
    
    try:
        # Infinite loop to keep the script running
        while True:
            ads = None
            try:
                # Wait for banner ads to be present
                ads = page.locator('a#adLink')
                ads.wait_for(state='visible', timeout=15000)  # Wait up to 15 seconds for ads to become visible

                if ads.count() == 0:
                    print("No ads found.")
                else:
                    print(f"Found {ads.count()} ads.")
                    for ad in range(ads.count()):
                        time.sleep(random.uniform(5, 15))  # Random pause before clicking
                        
                        # Smooth scroll to the ad (like a human)
                        ads.nth(ad).scroll_into_view_if_needed()
                        time.sleep(random.uniform(1, 3))
                        
                        if ads.nth(ad).is_visible() and ads.nth(ad).is_enabled():
                            ads.nth(ad).click()
                            ad_click_counter += 1
                            print(f"Ad clicked. Total clicks: {ad_click_counter}")
                        else:
                            print("Ad not clickable.")

                        time.sleep(random.uniform(5, 10))  # Pause after clicking ad
                        
                        # Go back to search results
                        page.go_back()
                        
            except Exception as e:
                print(f"Ads not found or click failed: {e}")
            
            # Log the number of ad clicks
            with open("click_log.txt", "w") as log_file:
                log_file.write(f"{ad_click_counter}\n")
            
            # Pause before the next iteration
            time.sleep(random.uniform(2, 5))  # Random pause between 2 and 5 seconds
            
    except KeyboardInterrupt:
        print("Script terminated by user.")
    finally:
        # Close the browser and context
        context.close()
        browser.close()

with sync_playwright() as playwright:
    run(playwright)
