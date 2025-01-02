// Send a heartbeat to the Python backend every 2 seconds
setInterval(() => {
  eel.Heartbeat();
}, 2000);

function switchToMainWindow() {
  document.getElementById("Loader").style.display = "none";
}

switchToMainWindow()

eel.expose(switchToMainWindow);