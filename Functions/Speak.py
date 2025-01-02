# Using TicTok TTS:

from playsound import playsound
import requests
import base64
import uuid
import json
import os
import re

alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = r"(Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov|edu|me)"
digits = "([0-9])"
multiple_dots = r'\.{2,}'

def split_into_sentences(text: str) -> list[str]:
  text = " " + text + "  "
  text = text.replace("\n"," ")
  text = re.sub(prefixes,"\\1<prd>",text)
  text = re.sub(websites,"<prd>\\1",text)
  text = re.sub(digits + "[.]" + digits,"\\1<prd>\\2",text)
  text = re.sub(multiple_dots, lambda match: "<prd>" * len(match.group(0)) + "<stop>", text)
  if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
  # text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
  text = re.sub(r"\s" + alphabets + r"[.] ", r" \1<prd> ", text)
  text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
  text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
  text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
  text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
  text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
  text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
  if "”" in text: text = text.replace(".”","”.")
  if "\"" in text: text = text.replace(".\"","\".")
  if "!" in text: text = text.replace("!\"","\"!")
  if "?" in text: text = text.replace("?\"","\"?")
  text = text.replace(".",".<stop>")
  text = text.replace("?","?<stop>")
  text = text.replace("!","!<stop>")
  text = text.replace("<prd>",".")
  sentences = text.split("<stop>")
  sentences = [s.strip() for s in sentences]
  if sentences and not sentences[-1]: sentences = sentences[:-1]
  return sentences

def text_to_speech(api_endpoint, text, voice, request_data_key, verbose=False):
  """
  Available Voice Options:
    - en_au_001
    - en_male_narration
    - en_male_funny
    - en_male_cody
    - en_female_emotional
    - en_us_rocket
    - en_female_f08_salut_damour
  """
  
  voice_options = (
      "en_au_001", "en_male_narration", "en_male_funny", "en_male_cody",
      "en_female_emotional", "en_us_rocket", "en_female_f08_salut_damour",
  )
  
  if voice not in voice_options: 
    raise ValueError(f"Invalid voice option '{voice}'. Available options are: {', '.join(voice_options)}")

  headers = {"Content-Type": "application/json"}
  request_data = {"text": text, "voice": voice}
  response = requests.post(api_endpoint, headers=headers, data=json.dumps(request_data))

  if response.status_code == 200:
    filename = f"Database/Audio/output_{uuid.uuid4().hex[:8]}.mp3"
    with open(filename, "wb") as output_file:
      output_file.write(base64.b64decode(response.json()[request_data_key]))
    if verbose:
      print(f"Speech synthesis successful. Output saved to '{filename}'")
    playsound(filename)
    try:
      os.remove(filename)
      if verbose:
        print(f"Temporary file '{filename}' deleted successfully.")
    except OSError as e:
      print(f"Error deleting file '{filename}': {e}")
  else:
    print(f"Error: Request failed with status code {response.status_code}. Response: {response.text}")

def Speak(Text, Voice):
  weilbyte_api_endpoint = "https://tiktok-tts.weilnet.workers.dev/api/generation"
  Sentences = split_into_sentences(Text)
  
  for Sentence in Sentences:
    print(f"Currently speaking: {Sentence}")
    text_to_speech(weilbyte_api_endpoint, Sentence, Voice, "data")

if __name__ == "__main__":
  Speak("Despite the heavy rain, which made the streets slippery and difficult to navigate, and the loud thunder that echoed across the city, we managed to continue our journey, passing by old buildings that had seen countless generations come and go, while the sound of distant conversations and the rustle of leaves in the trees filled the air, creating a mix of tranquility and excitement, as we ventured forward, unsure of what lay ahead but certain that every step we took would bring us closer to our destination, wherever that might be, in this unpredictable and fascinating world.", "en_male_cody")
