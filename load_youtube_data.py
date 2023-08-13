import os
import pandas as pd 
import requests

from yt_dlp import YoutubeDL

from youtube_links import youtube_links

def download_audio(url):
    video_id = url.split("/")[-1]
    filename = f"{video_id}.wav"

    if os.path.exists("filename"):
       os.remove("filename")
        
    with YoutubeDL({'extract_audio': True, 'format': 'bestaudio', 'outtmpl': filename}) as video:
        info_dict = video.extract_info(url, download = True)
        sub_url = info_dict['automatic_captions']['en'][0]['url']

        res = requests.get(sub_url)
        assert res.status_code == 200

        repsonse_json = res.json()

        transcript = ""
        for event in repsonse_json["events"]:
            if transcript:
                transcript += " "
            text_list = event.get('segs')
            if text_list and text_list !=  [{'utf8': '\n'}]:
                for word in text_list:
                    transcript += word['utf8']
    
    return filename, transcript

#TODO add a test to check all the links are the right format pytest
def download_youtube_info(youtube_links):
    # Get data into a mp3 and transript format
    youtube_data = {}
    for url in youtube_links:
        filename, transcript = download_audio(url)
        youtube_data[filename] = transcript
    
    return youtube_data

mp3 = download_youtube_info(youtube_links)

# TODO: don't foeget to delet the files when run
import ipdb
ipdb.set_trace()