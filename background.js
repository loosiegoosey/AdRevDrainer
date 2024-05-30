let intervalID;
let active = false;

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'start') {
    active = true;
    automationLoop();
  } else if (request.action === 'stop') {
    active = false;
    clearInterval(intervalID);
  }
});

function automationLoop() {
  if (!active) return;

  chrome.tabs.create({url: 'https://www.amazon.com/'}, (tab) => {
    chrome.tabs.executeScript(tab.id, {file: 'content.js'}, () => {
      openAds();
      intervalID = setInterval(() => {
        closeTabs(() => {
          chrome.tabs.update(tab.id, {url: 'https://www.amazon.com/'});
        });
      }, 10000); // Adjust time as necessary
    });
  });
}

function openAds() {
  chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
    chrome.tabs.sendMessage(tabs[0].id, {action: 'clickAds'});
  });
}

function closeTabs(callback) {
  chrome.tabs.query({}, (tabs) => {
    for (let tab of tabs) {
      if (tab.url !== 'https://www.amazon.com/') {
        chrome.tabs.remove(tab.id);
      }
    }
    if (callback) callback();
  });
}
