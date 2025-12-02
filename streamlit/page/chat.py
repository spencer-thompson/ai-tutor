import logging
import re
from typing import Literal

import streamlit as st

PATTERNS = [  # patterns for converting latex to markdown math
    {"rgx": re.compile(r"\\\s*?\(|\\\s*?\)", re.DOTALL), "new": r"$"},
    {"rgx": re.compile(r"\\\s*?\[|\\\s*?\]", re.DOTALL), "new": r"$$"},
]


def runner(
    courses,
    model: Literal["gpt-4o", "gpt-4o-mini", "o1", "gpt-4.1", "gpt-4.1-mini", "gpt-4.1-nano"] = "gpt-4.1",
    role: Literal["Auto", "Quick", "Tutor", "General"] = "Auto",
):
    """
    Helper function for the tutor, yields token as they are received
    """
    data = {
        "messages": st.session_state.messages,
        "courses": [c["id"] for c in courses],
        "model": model,
        "role": role,
    }
    completion = ""
    previous_tokens = []
    sliding_window_limit = 3  # set sliding window size
    for chunk in st.session_state.backend.post_stream("v1/smart_chat_stream", data):
        if token := chunk.get("content"):
            previous_tokens.append(token)
            window_size = len(previous_tokens) if len(previous_tokens) <= sliding_window_limit else sliding_window_limit
            sliding_window = "".join(previous_tokens[-window_size:])

            for pat in PATTERNS:
                if match := pat["rgx"].search(sliding_window):
                    # logging.warning(match.string)
                    previous_tokens = [sliding_window[: match.start()], pat["new"], sliding_window[match.end() :]]
                    # logging.warning(previous_tokens)

            if len(previous_tokens) >= sliding_window_limit:
                popped_token = previous_tokens.pop(0)  # lol an actual stack in the wild
                completion += popped_token
                yield popped_token

        elif token := chunk.get("flagged"):
            yield "Hey thats not cool bro"
            completion = "Hey thats not cool bro"

    if previous_tokens:  # flush out rest of sliding window
        for token in previous_tokens:
            completion += token
            yield token

    st.session_state.messages.append({"role": "assistant", "content": completion})


if "chat_control" not in st.session_state:
    st.session_state.chat_control = {}

if "selected_control" not in st.session_state:
    st.session_state.selected_control = False


if "messages" not in st.session_state:
    if history := st.session_state.user.get("chat_history"):
        st.session_state.messages = history

    else:
        st.session_state.messages = []


def clear_messages():
    st.session_state.messages = []
    st.rerun()


def respond_again():
    st.session_state.selected_control = True
    st.session_state.messages.pop()
    st.session_state.messages.pop()
    st.rerun()


def save_chat():
    st.session_state.selected_control = True
    st.session_state.backend.post("save_chat", st.session_state.messages)
    st.rerun()


def think():
    st.session_state.messages.pop()
    render_messages()
    with st.chat_message("assistant"):
        st.write_stream(runner(selected_courses, model="o1"))


def chat_control_buttons():
    if len(st.session_state.messages) > 0 and st.session_state.has_sent_message:
        # if not st.session_state.chat_control:
        if not st.session_state.selected_control:
            # st.write(st.session_state.chat_control)
            st.segmented_control(
                "Control",
                [
                    {"display": "New Chat", "func": clear_messages},
                    {"display": "Rewind", "func": respond_again},
                    {"display": "Save Chat", "func": save_chat},
                    # {"display": "Think about it", "func": think},
                ],
                key="chat_control",
                default=None,
                format_func=lambda o: o["display"],
                selection_mode="single",
                label_visibility="collapsed",
                width="stretch",
            )

            if st.session_state.chat_control:
                if func := st.session_state.chat_control.get("func"):
                    func()
        else:
            st.session_state.selected_control = False


st.title("AI Tutor :sparkles:")
st.caption("* Keep in mind responses may be inaccurate.")
st.write("---")


selected_courses = st.pills(
    "Courses",
    options=[
        c
        for c in st.session_state.user["courses"]
        if st.session_state.user["settings"].get("shown_courses").get(str(c.get("id")))
    ],
    default=[
        c
        for c in st.session_state.user["courses"]
        if st.session_state.user["settings"].get("shown_courses").get(str(c.get("id")))
    ],
    selection_mode="multi",
    # on_change=lambda: st.session_state.messages = [],
    format_func=lambda c: " ".join(c.get("course_code").split(" ")[0:2])
    if c.get("course_code")
    else " ".join(c["name"].split("|")[0].split("-")[0:2]),
    label_visibility="collapsed",
    width="stretch",
)

st.session_state.displayed_messages = st.empty()


# @st.fragment
def render_messages():
    with st.session_state.displayed_messages.container():
        for message in st.session_state.messages:
            if not message["content"]:
                continue

            elif message["role"] == "tool":
                continue

            elif message.get("name") == "system":
                continue

            else:
                st.chat_message(name=message["role"]).markdown(message["content"])


if (
    not st.session_state.has_sent_message
    and st.session_state.user["settings"].get("first_message")
    and len(st.session_state.messages) == 0
):
    st.session_state.messages.append(
        {
            "role": "user",
            "content": f"""
            Greet {st.session_state.user["first_name"]}, the user, and give a brief introduction
            about what you can do and who you are. Use markdown formatting but do not wrap in backticks.
            Include that you are **created by students for students**.
            Lastly invite the user to see the `Settings` and `Tips and Tricks` page.
            """,
            "name": "instructions",
        },
    )
    with st.chat_message("assistant"):
        st.write_stream(
            runner(
                selected_courses,
                model="gpt-4.1-nano",
                role="Quick",
            )
        )

    st.session_state.messages.pop(0)
    st.session_state.has_sent_message = True
    st.session_state.messages.pop(0)


render_messages()

if user_input := st.chat_input(
    "What updates do I have?" if len(st.session_state.messages) == 0 else "Send a chat", key="current_user_message"
):
    st.session_state.has_sent_message = True
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append(
        {"role": "user", "content": user_input, "name": st.session_state.user["first_name"]},
    )

    st.session_state.track_event("simple_chat", page="chat", props={"length": len(st.session_state.messages)})

    with st.chat_message("assistant"):
        st.write_stream(runner(selected_courses))

    st.session_state.refresh_token()  # refresh token on chat to keep user logged in
    st.rerun()

chat_control_buttons()
