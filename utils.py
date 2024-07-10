import re

def validate_ytb_url(url:str)-> bool:
    regex = r"^(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/watch\?v=([a-zA-Z0-9_]+)|youtu\.be\/([a-zA-Z\d_]+))(?:&.*)?$"
    match = re.search(regex,url)
    return True if match else False