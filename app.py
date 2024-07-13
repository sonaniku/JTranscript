import streamlit as st
import time
import os
from utils import *
import librosa
import torch
import ffmpeg
from transformers import AutoModelForCTC, AutoProcessor

st.set_page_config(page_title="Speech to Text Transcription App", page_icon=":desktop_computer:", layout="wide")

st.text("")
st.image(
    "https://emojipedia-us.s3.amazonaws.com/source/skype/289/parrot_1f99c.png",
    width=125,
)
st.title("Speech to text transcription app")
st.write(
    """  
-   Input youtube url, transcribe it, then export it to a text file!
        """
)

    
def main():
    try:
        with st.form('Form1'):
            url = st.text_input(label='Enter your url')
            submitted1 = st.form_submit_button('Submit')

        if not url:
            st.warning("Please input the url")
    
        if url:
            if validate_ytb_url(url):
                st.video(url)

                with st.spinner('Extracting video...'):
                    video =  extract_audio_from_yt_video(url)
                    time.sleep(5)
                st.success("Extracted successfully")

                if os.path.exists(video):
                    audio, rate = librosa.load("yt_dl_BI3yTjBI3ag.mp3",sr=16000)
                    tokenizer = AutoProcessor.from_pretrained("facebook/wav2vec2-large-960h-lv60-self")
                    model = AutoModelForCTC.from_pretrained("facebook/wav2vec2-large-960h-lv60-self")
                    input_values = tokenizer(audio, return_tensors = "pt").input_values
                    logits = model(input_values).logits
                    prediction = torch.argmax(logits, dim = -1)
                    transcription = tokenizer.batch_decode(prediction)[0]
                    word_start_times, word_end_times, words = get_timestamp_for_each_world(tokenizer, input_values, rate, prediction, transcription) 
                    csv_file = write_to_csv(word_start_times, word_end_times, words)
                    srt_data = generate_srt(csv_file)
                    with open(f"transcript.srt", "w") as srt_file:
                        for row in srt_data:
                            srt_file.write(row)
                            

                    with st.expander("View Transcript"):
                        button = st.download_button( label="Download Transcript",
                                                            data = transcription,
                                                            file_name="transcript.txt",)
                        st.info(transcription)
                        if button:
                            envir_var = os.environ
                            user_loc = envir_var.get('USERPROFILE')
                            loc = user_loc+"\Downloads\\transcript.txt"
                            with open(loc,'w') as video_file:
                                video_file.write(transcription)
            else:
                st.warning('please check your input link', icon="⚠️")
    except Exception as e:
        st.error(f"""Faced issue: {e}""", icon="⚠️")

    

if __name__ == "__main__":
    main()