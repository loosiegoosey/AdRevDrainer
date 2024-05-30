document.getElementById('start').addEventListener('click', startAutomation);
document.getElementById('stop').addEventListener('click', stopAutomation);

function startAutomation() {
  chrome.runtime.sendMessage({action: 'start'});
}

function stopAutomation() {
  chrome.runtime.sendMessage({action: 'stop'});
}
