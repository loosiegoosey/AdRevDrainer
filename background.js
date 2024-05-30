let intervalID;
let active = false;
let adCount = 0;

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'start') {
    active = true;
    adCount = 0;
    automationLoop();
  } else if (request.action === 'stop') {
    active = false;
    clearInterval(intervalID);
  }
});

function automationLoop() {
  if (!active) return;

  chrome.tabs.create({url: 'https://www.amazon.com/'}, (tab) => {
    chrome.scripting.executeScript({
      target: {tabId: tab.id},
      files: ['content.js']
    }, () => {
      clickAndNavigate(tab.id);
    });
  });
}

function clickAndNavigate(tabId) {
  chrome.scripting.executeScript({
    target: {tabId: tabId},
    function: clickAds
  }, (results) => {
    if (results && results[0] && results[0].result) {
      adCount++;
      updatePopupCount();
      setTimeout(() => {
        chrome.tabs.update(tabId, {url: 'https://www.amazon.com/'}, () => {
          if (active) {
            automationLoop();
          }
        });
      }, 3000); // Adjust delay as necessary
    }
  });
}

function updatePopupCount() {
  chrome.runtime.sendMessage({action: 'updateCount', count: adCount});
}

function clickAds() {
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
        window.location.href = link.href;
        clicked = true;
      }
    });
  });

  return clicked;
}
