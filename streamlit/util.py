"""
Various Utilities
"""

import logging
import pathlib
import shutil
from datetime import datetime, timedelta

from bs4 import BeautifulSoup

import streamlit as st

# import streamlit.components.v1.html as html

html = st.components.v1.html

NEW_HEAD_ID = "custom-head-tag"


def inject_header():
    """
    Inject HTML and CSS to preload custom fonts, and customize further
    """
    with open("head.html") as file:
        new_head_html = file.read()

    with open("styles/main.css") as styles:
        new_styles = styles.read()

    index_path = pathlib.Path(st.__file__).parent / "static" / "index.html"
    logging.info(f"Editing {index_path}")
    soup = BeautifulSoup(index_path.read_text(), features="lxml")
    if not soup.find(id=NEW_HEAD_ID):  # if cannot find tag
        bck_index = index_path.with_suffix(".bck")
        if bck_index.exists():
            shutil.copy(bck_index, index_path)  # recover from backup
        else:
            shutil.copy(index_path, bck_index)  # keep a backup
        html = str(soup)
        new_html = html.replace("<head>", "<head>\n" + new_head_html)
        new_html = new_html.replace("<title>Streamlit</title>", "<title>AI Tutor</title>")
        new_html = new_html.replace("</head>", f"<style>{new_styles}</style>\n</head>")
        index_path.write_text(new_html)


def style(filename: str = "./styles/main.css"):
    """
    Hide default style and add pretty fonts
    """
    with open(filename, "r") as f:
        css = f.read()
    return f"<style>{css}</style>"


def set_cookie(key: str, value: str, days: int):
    current_date = datetime.now()
    expiration = current_date + timedelta(days=days)
    cookie_expiration = expiration.strftime("%a, %d %b %Y %H:%M:%S GMT")
    html(f"<script>document.cookie = '{key}={value}; expires={cookie_expiration}; path=/';</script>", width=0, height=0)


def delete_cookie(key: str):
    current_date = datetime.now()
    expiration = current_date - timedelta(days=100)
    cookie_expiration = expiration.strftime("%a, %d %b %Y %H:%M:%S GMT")
    html(f"<script>document.cookie = '{key}=; expires={cookie_expiration}; path=/';</script>", width=0, height=0)


def set_storage(key: str, value: str):
    html(f"<script>localStorage.setItem('{key}', '{value}')</script>", width=0, height=0)


# def get_storage(key: str):
#     html(f"<script>localStorage.setItem('{key}', '{value}')</script>", width=0, height=0)


def remove_storage():
    pass


def clear_storage():
    pass


if __name__ == "__main__":
    inject_header()
