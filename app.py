import streamlit as st
import requests
import json
import os
import validators
from utils import *

# from css_tricks import _max_width_

# title and favicon ------------------------------------------------------------

st.set_page_config(page_title="Speech to Text Transcription App", page_icon="👄")

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
-   Upload a wav file, transcribe it, then export it to a text file!
-   Use cases: call centres, team meetings, training videos, school calls etc.
	    """
)


url = st.text_input('')

if not url:
    st.info("Please input the url")

try:
    if url:
        if validate_url(url):
            st.video(url)
except:
    st.error('This link is not valid', icon="⚠️")
    