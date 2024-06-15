#googletrans-3.1.0a0
from fastapi import FastAPI
from bs4 import BeautifulSoup
import requests, lxml
from typing import Optional
from pydub import AudioSegment
import speech_recognition as sr
from gtts import gTTS
from fastapi.responses import FileResponse

from fastapi import FastAPI, File, UploadFile
import googletrans
from googletrans import Translator
from fastapi.middleware.cors import CORSMiddleware
translator = Translator()
import shutil
import os
lan = googletrans.LANGUAGES
#print(lan)
keys = list(lan.keys())
vals = list(lan.values())


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/text-to-speech/{text}")
def text_to_speech(text: str):
    tts = gTTS(text)
    audio_file = 'text_to_speech.mp3'
    tts.save(audio_file)
    return FileResponse(audio_file, media_type='audio/mpeg')

@app.post("/speech-to-text/")
async def speech_to_text(audio_file: UploadFile = File(...), lang: Optional[str] = "en-US"):
    file_location = audio_file.filename
    with open(file_location, "wb") as file_object:
        shutil.copyfileobj(audio_file.file, file_object)
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_location) as source:
        audio = recognizer.record(source)
    os.remove(file_location)
    text = recognizer.recognize_google(audio, language=lang)
    return {"text": text}


@app.post("/translators/")
async def tra(sentence,lang):
        lang = lang.lower()
        return translator.translate(sentence,dest=keys[vals.index(lang)]).text


from hugchat import hugchat
from hugchat.login import Login
# Log in to huggingface and grant authorization to huggingchat


@app.post("/chat/{keyword}")
async def video(keyword):
    sign = Login("arafathbict@gmail.com", "Bict@100")
    cookies = sign.login()
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    bot_message = chatbot.chat(keyword)
    return str(bot_message).replace("\n", "<br>")
    

    

from woocommerce import API

wcapi = API(
    url="https://nsautotrading.co.uk",
    consumer_key="ck_05994a5bb7046e5da665ab8708d51a488236f922",
    consumer_secret="cs_20c4803581ed724f850ffd2ce34fcf1c8339cb68",
    version="wc/v3"
)

@app.post("/woo_make_order/")
def make_order(data:dict):
    print(type(data))
    return wcapi.post("orders", data).json()
        

@app.post("/video/{keyword}")
async def video(keyword):
       headers = {
           "User-Agent":
           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
       }

       params = {
           "q": keyword,"count":200
           #"cc": "us" # language/country of the search
       }

       html = requests.get('https://www.bing.com/videos/search', params=params, headers=headers)
       soup = BeautifulSoup(html.text, 'lxml')
       data=[]
       for result in soup.select('.mc_vtvc.b_canvas'):
              try:
                   d={}
                   d["title"] = result.select_one('.b_promtxt').text
                   d["link"] = f"https://www.bing.com{result.select_one('.mc_vtvc_link')['href']}"
                   d["views"] = result.select_one('.mc_vtvc_meta_row:nth-child(1) span:nth-child(1)').text
                   d["date"] = result.select_one('.mc_vtvc_meta_row:nth-child(1) span+ span').text
                   d["video_platform"] = result.select_one('.mc_vtvc_meta_row+ .mc_vtvc_meta_row span:nth-child(1)').text
                   d["channel_name"] = result.select_one('.mc_vtvc_meta_row_channel').text
                   img = str(result.select_one('.mc_vtvc_con_rc' )).split(",")[3].replace('"turl":"',"")
                   d["tump_img"] = img.replace('"',"")
                   data.append(d)
                   #c=0
                   #for i in img:
                       #print(c)
                       #print(i)
                       #c=c+1
                 
              except:
                   print()
       for i in data[7:25]:
              data.append(i)
       return {"video":data}

# for run the api uvicorn translator_api:app
