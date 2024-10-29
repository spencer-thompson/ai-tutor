"""
Various Utilities
"""

import logging
import pathlib
import shutil

from bs4 import BeautifulSoup

import streamlit as st

NEW_HEAD_ID = "custom-head-tag"


def inject_header():
    """
    Inject HTML and CSS to preload custom fonts, and customize further
    """
    with open("head.html") as file:
        new_head_html = file.read()

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
        index_path.write_text(new_html)


def style(filename: str = "./styles/main.css"):
    """
    Hide default style and add pretty fonts
    """
    with open(filename, "r") as f:
        css = f.read()
    return f"<style>{css}</style>"


if __name__ == "__main__":
    inject_header()
