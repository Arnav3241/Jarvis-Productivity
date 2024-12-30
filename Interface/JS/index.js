// Send a heartbeat to the Python backend every 2 seconds
setInterval(() => {
  eel.Heartbeat();
}, 2000);

function switchToMainWindow() {
    
}

eel.expose();