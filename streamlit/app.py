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


if "patterns" not in st.session_state:
    st.session_state.patterns = namedtuple("Pattern", ["mobile"])(
        re.compile(r"[mM]obile|iPhone|iPad|iPod|Android|webOS")
    )  # check mobile


if "user" not in st.session_state:
    default_user = {
        "role": "dev",  # TODO: change
        "mobile": True if st.session_state.patterns.mobile.search(st.context.headers["User-Agent"]) else False,
        # "logged_in": False,
        "authenticated": False,
    }
    try:
        st.session_state.user = default_user | st.session_state.backend.get("user")
        st.session_state.user["authenticated"] = True
        # st.session_state.user["logged_in"] = True
    except requests.exceptions.HTTPError:
        st.session_state.user = default_user  # figure out how to tell a user to login


if "user_settings" not in st.session_state and st.session_state.user.get("authenticated"):
    st.session_state.user_settings = {
        "show_courses": True,
        "shown_courses": {c["id"]: True for c in st.session_state.user["courses"]},
    }

if "user_count" not in st.session_state:
    st.session_state.user_count = st.session_state.backend.get("user_count").get("total_users")


if "layout" not in st.session_state:
    if st.session_state.patterns.mobile.search(st.context.headers["User-Agent"]) or st.query_params.get("extension"):
        st.session_state.layout = "wide"
    # elif st.query_params.get("extension"):
    #     st.session_state.layout = "wide"
    else:
        st.session_state.layout = "centered"

if "accepted_cookie" not in st.session_state:
    st.session_state.accepted_cookie = False


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
    if not st.session_state.user["authenticated"]:
        st.warning(":material/engineering: The AI Tutor is currently in development. Full release coming soon")
        st.title("Log In")
        st.caption(
            "* If you have previously logged in and are seeing this, visit the canvas page and refresh this page"
        )
        st.write("---")
        if not st.session_state.accepted_cookie:
            st.write("""
            First things first, we need to talk about cookies :cookie: 

            We all know the annoying popups usually saying something like:

            ### ```This website utilizes technologies such as cookies to enable essential site functionality...```
            
            *blah blah blah*


            **Anyway**, Instead of making everyone create a new account and remember a password,
            I decided I would prefer to store logging in and loggin out as a cookie.

            This has a lot of benefits, and streamlines the process of logging in and out *a lot*.

            ---

            **TLDR:** I need you to accept a cookies to let you use the AI Tutor
            """)
            if not st.button("Accept Cookie", use_container_width=True, type="primary"):
                st.stop()
            else:
                st.session_state.accepted_cookie = True
                st.rerun()
                # st.toast("Thank you!", icon=":material/sentiment_very_satisfied:")

        st.toast("Thank you!", icon=":material/sentiment_very_satisfied:")
        st.balloons()

        st.write("""
        Next, in order to log in, you need to install our **Browser Extension**.

        * [Google Chrome](www.google.com)
        
        * [Microsoft Edge](www.google.com)

        * [Firefox](www.google.com)

        ---

        After downloading the browser extension, if for some reason you are not automatically redirected,
        visit your universities canvas homepage.

        * [UVU](https://uvu.instructure.com/)
        
        ---

        **Lastly**, refresh the page and you should be good to go!
        """)
        st.caption("* Sometimes it can take a second while for canvas to load :material/sentiment_dissatisfied:")

        st.stop()


def logout():  # currently unused
    del st.session_state.user
    # st.session_state.cookies.delete("somethiing")
    st.rerun()


account_pages = [
    # st.Page(logout, title="Log Out", icon=":material/logout:"),
    st.Page("./page/settings.py", title="Settings", icon=":material/settings:"),
    st.Page("./page/mobile.py", title="Mobile", icon=":material/smartphone:"),
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

if st.session_state.user.get("authenticated"):
    if st.session_state.user["role"] in ["normal", "admin"]:
        pages["AI"] = user_pages
        pages["INFO"] = info_pages

    if st.session_state.user["role"] in ["dev"]:
        pages["AI"] = user_pages
        pages["INFO"] = info_pages
        pages["DEV"] = dev_pages

else:
    pages = {}


if len(pages) > 0:
    pg = st.navigation({"PROFILE": account_pages} | pages, expanded=True)

else:
    pg = st.navigation([st.Page(login)], expanded=True)

pg.run()

with st.sidebar:
    # st.metric("Users", f"{st.session_state.user_count} Users", "1", label_visibility="collapsed")
    if feedback := st.feedback("stars"):
        # st.write(feedback)
        st.write("implement")

# if feedback := st.sidebar.feedback("stars"):
#     st.sidebar.text_area("stuff", label_visibility="collapsed")

# st.sidebar.caption(f"* AI Tutor Version: :green-background[{VERSION}]")
