from typing import Literal

import streamlit as st


def runner(courses, model: Literal["gpt-4o", "o1"] = "gpt-4o"):
    data = {"messages": st.session_state.messages, "courses": [c["id"] for c in courses], "model": model}
    completion = ""
    for chunk in st.session_state.backend.post_stream("v1/smart_chat_stream", data):
        if c := chunk.get("content"):
            yield c
            completion += c

        elif c := chunk.get("flagged"):
            yield "Hey thats not cool bro"
            completion = "Hey thats not cool bro"

    st.session_state.messages.append({"role": "assistant", "content": completion})


def render_messages():
    for message in st.session_state.messages:
        if not message["content"]:
            continue

        elif message["role"] == "tool":
            continue

        elif message.get("name") == "system":
            continue

        else:
            st.chat_message(name=message["role"]).markdown(message["content"])


if "chat_control" not in st.session_state:
    st.session_state.chat_control = {}

if "chat_changed" not in st.session_state:
    st.session_state.chat_changed = False


def clear_messages():
    st.session_state.messages = []
    st.rerun()


def think():
    pass


if "messages" not in st.session_state:
    st.session_state.messages = []


# if st.sidebar.button("New Chat", use_container_width=True):
#     clear_messages()


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
    on_change=clear_messages,
    format_func=lambda c: " ".join(c["name"].split("|")[0].split("-")[0:2]),
    label_visibility="collapsed",
)

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
            """,
            "name": "instructions",
        },
    )
    with st.chat_message("assistant"):
        st.write_stream(runner(selected_courses))

    st.session_state.messages.pop(0)

    st.rerun()
    # render_messages()
    # clear_messages()


render_messages()

if user_input := st.chat_input("Send a message", key="current_user_message"):
    if not st.session_state.has_sent_message:
        st.session_state.messages.pop(0)
        st.session_state.has_sent_message = True

    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append(
        {"role": "user", "content": user_input, "name": st.session_state.user["first_name"]},
    )

    st.session_state.track_event("simple_chat", page="chat", props={"length": len(st.session_state.messages)})

    with st.chat_message("assistant"):
        st.write_stream(runner(selected_courses))

    st.rerun()


def respond_again():
    st.session_state.messages.pop()
    with st.chat_message("assistant"):
        st.write_stream(runner(selected_courses))


def chat_changed():
    st.session_state.chat_changed = True


# if len(st.session_state.messages) > 1 and not st.session_state.chat_control or st.session_state.chat_changed:
if len(st.session_state.messages) > 1:
    st.segmented_control(
        "Control",
        [
            {"display": "New Chat", "func": clear_messages},
            # {"display": "Again", "func": respond_again},
        ],  # , {"display": "Think about it", "func": think}
        key="chat_control",
        on_change=chat_changed,
        default=None,
        format_func=lambda o: o["display"],
        # selection_mode="",
        label_visibility="collapsed",
    )

    # st.toast(st.session_state.chat_control)

    # for f in st.session_state.chat_control:
    if func := st.session_state.chat_control.get("func"):
        func()
        st.session_state.chat_changed = False
        # st.session_state.chat_control = []
        # st.rerun()

    # if st.feedback() is False:
    #     st.write("test")


# if st.session_state.messages:
#     st.feedback(options="stars")  # TODO: Hook up
