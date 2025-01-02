// Send a heartbeat to the Python backend every 2 seconds
setInterval(() => {
  eel.Heartbeat();
}, 2000);

function switchToVoiceMainWindow() {
  document.getElementById("Loader").style.display = "none";
  document.getElementById("Chat").style.display = "none";
}

function switchToChatMainWindow() {
  document.getElementById("Loader").style.display = "none";
  document.getElementById("Voice").style.display = "none";
}

switchToChatMainWindow()

eel.expose(switchToVoiceMainWindow);
eel.expose(switchToChatMainWindow);