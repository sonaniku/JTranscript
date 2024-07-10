import streamlit as st
import requests
import json
import os
from utils import *
import librosa
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer

st.set_page_config(page_title="Speech to Text Transcription App", page_icon=":desktop_computer:")

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
        url = st.text_input('')

        if not url:
            st.info("Please input the url")
    
        if url:
            if validate_ytb_url(url):
                
                st.video(url)
                # processor = AutoProcessor.from_pretrained("datdo/wav2vec2-base-timit-demo-google-colab")
                # model = AutoModelForCTC.from_pretrained("datdo/wav2vec2-base-timit-demo-google-colab")
            
            else:
                st.warning('please check your input link', icon="⚠️")

        audio, rate = librosa.load("The_National_Park.wav",sr=16000)


        tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
        model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

        input_values = tokenizer(audio, return_tensors = "pt").input_values

        logits = model(input_values).logits

        prediction = torch.argmax(logits, dim = -1)

        transcription = tokenizer.batch_decode(prediction)[0]



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

    except:
        st.error(f"""Something went wrong""", icon="⚠️")

    

if __name__ == "__main__":
    main()