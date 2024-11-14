import streamlit as st


def runner(courses):
    data = {"messages": st.session_state.messages, "courses": [c["id"] for c in courses]}
    completion = ""
    for chunk in st.session_state.backend.post_stream("v1/smart_chat_stream", data):
        yield chunk["content"]
        completion += chunk["content"]

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
    st.session_state.chat_control = None


def clear_messages():
    st.session_state.messages = []


def think():
    pass


def control():
    func = st.session_state.chat_control.get("func")
    if func:
        func()


if "messages" not in st.session_state:
    st.session_state.messages = []


# if st.sidebar.button("New Chat", use_container_width=True):
#     clear_messages()


st.title("AI Tutor :sparkles:")
st.caption("* Keep in mind responses may be inaccurate.")
st.write("---")

render_messages()


selected_courses = st.pills(
    "Courses",
    options=[c for c in st.session_state.user["courses"] if st.session_state.user_settings["shown_courses"][c["id"]]],
    default=[c for c in st.session_state.user["courses"] if st.session_state.user_settings["shown_courses"][c["id"]]],
    selection_mode="multi",
    on_change=clear_messages,
    format_func=lambda c: " ".join(c["name"].split("|")[0].split("-")[0:2]),
    label_visibility="collapsed",
)

if user_input := st.chat_input("Send a message", key="current_user_message"):
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append(
        {"role": "user", "content": user_input, "name": st.session_state.user["first_name"]},
    )

    with st.chat_message("assistant"):
        st.write_stream(runner(selected_courses))

    st.rerun()


if st.session_state.messages:
    st.segmented_control(
        "Control",
        [{"display": "New Chat", "func": clear_messages}, {"display": "Think about it", "func": think}],
        key="chat_control",
        on_change=control,
        format_func=lambda o: o["display"],
        label_visibility="collapsed",
    )
    # if st.feedback() is False:
    #     st.write("test")


# if st.session_state.messages:
#     st.feedback(options="stars")  # TODO: Hook up
