const { chromium } = require('playwright');
const axios = require('axios');

const proxyAPI = 'https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&country=us&proxy_format=protocolipport&format=text&timeout=2000';
const authAPI = 'https://api.proxyscrape.com/v2/account/datacenter_shared/whitelist';
const authKey = 'nhuyjukilompnbvfrtyuui'; // Your authentication key

async function getProxies() {
  try {
    const response = await axios.get(proxyAPI);
    const proxyList = response.data.split('\n').filter(proxy => proxy.trim() !== '');
    return proxyList.map(proxy => {
      const [ip, port] = proxy.split(':');
      return { ip, port: parseInt(port, 10) };
    }).filter(proxy => proxy.ip && !isNaN(proxy.port)); // Filter out invalid entries
  } catch (error) {
    console.error('Error fetching proxies:', error);
    return [];
  }
}

async function authenticateIP(ip) {
  try {
    await axios.get(authAPI, {
      params: {
        auth: authKey,
        type: 'add',
        ip: [ip]
      }
    });
    console.log(`Authenticated IP: ${ip}`);
  } catch (error) {
    console.error('Error authenticating IP:', error);
  }
}

(async () => {
  const { default: internalIp } = await import('internal-ip'); // Dynamic import for ESM module
  const localIP = await internalIp.v4();
  await authenticateIP(localIP); // Authenticate the local IP first

  let adCount = 0;
  const proxies = await getProxies();

  if (proxies.length === 0) {
    console.error('No proxies available. Exiting...');
    return;
  }

  async function clickAds(browser, proxy) {
    console.log(`Using proxy: http://${proxy.ip}:${proxy.port}`);
    
    let context, page;

    try {
      context = await browser.newContext({
        proxy: { server: `http://${proxy.ip}:${proxy.port}` },
      });
      page = await context.newPage();

      if (!page) {
        throw new Error('Failed to create a new page.');
      }

      await page.goto('https://www.amazon.com/', { waitUntil: 'domcontentloaded' });
      console.log('Navigated to Amazon homepage');

      const adSelectors = [
        'div[id^="desktop-ad-"]',
        'div[data-cel-widget*="adplacements:"]'
      ];

      for (const selector of adSelectors) {
        const ads = await page.$$(selector);
        console.log(`Found ${ads.length} ads with selector ${selector}`);

        for (const ad of ads) {
          const link = await ad.$('a');
          if (link) {
            const href = await link.getAttribute('href');
            if (href) {
              console.log('Clicking on ad:', href);

              const [newPage] = await Promise.all([
                context.waitForEvent('page').catch(() => null), // Catch case where no new page is opened
                link.click()
              ]);

              adCount++;
              console.log('Ad clicked');

              if (newPage) {
                console.log('New tab opened, closing tab');
                await newPage.close();
              }

              console.log('Navigating back to Amazon homepage');
              await page.goto('https://www.amazon.com/', { waitUntil: 'domcontentloaded' });
              console.log('Navigated back to Amazon homepage');

              await page.waitForTimeout(Math.random() * 5000 + 5000); // Random delay between 5-10 seconds
              return;
            }
          }
        }
      }
    } catch (error) {
      console.error('Error during ad clicking:', error);
    } finally {
      if (context) {
        await context.close();
      }
    }
  }

  let browser;
  try {
    browser = await chromium.launch({
      headless: false,
      proxy: { server: 'http://per-context' }
    });
    console.log('Browser launched');
  } catch (error) {
    console.error('Error launching browser:', error);
    return;
  }

  while (true) {
    for (const proxy of proxies) {
      try {
        await clickAds(browser, proxy);
        console.log('Total ads clicked:', adCount);

        // Random delay between switching proxies to further mimic human behavior
        await new Promise(resolve => setTimeout(resolve, Math.random() * 5000 + 2000)); // Random delay between 2-7 seconds
      } catch (error) {
        console.error('Skipping proxy due to error:', error);
      }
    }
  }

  await browser.close();
})();
