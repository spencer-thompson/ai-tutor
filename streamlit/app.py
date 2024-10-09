"""
Entry point for streamlit
"""

import re
from collections import namedtuple

import streamlit as st

VERSION = 0.250

# two collections, one for users, one for classes

if "patterns" not in st.session_state:
    st.session_state.patterns = namedtuple("Pattern", ["mobile"])(
        re.compile(r"[mM]obile|iPhone|iPad|iPod|Android|webOS")
    )  # check mobile


if "user" not in st.session_state:
    User = namedtuple("User", ["id", "name", "mobile"])

if "layout" not in st.session_state:
    if st.session_state.patterns.mobile.search(st.context.headers["User-Agent"]):
        st.session_state.user.mobile = True
        st.session_state.layout = "wide"
    else:
        st.session_state.layout = "centered"


st.set_page_config(
    page_title="AI Tutor",
    page_icon=":mortar_board:",
    layout=st.session_state.layout,
    initial_sidebar_state="collapsed" if st.session_state.user.mobile else "expanded",
    menu_items={
        "Get Help": None,  # url
        "Report a bug": None,  # url
        "About": f"""# Version: {VERSION}""",
    },
)

usr_pages = []
dev_pages = []

pages = {}

pages["AI"] = [st.Page("chat.py", title="Chat", icon=":material/chat:", default=True)]


pg = st.navigation(pages)

pg.run()
