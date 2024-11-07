"""
Entry point for streamlit
"""

import json
import os
import re
from collections import namedtuple

import requests

import streamlit as st

# import streamlit.components.v1.html as html

VERSION = 1.000

if "token" not in st.session_state:
    st.session_state.token = st.context.cookies.get("token")

if "backend" not in st.session_state:  # maybe change to a class?
    base_url = os.getenv("BACKEND")
    headers = {
        os.getenv("BACKEND_API_KEY_NAME"): os.getenv("BACKEND_API_KEY"),
    }
    if st.session_state.token:
        headers = headers | {"Authorization": f"Bearer {st.session_state.token}"}

    def backend_get(endpoint: str = "", data: dict | None = None):
        r = requests.get(url=base_url + endpoint, headers=headers, json=data)
        r.raise_for_status()
        return r.json()

        # if r.status_code == 200:
        #     return r.json()
        # else:
        #     st.warning(f"Error: {r.status_code}")
        #     return r.json()

    def backend_post(endpoint: str = "", data: dict | None = None):
        r = requests.post(url=base_url + endpoint, headers=headers, json=data)
        if r.status_code == 200:
            return r.json()
        else:
            st.warning(f"Error: {r.status_code}")
            return r.json()

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

# if "cookie" not in st.session_state:
#     st.session_state.cookie = namedtuple("Cookie", ["set", "delete"])(set_cookie, delete_cookie)


if "user" not in st.session_state:
    default_user = {
        "role": "dev",  # TODO: change
        "mobile": False,
    }
    # TODO: probably add try except here
    st.session_state.user = default_user | st.session_state.backend.get("user")

if "user_settings" not in st.session_state:
    st.session_state.user_settings = {"show_courses": True}


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
    # if st.session_state
    # st.write(st.session_state.backend.get("user"))
    try:
        user = st.session_state.backend.get("user")
        st.session_state.user = st.session_state.user | user

    except requests.exceptions.HTTPError:
        st.error("HTTP error")

        # st.json(user)
        # user["courses"] = [{"id": c["id"], "name": c["name"], "role": c["role"]} for c in user["courses"]]
        # user["courses"] = [{**c.items()} for c in user["courses"]]
        # st.write(user["courses"][0])
        st.header("Log In")
        if st.button("login"):
            st.session_state.user["role"] = "dev"
            st.rerun()
        else:
            st.stop()


def logout():
    del st.session_state.user
    # st.session_state.cookies.delete("somethiing")
    st.rerun()


account_pages = [
    st.Page(logout, title="Log Out", icon=":material/logout:"),
    st.Page("./page/settings.py", title="Settings", icon=":material/settings:"),
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
