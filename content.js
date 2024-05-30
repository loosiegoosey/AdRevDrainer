chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'clickAds') {
      clickAds();
    }
  });
  
  function clickAds() {
    const ads = document.querySelectorAll('a[href*="/gp/slredirect/"]');
    ads.forEach(ad => {
      window.open(ad.href, '_blank');
    });
  }
  