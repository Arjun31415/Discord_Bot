import base64  # inbuilt module for encoding and decodingto base64
import re

import markdown
from bs4 import BeautifulSoup  # pip install beautifulsoup4


def md_to_text(md):
    html = markdown.markdown(md)
    soup = BeautifulSoup(html, features='html.parser')
    return soup.get_text()


def substring_range(s, substring):
    for i in re.finditer(re.escape(substring), s):
        return (i.start(), i.end())


def encode(text: str):
    text_bytes = text.encode('utf-8')
    base64_bytes = base64.b64encode(text_bytes)
    base64_string = base64_bytes.decode("utf-8")
    return base64_string


def decode(b64_string: str):
    base64_bytes = b64_string.encode("utf-8")

    sample_string_bytes = base64.b64decode(base64_bytes)
    sample_string = sample_string_bytes.decode("utf-8")
    return sample_string
