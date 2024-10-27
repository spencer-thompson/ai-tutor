"""
Entry point for streamlit
"""

import os
import re
from collections import namedtuple

import requests

import streamlit as st

VERSION = 0.250


if "backend" not in st.session_state:

    def backend_get(endpoint: str = "", data: dict | None = None):  # TODO:
        r = requests.get(url=os.getenv("BACKEND") + endpoint, json=data)
        if r.status_code == 200:
            return r.json()
        else:
            st.warning(f"Error: {r.status_code}")

    def backend_post(endpoint: str = "", data: dict | None = None):
        r = requests.post(url=os.getenv("BACKEND") + endpoint, json=data)
        if r.status_code == 200:
            return r.json()
        else:
            st.warning(f"Error: {r.status_code}")

    st.session_state.backend = namedtuple("Backend", ["get", "post"])(
        backend_get,
        backend_post,
    )  # add more if needed


if "user" not in st.session_state:
    User = namedtuple("User", ["id", "name", "mobile"])
    st.session_state.user = {"mobile": False}
    # HACK: Temporary


if "patterns" not in st.session_state:
    st.session_state.patterns = namedtuple("Pattern", ["mobile"])(
        re.compile(r"[mM]obile|iPhone|iPad|iPod|Android|webOS")
    )  # check mobile


if "layout" not in st.session_state:
    if st.session_state.patterns.mobile.search(st.context.headers["User-Agent"]):
        st.session_state.user["mobile"] = True
        st.session_state.layout = "wide"
    else:
        st.session_state.layout = "centered"


st.set_page_config(
    page_title="AI Tutor",
    page_icon=":mortar_board:",
    layout=st.session_state.layout,
    initial_sidebar_state="collapsed" if st.session_state.user["mobile"] else "expanded",
    menu_items={
        "Get Help": None,  # url
        "Report a bug": None,  # url
        "About": f"""# Version: {VERSION}""",
    },
)


def login():
    st.header("Log in")


def logout():
    pass


account_pages = [
    st.Page(logout, title="Log Out", icon=":material/logout:"),
]
user_pages = [
    st.Page("./page/chat.py", title="Chat", icon=":material/chat:", default=True),
]
dev_pages = [
    st.Page("./page/session_state.py", title="Session State", icon=":material/settings:"),
]

pages = {}

pages["AI"] = user_pages
pages["DEV"] = dev_pages


if len(pages) > 0:
    # pg = st.navigation(pages)
    pg = st.navigation({"Profile": account_pages} | pages)

else:
    pg = st.navigation([st.Page(login)])

pg.run()
