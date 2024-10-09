import asyncio
from playwright.async_api import async_playwright
import random
from datetime import datetime

# Function to log the number of ads clicked
def log_click_count(click_count):
    with open('click_log.txt', 'a') as log_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"{timestamp} - Click Count: {click_count}\n")

async def run(playwright, url, max_iterations, timeout=60000):
    # Launch the browser in headless mode for better performance
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()
    
    try:
        # Navigate to the specified URL with retry logic
        for attempt in range(3):
            try:
                await page.goto(url, timeout=timeout)
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
                for _ in range(120):  # Check every 5 seconds for up to 600 seconds
                    if not await page.locator(f'text={captcha_text}').is_visible():
                        break
                    print("Waiting for CAPTCHA to be solved...")
                    await asyncio.sleep(5)
                else:
                    print("CAPTCHA was not solved in time.")
                    return
        except Exception as e:
            print(f"Error checking for CAPTCHA: {e}")
            return
        
        # Wait for the search box to be available
        try:
            await page.wait_for_selector("#twotabsearchtextbox", timeout=30000)
            search_box = page.locator("#twotabsearchtextbox")
            await search_box.fill('Kellogg')  # Enter the search term
            await search_box.press("Enter")  # Press Enter to search
        except Exception as e:
            print(f"Search box not found or not interactable: {e}")
            return

        # Initialize click counter
        click_count = 0
        navigation_stack = []
        
        # Loop with a maximum number of iterations to prevent indefinite execution
        for _ in range(max_iterations):
            try:
                # Scroll to the bottom of the page to load more ads, retry if fails
                for attempt in range(3):
                    try:
                        await page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")
                        await asyncio.sleep(random.uniform(2, 5))  # Wait for the page to load more content
                        break
                    except Exception as e:
                        if attempt < 2:
                            print(f"Scrolling failed (attempt {attempt + 1}). Retrying...")
                            await asyncio.sleep(5)
                        else:
                            print(f"Failed to scroll after 3 attempts: {e}")

                # Locate ads on the page, including iframes
                ads = page.locator("a[href*='/dp/'][aria-label*='Sponsored'], a.a-link-normal.sp_short_strip_adlink")
                ads_count = await ads.count()
                
                # Click ads found on the main page
                for i in range(ads_count):
                    single_ad = ads.nth(i)
                    
                    # Scroll to ad smoothly, retry if fails
                    for attempt in range(3):
                        try:
                            await single_ad.scroll_into_view_if_needed()
                            await asyncio.sleep(random.uniform(1, 3))  # Random delay before clicking
                            break
                        except Exception as e:
                            if attempt < 2:
                                print(f"Scrolling to ad failed (attempt {attempt + 1}). Retrying...")
                                await asyncio.sleep(2)
                            else:
                                print(f"Failed to scroll to ad after 3 attempts: {e}")
                                continue

                    # Click the ad
                    try:
                        await single_ad.click()
                        click_count += 1
                        log_click_count(click_count)  # Update the log file

                        await asyncio.sleep(random.uniform(5, 10))  # Pause after clicking ad
                        await page.wait_for_load_state("load")  # Wait for the page to load after clicking the ad
                        await page.goto(url)  # Navigate back to the main page
                    except Exception as e:
                        print(f"Error clicking ad: {e}")
                        continue
                
                # Iterate over all frames to find ads within iframes
                for frame in page.frames:
                    try:
                        iframe_ads = frame.locator("a[href*='/dp/'][aria-label*='Sponsored'], a.a-link-normal.sp_short_strip_adlink")
                        iframe_ads_count = await iframe_ads.count()

                        for i in range(iframe_ads_count):
                            iframe_ad = iframe_ads.nth(i)
                            
                            # Scroll to iframe ad smoothly, retry if fails
                            for attempt in range(3):
                                try:
                                    await iframe_ad.scroll_into_view_if_needed()
                                    await asyncio.sleep(random.uniform(1, 3))
                                    break
                                except Exception as e:
                                    if attempt < 2:
                                        print(f"Scrolling to iframe ad failed (attempt {attempt + 1}). Retrying...")
                                        await asyncio.sleep(2)
                                    else:
                                        print(f"Failed to scroll to iframe ad after 3 attempts: {e}")
                                        continue

                            # Click the iframe ad
                            try:
                                await iframe_ad.click()
                                click_count += 1
                                log_click_count(click_count)

                                await asyncio.sleep(random.uniform(5, 10))
                                await page.wait_for_load_state("load")  # Wait for the page to load after clicking the ad
                                await page.goto(url)  # Navigate back to the main page
                            except Exception as e:
                                print(f"Error clicking iframe ad: {e}")
                                continue
                    except Exception as e:
                        print(f"Error interacting with iframe: {e}")
                        continue
                
                if ads_count == 0:
                    print("No ads found on the page. Refreshing...")
                    await page.reload()
                    await asyncio.sleep(random.uniform(2, 5))  # Random pause before retrying
                
            except Exception as e:
                print(f"An error occurred: {e}")
                break

            # Random pause before the next iteration
            await asyncio.sleep(random.uniform(2, 5))  # Random pause between iterations
    finally:
        try:
            if context:
                await context.close()
            if browser:
                await browser.close()
        except Exception as e:
            print(f"Error while closing resources: {e}")

async def main():
    url = 'https://www.amazon.com'
    max_iterations = 10
    async with async_playwright() as playwright:
        await run(playwright, url, max_iterations, timeout=60000)

if __name__ == "__main__":
    asyncio.run(main())