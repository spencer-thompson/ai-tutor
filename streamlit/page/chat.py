import streamlit as st


def runner():
    completion = ""
    for chunk in st.session_state.backend.post_stream("v1/chat_stream", st.session_state.messages):
        yield chunk["content"]
        completion += chunk["content"]

    st.session_state.messages.append({"role": "assistant", "content": completion})


def render_messages():
    for message in st.session_state.messages:
        if not message["content"]:
            continue

        elif message["role"] == "tool":
            continue

        else:
            st.chat_message(name=message["role"]).markdown(message["content"])


if "messages" not in st.session_state:
    st.session_state.messages = []

if st.sidebar.button("New Chat", use_container_width=True):
    st.session_state.messages = []

st.title("AI Tutor :sparkles:")
st.caption("* Keep in mind responses may be inaccurate.")
st.write("---")

render_messages()

if user_input := st.chat_input("Send a message", key="current_user_message"):
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append(
        {"role": "user", "content": user_input, "name": st.session_state.user["name"]},
    )

    with st.chat_message("assistant"):
        st.write_stream(runner())

if st.session_state.messages:
    st.feedback(options="stars")  # TODO: Hook up
