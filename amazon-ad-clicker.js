const { chromium } = require('playwright');
const axios = require('axios');

const proxyAPI = 'https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&country=us&proxy_format=protocolipport&format=text&timeout=2000';
const authAPI = 'https://api.proxyscrape.com/v2/account/datacenter_shared/whitelist';
const authKey = 'nhuyjukilompnbvfrtyuui'; // Your authentication key

async function getProxies() {
  try {
    const response = await axios.get(proxyAPI);
    const proxyList = response.data.split('\n').filter(proxy => proxy.trim() !== '');
    console.log('Proxies fetched:', proxyList.length);
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
  const { internalIpV4 } = await import('internal-ip'); // Correct import for ESM module
  const localIP = await internalIpV4();
  console.log('Local IP:', localIP);
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

      // Use the recorded Playwright actions
      await page.goto('https://www.amazon.com/');
      await page.frameLocator('iframe[name="        \\{\\a             \\"placementName\\" \\:   \\"Gateway_desktop-ad-center-1_desktop\\"\\,\\a             \\"renderingId\\"\\:      \\"ca419b94-3dba-4c23-afa0-57c25ab467f4\\"\\,\\a             \\"creative\\"\\: \\{\\"flow\\"\\:\\"SERVER_SIDE\\"\\,\\a             \\"pageType\\"\\:         \\"Gateway\\"\\,\\a             \\"subPageType\\"\\:      \\"desktop\\"\\,\\a             \\"slotName\\" \\:        \\"desktop-ad-center-1\\"\\,\\a             \\"arid\\" \\:            \\"ec9cb9d85eaf4770bb9115ebbde2ee97\\"\\,\\a                 \\"placementId\\"\\:     \\"73950e1c-6f66-4784-b2d9-e5d5693a4353\\"\\,\\a             \\"size\\" \\:            \\{\\a                                     \\"width\\"\\: \\"970\\"\\,\\a                                     \\"height\\" \\: \\"250\\"\\a                                 \\}\\,\\a             \\"allowedSizes\\" \\:    \\[\\{\\"width\\"\\:\\"970px\\"\\,\\"height\\"\\:\\"250px\\"\\}\\]\\,\\a             \\"allowChangeSize\\"\\:  true\\,\\a             \\"firePixelsAfter\\" \\: \\"amznJQ\\.onCompletion\\:amznJQ\\.x1\\:x1\\"\\,\\a             \\"isCardsFlow\\"\\: false\\,\\a                 \\"aaxImpPixelUrl\\"\\:      \\"https\\:\\/\\/aax-us-iad\\.amazon\\.com\\/e\\/xsp\\/imp\\?b\\=RK1hpu4gmEsw-dlz5nf_giMAAAGPzK2VXgEAAAH0AQBvbm9fdHhuX2JpZDEgICBvbm9fdHhuX2ltcDEgICBO1yT_\\"\\,\\a             \\"aaxInstrPixelUrl\\"\\: \\"https\\:\\/\\/aax-us-iad\\.amazon\\.com\\/x\\/px\\/RK1hpu4gmEsw-dlz5nf_giMAAAGPzK2VXgEAAAH0AQBvbm9fdHhuX2JpZDEgICBvbm9fdHhuX2ltcDEgICBO1yT_\\/\\"\\,\\a                 \\"htmlContentEncoded\\"\\: \\"\\\\u003C\\!doctype html\\>\\\\n\\<html lang\\=\\\\\\"en\\\\\\"\\>\\\\n\\<head\\>\\\\n    \\<meta charset\\=\\\\\\"UTF-8\\\\\\"\\>\\\\n    \\<title\\>\\<\\\\\\/title\\>\\\\n\\<\\\\\\/head\\>\\\\n\\<body style\\=\\\\\\"margin\\:0\\;position\\:absolute\\;top\\:0\\;left\\:0\\;bottom\\:0\\;right\\:0\\;\\\\\\"\\>\\\\n\\<script\\>window\\.t0\\=\\+new Date\\(\\)\\;\\<\\\\\\/script\\>\\\\n\\<script\\>\\\\n    \\\\n\\<\\\\\\/script\\>\\\\n\\\\n\\<div id\\=\\\\\\"ad\\\\\\" style\\=\\\\\\"width\\:100\\%\\;height\\:100\\%\\;\\\\\\"\\>\\<div class\\=\\\\\\"creative-container\\\\\\" style\\=\\\\\\"position\\:absolute\\;top\\:0\\;right\\:0\\;bottom\\:0\\;left\\:0\\;overflow\\:hidden\\\\\\" aria-label\\=\\\\\\"Sponsored Ad\\\\\\" data-reactroot\\=\\\\\\"\\\\\\"\\>\\<img class\\=\\\\\\"ad-background-image mrc-btr-creative\\\\\\" src\\=\\\\\\"https\\:\\/\\/m\\.media-amazon\\.com\\/images\\/S\\/al-na-9d5791cf-3faf\\/154b64bf-a560-45e5-b3bb-ecbe6cebd54e\\._QL25_\\.jpg\\\\\\" style\\=\\\\\\"max-width\\:none\\;max-height\\:none\\;width\\:100\\%\\;height\\:auto\\;margin-left\\:50\\%\\;-webkit-transform\\:translateX\\(-50\\%\\)\\;-moz-transform\\:translateX\\(-50\\%\\)\\;-ms-transform\\:translateX\\(-50\\%\\)\\;-o-transform\\:translateX\\(-50\\%\\)\\;transform\\:translateX\\(-50\\%\\)\\\\\\"\\/\\>\\<div class\\=\\\\\\"border-enforcement\\\\\\" style\\=\\\\\\"position\\:absolute\\;top\\:0\\;right\\:0\\;bottom\\:0\\;left\\:0\\;cursor\\:pointer\\;border\\:1px solid \\#ccc\\\\\\"\\>\\<\\\\\\/div\\>\\<a style\\=\\\\\\"position\\:absolute\\;top\\:0\\;right\\:0\\;bottom\\:0\\;left\\:0\\;cursor\\:pointer\\;background\\:transparent url\\(data\\:image\\/png\\;base64\\,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII\\=\\) repeat 0 0\\\\\\" class\\=\\\\\\"clickthrough\\\\\\" href\\=\\\\\\"https\\:\\/\\/www\\.amazon\\.com\\/Maison-Perrier-Ultimate-Sparkling-Water\\/dp\\/B0CQMZTBZN\\/ref\\=sr_1_1\\?aref\\=GNGvtnoD5w\\&amp\\;aaxitk\\=4f24fe677f7b83d0b03da2156693bf50\\&amp\\;crid\\=1EA03YENNLYNE\\&amp\\;dib\\=eyJ2IjoiMSJ9\\.3aZtl2uuEqNsSn0WycjSHQ\\.Uwpx9a1uVQT-lzTUazuzP-woAmWJfKj8epEJA_o89j4\\&amp\\;dib_tag\\=se\\&amp\\;keywords\\=B0CQMZTBZN\\%2Caps\\%2C124\\&amp\\;sr\\=8-1\\\\\\" target\\=\\\\\\"_top\\\\\\"\\>\\<\\\\\\/a\\>\\<\\\\\\/div\\>\\<\\\\\\/div\\>\\\\n\\<script\\>\\\\n    window\\.\\$ad \\= document\\.getElementById\\(\\\'ad\\\'\\)\\;\\\\n\\<\\\\\\/script\\>\\\\n\\\\n\\<script crossorigin\\=\\\\\\"anonymous\\\\\\" src\\=\\\\\\"https\\:\\/\\/m\\.media-amazon\\.com\\/images\\/I\\/71fELLZCR3L\\.js\\\\\\"\\>\\<\\\\\\/script\\>\\\\n\\\\n\\<script\\>\\\\n    window\\.imageCreative \\= Creative\\.default\\(\\$ad\\, \\{\\\\\\"cta\\\\\\"\\:\\{\\\\\\"linkIn\\\\\\"\\:true\\,\\\\\\"type\\\\\\"\\:\\\\\\"url\\\\\\"\\,\\\\\\"url\\\\\\"\\:\\\\\\"https\\:\\/\\/www\\.amazon\\.com\\/Maison-Perrier-Ultimate-Sparkling-Water\\/dp\\/B0CQMZTBZN\\/ref\\=sr_1_1\\?crid\\=1EA03YENNLYNE\\&dib\\=eyJ2IjoiMSJ9\\.3aZtl2uuEqNsSn0WycjSHQ\\.Uwpx9a1uVQT-lzTUazuzP-woAmWJfKj8epEJA_o89j4\\&dib_tag\\=se\\&keywords\\=B0CQMZTBZN\\&qid\\=1713640690\\&sprefix\\=b0cqmztbzn\\%2Caps\\%2C124\\&sr\\=8-1\\\\\\"\\}\\,\\\\\\"backgroundImage\\\\\\"\\:\\{\\\\\\"url\\\\\\"\\:\\\\\\"https\\:\\/\\/m\\.media-amazon\\.com\\/images\\/S\\/al-na-9d5791cf-3faf\\/154b64bf-a560-45e5-b3bb-ecbe6cebd54e\\.jpg\\\\\\"\\}\\,\\\\\\"adChoicesPosition\\\\\\"\\:\\\\\\"topright\\\\\\"\\,\\\\\\"additionalHtml\\\\\\"\\:\\\\\\"\\\\\\"\\,\\\\\\"impressionUrls\\\\\\"\\:\\[\\]\\,\\\\\\"clickTrackerUrls\\\\\\"\\:\\[\\\\\\"https\\:\\/\\/aax-us-iad\\.amazon\\.com\\/x\\/c\\/RK1hpu4gmEsw-dlz5nf_giMAAAGPzK2VXgEAAAH0AQBvbm9fdHhuX2JpZDEgICBvbm9fdHhuX2ltcDEgICBO1yT_\\/\\\\\\"\\]\\,\\\\\\"isBordered\\\\\\"\\:true\\,\\\\\\"backgroundColor\\\\\\"\\:\\\\\\"\\#ffffff\\\\\\"\\,\\\\\\"width\\\\\\"\\:970\\,\\\\\\"height\\\\\\"\\:250\\,\\\\\\"creativeImageData\\\\\\"\\:null\\,\\\\\\"locale\\\\\\"\\:\\\\\\"US\\\\\\"\\,\\\\\\"region\\\\\\"\\:\\\\\\"na\\\\\\"\\,\\\\\\"mediaCentralPath\\\\\\"\\:\\\\\\"https\\:\\/\\/images-na\\.ssl-images-amazon\\.com\\/images\\/G\\/01\\\\\\"\\,\\\\\\"privacyUrl\\\\\\"\\:\\\\\\"https\\:\\/\\/www\\.amazon\\.com\\/adprefs\\\\\\"\\,\\\\\\"deviceContext\\\\\\"\\:\\{\\\\\\"userAgent\\\\\\"\\:\\\\\\"Mozilla\\/5\\.0 \\(Windows NT 10\\.0\\; Win64\\; x64\\) AppleWebKit\\/537\\.36 \\(KHTML\\, like Gecko\\) Chrome\\/125\\.0\\.0\\.0 Safari\\/537\\.36\\\\\\"\\}\\,\\\\\\"isPreview\\\\\\"\\:null\\,\\\\\\"isMobile\\\\\\"\\:false\\,\\\\\\"isBlackjack\\\\\\"\\:false\\,\\\\\\"isOffsite\\\\\\"\\:false\\,\\\\\\"use1pRendering\\\\\\"\\:false\\,\\\\\\"appendQueryParams\\\\\\"\\:\\\\\\"\\\\\\"\\,\\\\\\"isExternalLink\\\\\\"\\:false\\,\\\\\\"adLink\\\\\\"\\:\\\\\\"https\\:\\/\\/www\\.amazon\\.com\\/Maison-Perrier-Ultimate-Sparkling-Water\\/dp\\/B0CQMZTBZN\\/ref\\=sr_1_1\\?aref\\=GNGvtnoD5w\\&aaxitk\\=4f24fe677f7b83d0b03da2156693bf50\\&crid\\=1EA03YENNLYNE\\&dib\\=eyJ2IjoiMSJ9\\.3aZtl2uuEqNsSn0WycjSHQ\\.Uwpx9a1uVQT-lzTUazuzP-woAmWJfKj8epEJA_o89j4\\&dib_tag\\=se\\&keywords\\=B0CQMZTBZN\\&qid\\=1713640690\\&sprefix\\=b0cqmztbzn\\%2Caps\\%2C124\\&sr\\=8-1\\\\\\"\\,\\\\\\"cascadingIntent\\\\\\"\\:null\\,\\\\\\"isAmazonClickUrl\\\\\\"\\:true\\,\\\\\\"isPrimeNowClickUrl\\\\\\"\\:false\\,\\\\\\"is1pUrlSafe\\\\\\"\\:true\\}\\)\\;\\\\n\\<\\\\\\/script\\>\\\\n\\\\n\\\\n\\<\\\\\\/body\\>\\\\n\\<\\\\\\/html\\>\\\\n\\"\\,\\a                 \\"htmlContentEncodedLength\\"\\: 3483\\,\\a \\a             \\"serverSideFetchAd\\"\\: \\"true\\"\\,\\a             \\"disableResizeFunc\\"\\: true\\,\\a             \\"fallbackStaticAdImgUrl\\"\\: \\"https\\:\\/\\/m\\.media-amazon\\.com\\/images\\/G\\/01\\/GiftCards\\/Consumer\\/multi-product\\/House\\/2022_fallback_HouseAds_1940x500_EN\\.jpg\\"\\,\\a             \\"fallbackStaticAdClickUrl\\"\\: \\"https\\:\\/\\/www\\.amazon\\.com\\/b\\/\\?node\\=2973106011\\"\\,\\a             \\"fallbackStaticAdExtraStyle\\"\\: \\"width\\=100\\% height\\=auto alt\\=\\\\\\"GiftCards\\/Consumer\\/multi-product\\/House\\/2022_fallback_HouseAds_1940x500_EN\\\\\\"\\"\\,\\a             \\"adFeedbackInfo\\"\\:         \\{\\a             \\"adProgramId\\"\\: \\"1002\\"\\, \\a             \\"endPoint\\"\\: \\"\\/af\\/feedback-link\\"\\,\\a             \\"boolFeedback\\"\\: true\\,\\a             \\"sponsoredText\\"\\: \\"Sponsored         \\<b id\\=\\\\\\"ape_Gateway_desktop-ad-center-1_desktop_feedbackIcon\\\\\\" style\\=\\\\\\"display\\: inline-block\\;\\\\n                                         vertical-align\\: text-bottom\\;\\\\n                                         margin\\: 1px 0px\\;\\\\n                                         width\\: 14px\\;\\\\n                                         height\\: 12px\\;\\\\n                                         background\\: url\\(\\\'https\\:\\/\\/m\\.media-amazon\\.com\\/images\\/G\\/01\\/ad-feedback\\/info_icon_1Xsprite\\.png\\\'\\) 0px 0px no-repeat scroll transparent\\;\\\\\\"\\/\\>\\\\n\\"\\,\\a             \\"adFeedbackOnTop\\"\\:false\\a         \\}\\a \\,\\a             \\"adPlacementMetaData\\"\\:         \\{\\a             \\"pageUrl\\"\\: \\"aHR0cHM6Ly93d3cuYW1hem9uLmNvbS8\\/\\"\\,\\a             \\"adElementId\\"\\: \\"ape_Gateway_desktop-ad-center-1_desktop_placement\\"\\,\\a             \\"pageType\\"\\: \\"Gateway\\"\\,\\a             \\"slotName\\"\\: \\"desktop-ad-center-1\\"\\a         \\}\\a \\,\\a             \\"adCreativeMetaData\\"\\:         \\{\\a             \\"adProgramId\\"\\: \\"1002\\"\\,\\a             \\"adCreativeTemplateName\\"\\: \\"Standard Display\\"\\,\\a             \\"adImpressionId\\"\\: \\"https\\:\\/\\/aax-us-iad\\.amazon\\.com\\/e\\/xsp\\/imp\\?b\\=RK1hpu4gmEsw-dlz5nf_giMAAAGPzK2VXgEAAAH0AQBvbm9fdHhuX2JpZDEgICBvbm9fdHhuX2ltcDEgICBO1yT_\\"\\,\\a             \\"adCreativeId\\"\\: \\"588819611015902692\\"\\,\\a             \\"adId\\"\\: \\"581723488290944778\\"\\,\\a             \\"adCreativeDetails\\"\\: \\[\\]\\,\\a             \\"adNetwork\\"\\: \\"cs\\"\\a         \\}\\a \\,\\a             \\"advertisementStyle\\"\\:     \\{\\a         \\"position\\"\\: \\"absolute\\"\\,\\a         \\"top\\"\\: \\"4\\.5px\\"\\,\\a         \\"right\\"\\: \\"0px\\"\\,\\a         \\"display\\"\\: \\"inline-block\\"\\,\\a         \\"font\\"\\: \\"11px \\\\\\"Amazon Ember Regular\\\\\\"\\, \\\\\\"Amazon Ember\\\\\\"\\, Arial\\"\\,\\a         \\"color\\"\\: \\"rgb\\(85\\,85\\,85\\)\\"\\,\\a         \\"text-align\\"\\: \\"right\\"\\a     \\}\\a \\,\\a             \\"feedbackDivStyle\\"\\: \\{\\"position\\"\\:\\"relative\\"\\,\\"height\\"\\:\\"17px\\"\\,\\"top\\"\\:\\"0px\\"\\}\\,\\a             \\"abpStatus\\"\\: \\"0\\"\\,\\a             \\"abpAcceptable\\"\\: \\"true\\"\\,\\a                 \\"mediaType\\"\\: \\"D\\"\\,\\a                 \\"brandNameEncoded\\"\\: \\"Maison Perrier\\"\\,\\a             \\"adUnitPlacementId\\"\\:\\"ape_Gateway_desktop-ad-center-1_desktop_placement\\"\\,\\a             \\"adUnitIframeId\\"\\:\\"ape_Gateway_desktop-ad-center-1_desktop_iframe\\"\\,\\a             \\"weblabTreatments\\"\\:\\"\\{\\\\\\"ADPT_SF_LIGHTADS_REFACTOR_903064\\\\\\"\\:\\\\\\"C\\\\\\"\\,\\\\\\"ADPT_SF_ADSP_VIDEO_833419\\\\\\"\\:\\\\\\"C\\\\\\"\\,\\\\\\"ADPT_SF_CLIENT_LATENCY_2023Q1_632539\\\\\\"\\:\\\\\\"C\\\\\\"\\,\\\\\\"ADPT_SF_CLIENT_LATENCY_2023Q3_737747\\\\\\"\\:\\\\\\"C\\\\\\"\\,\\\\\\"ADPT_SF_TEMPLATE_PARAMETER_CLASS_906958\\\\\\"\\:\\\\\\"C\\\\\\"\\,\\\\\\"ADPT_SF_APE_WW_MOBILE_SEARCH_ZOETROPE_EPB_EXP_792200\\\\\\"\\:\\\\\\"C\\\\\\"\\,\\\\\\"ADPT_SF_SPARKLE_838607\\\\\\"\\:\\\\\\"C\\\\\\"\\,\\\\\\"ADPT_SF_H1_VIDEO_ADS_MOCK_940184\\\\\\"\\:\\\\\\"C\\\\\\"\\,\\\\\\"ADPT_SF_ADREPORTER_REFACTOR_973426\\\\\\"\\:\\\\\\"C\\\\\\"\\,\\\\\\"ADPT_SF_RESIZE_ASPECT_RATIO_909226\\\\\\"\\:\\\\\\"C\\\\\\"\\,\\\\\\"ADPT_SF_H1_VIDEO_ADS_835424\\\\\\"\\:\\\\\\"C\\\\\\"\\,\\\\\\"ADPT_SF_DEFAULT_SPONSORED_LABEL_863363\\\\\\"\\:\\\\\\"C\\\\\\"\\,\\\\\\"ADPT_SF_DOCWRITE_689243\\\\\\"\\:\\\\\\"T1\\\\\\"\\,\\\\\\"ADPT_SF_TRANSPARENCY_INFO_MANDATORY_FOR_EU_712921\\\\\\"\\:\\\\\\"C\\\\\\"\\}\\"\\a         \\}\\a "]').getByRole('link').click();
      adCount++;
      console.log('Ad clicked');

      console.log('Navigating back to Amazon homepage');
      await page.goto('https://www.amazon.com/', { waitUntil: 'domcontentloaded' });
      console.log('Navigated back to Amazon homepage');

      await page.waitForTimeout(Math.random() * 5000 + 5000); // Random delay between 5-10 seconds
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
