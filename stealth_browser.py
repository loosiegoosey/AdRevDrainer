import random
import time
from playwright.sync_api import sync_playwright

class StealthBrowser:
    def __init__(self, proxy, user_agent):
        self.proxy = proxy
        self.user_agent = user_agent
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(proxy={"server": proxy})
        self.context = self.browser.new_context(user_agent=user_agent)
        self.page = self.context.new_page()

    def navigate_to(self, url):
        self.page.goto(url)

    def find_ads_and_click(self):
        ads = self.page.query_selector_all('.ad-class-selector')
        for ad in ads:
            ad.click()
            self.random_delay()

    def random_delay(self):
        delay = random.uniform(1, 5)
        time.sleep(delay)

# Example usage
if __name__ == '__main__':
    proxies = ["http://proxy1:port", "http://proxy2:port", "http://proxy3:port"]
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
    ]
    proxy = random.choice(proxies)
    user_agent = random.choice(user_agents)
    stealth_browser = StealthBrowser(proxy, user_agent)
    stealth_browser.navigate_to("https://www.amazon.com")
    stealth_browser.find_ads_and_click()
