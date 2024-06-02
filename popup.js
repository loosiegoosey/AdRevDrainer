document.getElementById('start').addEventListener('click', startAutomation);
document.getElementById('stop').addEventListener('click', stopAutomation);

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log('Message received in popup:', message);
  if (message.action === 'updateCount') {
    document.getElementById('adCount').textContent = message.count;
  }
});

function startAutomation() {
  console.log('Starting automation');
  chrome.runtime.sendMessage({action: 'start'}, (response) => {
    if (chrome.runtime.lastError) {
      console.error('Error starting automation:', chrome.runtime.lastError);
    } else {
      console.log('Start message sent successfully:', response);
    }
  });
}

function stopAutomation() {
  console.log('Stopping automation');
  chrome.runtime.sendMessage({action: 'stop'}, (response) => {
    if (chrome.runtime.lastError) {
      console.error('Error stopping automation:', chrome.runtime.lastError);
    } else {
      console.log('Stop message sent successfully:', response);
    }
  });
}
