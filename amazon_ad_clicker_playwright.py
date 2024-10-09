import asyncio
from playwright.async_api import async_playwright
import time
import random
from datetime import datetime

# Function to log the number of ads clicked
def log_click_count(click_count):
    with open('click_log.txt', 'a') as log_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"{timestamp} - Click Count: {click_count}\n")

async def run(playwright, url, max_iterations):
    # Launch the browser in headless mode for better performance
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()
    
    try:
        # Navigate to the specified URL with retry logic
        for attempt in range(3):
            try:
                await page.goto(url, timeout=30000)
                break
            except Exception as e:
                if attempt < 2:
                    print(f"Navigation to {url} failed (attempt {attempt + 1}). Retrying...")
                    await asyncio.sleep(5)
                else:
                    print(f"Failed to navigate to {url} after 3 attempts: {e}")
                    return

        # Check for CAPTCHA and wait for manual resolution if found
        try:
            captcha_text = 'Enter the characters you see below'
            if await page.locator(f'text={captcha_text}').is_visible():
                print("CAPTCHA detected. Please solve it manually.")
                await asyncio.wait_for(page.wait_for_selector(f'text={captcha_text}', state='hidden'), timeout=60000)  # Wait up to 60 seconds for CAPTCHA to be solved
        except Exception as e:
            print(f"Error checking for CAPTCHA: {e}")
            return
        
        # Wait for the search box to be available
        try:
            await page.wait_for_selector("#twotabsearchtextbox", timeout=15000)
            search_box = page.locator("#twotabsearchtextbox")
            await search_box.fill('Kellogg')  # Enter the search term
            await search_box.press("Enter")  # Press Enter to search
        except Exception as e:
            print(f"Search box not found or not interactable: {e}")
            return

        # Initialize click counter
        click_count = 0
        
        # Loop with a maximum number of iterations to prevent indefinite execution
        for _ in range(max_iterations):
            try:
                # Locate ads on the page
                ads = page.locator("#adLink, [aria-labelledby='adLink adLink-label']")
                ads_count = await ads.count()
                
                if ads_count > 0:
                    for i in range(ads_count):
                        single_ad = ads.nth(i)
                        
                        # Scroll to ad smoothly
                        await single_ad.scroll_into_view_if_needed()
                        await asyncio.sleep(random.uniform(1, 3) * random.uniform(0.5, 1.5))  # More dynamic random delay before clicking

                        # Click the ad
                        await single_ad.click()
                        click_count += 1
                        log_click_count(click_count)  # Update the log file

                        await asyncio.sleep(random.uniform(5, 10) * random.uniform(0.5, 1.5))  # More dynamic pause after clicking ad

                        # Navigate back to the search results
                        await page.goto(url)
                else:
                    print("No ads found on the page. Refreshing...")
                    await page.reload()
                    await asyncio.sleep(random.uniform(2, 5) * random.uniform(0.5, 1.5))  # More dynamic random pause before retrying
                
            except Exception as e:
                print(f"An error occurred: {e}")
                break

            # Random pause before the next iteration
            await asyncio.sleep(random.uniform(2, 5) * random.uniform(0.5, 1.5))  # More dynamic random pause between iterations
    finally:
        # Close the page, context, and browser to avoid resource leaks
        await page.close()
        await context.close()
        await browser.close()

async def main():
    url = 'https://www.amazon.com'
    max_iterations = 10
    async with async_playwright() as playwright:
        await run(playwright, url, max_iterations)

if __name__ == "__main__":
    if asyncio.get_event_loop().is_running():
        loop = asyncio.get_event_loop()
        loop.create_task(main())
    else:
        asyncio.run(main())