import streamlit as st
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
        with st.form('Form1'):
            url = st.text_input(label='Enter your url')
            submitted1 = st.form_submit_button('Submit')

        if not url:
            st.warning("Please input the url")
    
        if url:
            if validate_ytb_url(url):
                st.video(url)
                extract_audio_from_yt_video(url = url)
                audio, rate = librosa.load("temp_audio.wav",sr=16000)
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
            else:
                st.warning('please check your input link', icon="⚠️")

        
    except Exception as e:
        st.error(f"""Faced issue: {e}""", icon="⚠️")

    

if __name__ == "__main__":
    main()