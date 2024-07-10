import streamlit as st
import re
import requests
import json
import os
import validators
from utils import *
from transformers import AutoProcessor, AutoModelForCTC


# from css_tricks import _max_width_

# title and favicon ------------------------------------------------------------

st.set_page_config(page_title="Speech to Text Transcription App", page_icon=":desktop_computer:")

# _max_width_()

# logo and header -------------------------------------------------

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


url = st.text_input('')

if not url:
    st.info("Please input the url")

try:
    if url:
        if validate_ytb_url(url):
            st.video(url)
            processor = AutoProcessor.from_pretrained("datdo/wav2vec2-base-timit-demo-google-colab")
            model = AutoModelForCTC.from_pretrained("datdo/wav2vec2-base-timit-demo-google-colab")
        else:
            st.warning('please check your input link', icon="⚠️")
except:
    st.error(f"""Something went wrong""", icon="⚠️")
    