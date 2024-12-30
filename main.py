"""
Made by Arnav Singh (https://github.com/Arnav3241) with 💖
"""
import multiprocessing
import threading
import time
import eel
import sys
import os

# Important Variables:
ChatPause = multiprocessing.Value("b", False)
Last_Heartbeat = time.time()
voice = []

CWD = os.getcwd()

# Functions to check if the web app is still alive: 
@eel.expose
def Heartbeat():
  global Last_Heartbeat
  Last_Heartbeat = time.time()

def Monitor_Heartbeat(process, timeout=5):
  global Last_Heartbeat; time.sleep(3)
  
  while True:
    time.sleep(1)
    
    if time.time() - Last_Heartbeat > timeout:
      print("\n💻: Browser window closed. Cleaning up...")
      if process.is_alive(): process.terminate(); print("🛑: VoiceChat process terminated.")
      sys.exit(0)


def VoiceChat(pause_var):
  from WebSpeechRecognition import SpeechRecognition
  
  recogniser = SpeechRecognition(f"{CWD}/Drivers/chromedriver.exe", language="en-US")
  recogniser.Init()
  
  while True:
    print("Running")


if __name__ == "__main__":
  eel.init("Interface")
  
  VoiceExeProcess = multiprocessing.Process(target=VoiceChat, args=(ChatPause,))
  VoiceExeProcess.start()
  
  heartbeat_thread = threading.Thread(target=Monitor_Heartbeat, args=(VoiceExeProcess, 3))
  heartbeat_thread.daemon = True
  heartbeat_thread.start()
  
  try: eel.start("index.html", size=(1500, 1200), port=8080)
  except Exception as e: 
    print(f"\n💀: Jarvis has encountered a fatal error. Please try later. Error: {e}")
    if VoiceExeProcess.is_alive(): VoiceExeProcess.terminate()