import re
import yt_dlp
from yt_dlp import DownloadError

def validate_ytb_url(url:str)-> bool:
    regex = r"^(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/watch\?v=([a-zA-Z0-9_]+)|youtu\.be\/([a-zA-Z\d_]+))(?:&.*)?$"
    match = re.search(regex,url)
    return True if match else False


def extract_audio_from_yt_video(url):
    # Create a file name based on the video's URL
    filename = r"yt_dl_" + url[-11:]
    # Extract the audio from the video 
    try:
        # Settings
        ydl_opts = {
            'verbose': True,
            'format': 'bestaudio/best',
            'outtmpl': filename,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '192',
            }],
            'compat-options': 'no-certifi',
            'no-check-certificates': True,
        }
        # DownloadS
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        print("\nAudio has been downloaded. Path is :", filename)

    # Handle DownloadError case
    except Exception as e:
        raise Exception(f"""Dowload failed due to: {e}""")
    
    return filename+'.wav'

