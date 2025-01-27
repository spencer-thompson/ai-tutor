"""
Entry point for streamlit
"""

import json
import logging
import os
import re
import uuid
from collections import namedtuple

import requests

import streamlit as st
from streamlit.components.v1 import html

VERSION = 1.000
UNIVERSITIES = ["UVU"]
UPDATES = [  # notifications to display the user upon login
    "- :material/qr_code: Mobile Login Now Available!",
    "- :material/healing: Locked assigments no longer shown.",
]

# st.session_state.updates = UPDATES

if "patterns" not in st.session_state:
    st.session_state.patterns = namedtuple("Pattern", ["mobile"])(
        re.compile(r"[mM]obile|iPhone|iPad|iPod|Android|webOS")
    )  # check mobile


if "layout" not in st.session_state:
    if st.session_state.patterns.mobile.search(st.context.headers["User-Agent"]) or st.query_params.get("extension"):
        st.session_state.layout = "wide"
    else:
        st.session_state.layout = "centered"

st.set_page_config(
    page_title="AI Tutor",
    page_icon=":mortar_board:",
    layout=st.session_state.layout,
    # initial_sidebar_state="collapsed" if st.session_state.user["mobile"] else "auto",
    initial_sidebar_state="collapsed",
    menu_items={
        "Get Help": None,  # url
        "Report a bug": None,  # url
        "About": f"""# Version: {VERSION}""",
    },
)


def track_event(name: str, page: str, props: dict = {}):
    analytics_url = os.getenv("BASE_URL")
    analytics_headers = {
        "User-Agent": st.context.headers.get("User-Agent"),
        "X-Forwarded-For": st.context.headers.get("X-Forwarded-For"),
        "Content-Type": "application/json",
    }

    domain = os.getenv("DOMAIN")
    full_url = f"https://{domain}/{page}"

    analytics_data = {"domain": domain, "name": name, "url": full_url, "props": props}

    r = requests.post(url=analytics_url + "/api/event", headers=analytics_headers, json=analytics_data)
    if r.status_code != 202:
        #     return r.json()
        # else:
        logging.warning("Analytics Error")
        # return r.json()


def set_cookie(key: str, val: str):
    """
    Sets a cookie for 1 day
    """
    html(
        f"""
    <script>
        const date = new Date();
        date.setTime(date.getTime() + (1 * 24 * 60 * 60 * 1000)); // Set expiration to 1 day from now
        const expires = "expires=" + date.toUTCString();

        document.cookie = "{key}={val}; " + expires + "; path=/; Secure; SameSite=None";
    </script>
    """,
        height=0,
    )


if "set_cookie" not in st.session_state:
    st.session_state.set_cookie = set_cookie


if "token" not in st.session_state:
    if token := st.query_params.get("token"):
        set_cookie("token", token)
        st.session_state.token = token
        del st.query_params["token"]
        st.rerun()

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


def refresh_token():
    new_token = st.session_state.backend.get("token")
    st.session_state.token = new_token.get("token")
    st.session_state.set_cookie("token", st.session_state.token)


if "refresh_token" not in st.session_state:
    st.session_state.refresh_token = refresh_token


if "track_event" not in st.session_state:
    st.session_state.track_event = track_event


if "user" not in st.session_state:
    default_user = {
        "role": "dev",
        "mobile": True if st.session_state.patterns.mobile.search(st.context.headers["User-Agent"]) else False,
        # "logged_in": False,
        "authenticated": False,
    }
    try:
        st.session_state.user = default_user | st.session_state.backend.get("user")
        st.session_state.user["authenticated"] = True
        if "session_id" not in st.session_state:
            st.session_state.session_id = str(uuid.uuid4())

        # st.session_state.analytics.event(
        track_event(
            "session",
            page="",
            props={
                "id": st.session_state.session_id,
                "role": st.session_state.user.get("role"),
                "mobile": st.session_state.user.get("mobile"),
                "canvas_id": st.session_state.user.get("canvas_id"),
                "institution": st.session_state.user.get("institution"),
                "first_name": st.session_state.user.get("first_name"),
                "last_name": st.session_state.user.get("last_name"),
            },
        )
        if not st.session_state.user.get("settings"):
            st.session_state.user["settings"] = {  # Need to move this to the backend
                "bio": "",
                "notify_updates": True,
                "first_message": True,
                "show_courses": True,
                "shown_courses": {str(c["id"]): True for c in st.session_state.user["courses"]},
            }

            st.session_state.backend.post("user_settings", st.session_state.user["settings"])

        st.session_state.user_count = st.session_state.backend.get("user_count").get("total_users")
        # st.session_state.user["logged_in"] = True
    except requests.exceptions.HTTPError as e:
        logging.warning(e)
        st.session_state.user = default_user  # figure out how to tell a user to login


# if "user_count" not in st.session_state:
#     st.session_state.user_count = st.session_state.backend.get("user_count").get("total_users")

if "has_sent_message" not in st.session_state:
    st.session_state.has_sent_message = False


if "accepted_cookie" not in st.session_state:
    st.session_state.accepted_cookie = False


st.logo("./512.png", size="large", icon_image="./512.png")


def login():
    if not st.session_state.user["authenticated"]:
        st.warning(":material/engineering: The AI Tutor is currently in development. Full release coming soon")
        st.title("Log In")
        st.caption("* If you have previously logged in and are seeing this, visit canvas and refresh this page")
        st.write("---")
        if not st.session_state.accepted_cookie:
            st.write("""
            First things first, we need to talk about cookies :cookie: 

            Instead of making everyone create a new account and remember a password,
            I decided I would prefer to store logging in and loggin out as a cookie.""")

            st.caption("* This has a lot of benefits, and streamlines the process of logging in and out *a lot*.")

            st.write("""
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

        st.write("""
        Next, in order to log in, you need to install our **Browser Extension**.""")
        st.caption(
            "* The browser extension allows us to communicate with canvas.\n* Sadly, we can't provide this experience without it."
        )

        st.link_button(
            "**Google Chrome**",
            "https://chromewebstore.google.com/detail/ai-tutor/eoidpdhnopocccgnlclpmadnccolaman",
            type="primary",
            use_container_width=True,
        )
        st.link_button(
            "**Microsoft Edge**",
            "https://chromewebstore.google.com/detail/ai-tutor/eoidpdhnopocccgnlclpmadnccolaman",
            type="primary",
            use_container_width=True,
        )
        st.link_button(
            "**Firefox** - *Coming Soon*",
            "https://chromewebstore.google.com/detail/ai-tutor/eoidpdhnopocccgnlclpmadnccolaman",
            type="primary",
            disabled=True,
            use_container_width=True,
        )
        st.link_button(
            "**Safari** - *Coming Soon*",
            "https://chromewebstore.google.com/detail/ai-tutor/eoidpdhnopocccgnlclpmadnccolaman",
            type="primary",
            disabled=True,
            use_container_width=True,
        )
        st.write("""
        ##### After downloading the browser extension, if for some reason you are not automatically redirected, visit your university canvas homepage.
        """)

        cols = st.columns(len(UNIVERSITIES))
        for c, u in zip(cols, UNIVERSITIES):
            c.link_button(u, f"https://{u.lower()}.instructure.com", type="secondary", use_container_width=True)
        # if uni := st.pills("Universities", UNIVERSITIES, default=UNIVERSITIES[0]):
        #     st.switch_page("https://uvu.instructure.com")

        st.caption(
            "* I don't see [my university](mailto:ahmed.alsharif@uvu.edu?subject=AI%20Tutor%20University%20Request)..."
        )

        st.write("""
        ---

        **Lastly**, refresh the page and you should be good to go!
        """)
        st.caption("* Sometimes it can take a second while for canvas to load :material/sentiment_dissatisfied:")

        st.stop()


def logout():  # currently unused
    del st.session_state.user
    st.rerun()


account_pages = [
    # st.Page(logout, title="Log Out", icon=":material/logout:"),
    st.Page("./page/settings.py", title="Settings", icon=":material/settings:"),
    st.Page("./page/mobile.py", title="Mobile", icon=":material/smartphone:"),
]
user_pages = [
    st.Page("./page/chat.py", title="Chat", icon=":material/chat:", default=True),
    st.Page("./page/tips.py", title="Tips and Tricks", icon=":material/lightbulb_2:"),
]
info_pages = (
    [
        st.Page("./page/about.py", title="About", icon=":material/info:"),
        st.Page(
            "./page/privacy.py",
            title="Privacy Policy",
            icon=":material/policy:",
            default=True if st.query_params.get("privacy_policy") else False,
        ),
    ]
    # if st.query_params.get("privacy_policy")
    # else [st.Page("./page/about.py", title="About", icon=":material/info:")]
)
dev_pages = [
    st.Page("./page/session_state.py", title="Session State", icon=":material/settings:"),
]

pages = {}
pages["INFO"] = info_pages

if st.session_state.user.get("authenticated"):
    if st.session_state.user["role"] in ["normal", "admin"]:
        pages["AI"] = user_pages
        # pages["INFO"] = info_pages

    if st.session_state.user["role"] in ["dev"]:
        pages["AI"] = user_pages
        # pages["INFO"] = info_pages
        pages["DEV"] = dev_pages

    pg = st.navigation({"PROFILE": account_pages} | pages, expanded=True)

    if not st.session_state.has_sent_message and st.session_state.user["settings"].get("notify_updates"):
        for u in UPDATES:
            st.toast(u, icon=":material/new_releases:")

else:
    pg = st.navigation(
        {
            "PROFILE": [
                st.Page(
                    login,
                    title="Log In",
                    icon=":material/login:",
                    default=False if st.query_params.get("privacy_policy") else True,
                )
            ]
        }
        | pages,
        expanded=True,
    )


pg.run()


with st.sidebar:
    # st.metric("Users", f"{st.session_state.user_count} Users", "1", label_visibility="collapsed")
    if feedback := st.feedback("stars"):
        # st.write(feedback)
        st.write("haha it doesn't do anything but you still clicked :smirk: :blush:")

# if feedback := st.sidebar.feedback("stars"):
#     st.sidebar.text_area("stuff", label_visibility="collapsed")

# st.sidebar.caption(f"* AI Tutor Version: :green-background[{VERSION}]")
