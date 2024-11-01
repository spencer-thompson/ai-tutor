"""
Entry point for streamlit
"""

import json
import os
import re
from collections import namedtuple

import requests

import streamlit as st

VERSION = 1.000

if "backend" not in st.session_state:  # maybe change to a class?
    base_url = os.getenv("BACKEND")
    headers = {
        os.getenv("BACKEND_API_KEY_NAME"): os.getenv("BACKEND_API_KEY"),
    }

    def backend_get(endpoint: str = "", data: dict | None = None):
        r = requests.get(url=base_url + endpoint, headers=headers, json=data)
        if r.status_code == 200:
            return r.json()
        else:
            st.warning(f"Error: {r.status_code}")

    def backend_post(endpoint: str = "", data: dict | None = None):
        r = requests.post(url=base_url + endpoint, headers=headers, json=data)
        if r.status_code == 200:
            return r.json()
        else:
            st.warning(f"Error: {r.status_code}")

    def backend_post_stream(endpoint: str = "", data: dict | None = None):
        r = requests.post(url=base_url + endpoint, headers=headers, json=data, stream=True)
        r.raise_for_status()
        for chunk in r.iter_content(chunk_size=None, decode_unicode=True):
            if chunk:
                try:
                    yield json.loads(chunk)
                except UnicodeDecodeError as e:
                    st.error(e)

    st.session_state.backend = namedtuple("Backend", ["get", "post", "post_stream"])(
        backend_get,
        backend_post,
        backend_post_stream,
    )


if "user" not in st.session_state:
    User = namedtuple("User", ["id", "name", "mobile"])
    st.session_state.user = {"mobile": False, "role": None, "id": "1", "user": "test_user"}
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
    initial_sidebar_state="collapsed" if st.session_state.user["mobile"] else "auto",
    menu_items={
        "Get Help": None,  # url
        "Report a bug": None,  # url
        "About": f"""# Version: {VERSION}""",
    },
)


def login():
    st.header("Log In")
    if st.button("login"):
        st.session_state.user["role"] = "dev"
        st.rerun()
    else:
        st.stop()


def logout():
    del st.session_state.user
    st.rerun()


account_pages = [
    st.Page(logout, title="Log Out", icon=":material/logout:"),
]
user_pages = [
    st.Page("./page/chat.py", title="Chat", icon=":material/chat:", default=True),
]
info_pages = [
    st.Page("./page/about.py", title="About", icon=":material/info:"),
]
dev_pages = [
    st.Page("./page/session_state.py", title="Session State", icon=":material/settings:"),
]

pages = {}

if st.session_state.user["role"] in ["normal", "admin"]:
    pages["AI"] = user_pages
    pages["INFO"] = info_pages


if st.session_state.user["role"] in ["dev"]:
    pages["AI"] = user_pages
    pages["INFO"] = info_pages
    pages["DEV"] = dev_pages


if len(pages) > 0:
    pg = st.navigation({"PROFILE": account_pages} | pages, expanded=True)

else:
    pg = st.navigation([st.Page(login)], expanded=True)

pg.run()

st.sidebar.caption(f"* AI Tutor Version: :green-background[{VERSION}]")
