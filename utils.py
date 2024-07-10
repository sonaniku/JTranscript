import re
import yt_dlp
from yt_dlp import DownloadError

def validate_ytb_url(url:str)-> bool:
    regex = r"^(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/watch\?v=([a-zA-Z0-9_]+)|youtu\.be\/([a-zA-Z\d_]+))(?:&.*)?$"
    match = re.search(regex,url)
    return True if match else False


def extract_audio_from_yt_video(url):
    # Create a file name based on the video's URL
    filename = r"yt_dl_" + url[-11:] + ".wav"
    # Extract the audio from the video 
    try:
        # Settings
        ydl_opts = {
            'verbose': True,
            'format': 'bestaudio/best',
            'outtmpl': filename,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
            }],
            'compat-options': 'no-certifi',
            'no-check-certificates': True,
        }
        # Download
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        print("\nAudio has been downloaded. Path is :", filename)

    # Handle DownloadError case
    except DownloadError as err:
        # With the default video below, you should not have any problem. But DownloadError can occur with some videos, do not forget to handle it!
        print(err)
        print("\nAudio has not been downloaded. Error occured, please retry.")
        
    return filename
