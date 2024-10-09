import asyncio
from playwright.async_api import async_playwright
import time
import random
import nest_asyncio

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

# Function to log the number of ads clicked
def log_click_count(click_count):
    with open('click_log.txt', 'a') as log_file:
        log_file.write(str(click_count))

async def run(playwright, url):
    # Launch the browser in headless mode for better performance
    browser = await playwright.chromium.launch(headless=True)
    context = await browser.new_context()
    page = await context.new_page()
    
    # Navigate to the specified URL
    await page.goto(url)

    # Check for CAPTCHA and wait for manual resolution if found
    try:
        captcha_text = 'Enter the characters you see below'
        if await page.locator(f'text={captcha_text}').is_visible():
            print("CAPTCHA detected. Please solve it manually.")
            await page.pause()  # Pause the script and allow manual CAPTCHA resolution
    except Exception as e:
        print(f"Error checking for CAPTCHA: {e}")
        await browser.close()
        return
    
    # Wait for the search box to be available
    try:
        search_box = await page.wait_for_selector("#twotabsearchtextbox", timeout=10000)
        await search_box.fill('Kellogg')  # Enter the search term
        await search_box.press("Enter")  # Press Enter to search
    except Exception as e:
        print(f"Search box not found or not interactable: {e}")
        await browser.close()
        return

    # Initialize click counter
    click_count = 0
    
    # Loop with a maximum number of iterations to prevent indefinite execution
    max_iterations = 10
    for _ in range(max_iterations):
        try:
            # Locate iframes on the page
            iframes = page.frames
            
            ads_found = False

            for iframe in iframes:
                try:
                    # Check if the iframe contains the ad element
                    ad = iframe.locator("#adLink")
                    
                    if await ad.count() > 0:
                        ads_found = True
                        for i in range(await ad.count()):
                            single_ad = ad.nth(i)
                            
                            # Scroll to ad smoothly
                            await iframe.evaluate("(ad) => ad.scrollIntoView({behavior: 'smooth'})", single_ad)
                            await asyncio.sleep(random.uniform(1, 3))  # Random delay before clicking

                            # Click the ad
                            await single_ad.click()
                            click_count += 1
                            log_click_count(click_count)  # Update the log file

                            await asyncio.sleep(random.uniform(5, 10))  # Pause after clicking ad

                            # Navigate back to the search results
                            await page.go_back()
                    else:
                        print("No ads found in the current iframe.")
                except Exception as iframe_error:
                    print(f"Error interacting with iframe: {iframe_error}")
            
            if not ads_found:
                print("No ads found on the page. Refreshing...")
                await page.reload()
                await asyncio.sleep(random.uniform(2, 5))  # Random pause before retrying
            
        except Exception as e:
            print(f"An error occurred: {e}")
            break

        # Random pause before the next iteration
        await asyncio.sleep(random.uniform(2, 5))  # Random pause between 2 and 5 seconds

    # Close the browser (if you ever break out of the loop)
    await browser.close()

async def main():
    url = 'https://www.amazon.com'
    async with async_playwright() as playwright:
        await run(playwright, url)

if __name__ == "__main__":
    asyncio.run(main())