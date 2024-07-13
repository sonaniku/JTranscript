import re
import yt_dlp
import pandas as pd
from itertools import groupby
import tokenizers
import time
import csv

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
                'preferredcodec': 'mp3',
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
    
    return filename+'.mp3'

def get_timestamp_for_each_world(tokenizer, input_values, rate, prediction, transcription):
    words = [w for w in transcription.split(' ') if len(w) > 0]
    prediction = prediction[0].tolist()
    duration_sec = input_values.shape[1] / rate
    ids_w_time = [(i / len(prediction) * duration_sec, _id) for i, _id in enumerate(prediction)]
    # remove entries which are just "padding" (i.e. no characers are recognized)
    ids_w_time = [i for i in ids_w_time if i[1] != tokenizer.tokenizer.pad_token_id]
    # now split the ids into groups of ids where each group represents a word
    split_ids_w_time = [list(group) for k, group
                        in groupby(ids_w_time, lambda x: x[1] == tokenizer.tokenizer.word_delimiter_token_id)
                        if not k]
    word_start_times = []
    word_end_times = []
    for cur_ids_w_time, cur_word in zip(split_ids_w_time, words):
        _times = [_time for _time, _id in cur_ids_w_time]
        word_start_times.append(min(_times))
        word_end_times.append(max(_times))
        
    return word_start_times, word_end_times, words

def formattedtime(seconds):
    final_time = time.strftime("%H:%M:%S", time.gmtime(float(seconds)))
    return f"{final_time},{seconds.split('.')[1]}"

def write_to_csv(word_start_times, word_end_times, words):
    csv_file = "transcript.csv"
    
    start = [formattedtime(format(i, ".3f")) for i in word_start_times]
    end = [formattedtime(format(i, ".3f")) for i in word_end_times]
    df = pd.DataFrame({'start_times': start, 'end_time': end, 'text': words})
    df.to_csv(csv_file, encoding='utf-8', index=False, header=True)
    return csv_file


def generate_srt(csv_file):
    rows = []
    count = 0
    with open(csv_file) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            count += 1
            txt = f"""{count}\n{row["start_times"]} --> {row["end_time"]}\n{row["text"].strip()}\n\n"""
            rows.append(txt)

    return rows