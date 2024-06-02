function clickAds() {
  console.log('clickAds function called');
  const adSelectors = [
    'div[id^="desktop-ad-"]',
    'div[data-cel-widget*="adplacements:"]'
  ];

  let clicked = false;

  adSelectors.forEach(selector => {
    if (clicked) return;

    const ads = document.querySelectorAll(selector);
    ads.forEach(ad => {
      if (clicked) return;

      const link = ad.querySelector('a');
      if (link && link.href) {
        console.log('Ad clicked:', link.href);
        window.location.href = link.href;
        clicked = true;
      }
    });
  });

  return clicked;
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log('Message received in content script:', request);
  if (request.action === 'clickAds') {
    const result = clickAds();
    sendResponse({result: result});
  }
});
