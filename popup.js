document.getElementById('start').addEventListener('click', startAutomation);
document.getElementById('stop').addEventListener('click', stopAutomation);

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'updateCount') {
    document.getElementById('adCount').textContent = message.count;
  }
});

function startAutomation() {
  chrome.runtime.sendMessage({action: 'start'});
}

function stopAutomation() {
  chrome.runtime.sendMessage({action: 'stop'});
}
