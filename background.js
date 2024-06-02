let intervalID;
let active = false;
let adCount = 0;

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log('Message received in background:', request);
  if (request.action === 'start') {
    active = true;
    adCount = 0;
    console.log('Automation started');
    automationLoop();
    sendResponse({status: 'started'});
  } else if (request.action === 'stop') {
    active = false;
    clearInterval(intervalID);
    console.log('Automation stopped');
    sendResponse({status: 'stopped'});
  }
});

function automationLoop() {
  if (!active) return;

  chrome.tabs.create({url: 'https://www.amazon.com/'}, (tab) => {
    console.log('New tab created:', tab.id);
    chrome.scripting.executeScript({
      target: {tabId: tab.id},
      files: ['content.js']
    }, () => {
      console.log('content.js injected');
      clickAndNavigate(tab.id);
    });
  });
}

function clickAndNavigate(tabId) {
  chrome.scripting.executeScript({
    target: {tabId: tabId},
    function: clickAds
  }, (results) => {
    console.log('Results from clickAds:', results);
    if (results && results[0] && results[0].result) {
      adCount++;
      updatePopupCount();
      setTimeout(() => {
        chrome.tabs.update(tabId, {url: 'https://www.amazon.com/'}, () => {
          if (active) {
            console.log('Navigating to Amazon again');
            automationLoop();
          }
        });
      }, 3000); // Adjust delay as necessary
    }
  });
}

function updatePopupCount() {
  console.log('Updating popup count:', adCount);
  chrome.runtime.sendMessage({action: 'updateCount', count: adCount});
}

function clickAds() {
  console.log('clickAds function called in background');
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
