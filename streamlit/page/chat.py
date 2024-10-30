import streamlit as st


def stream_helper(user_input: str):
    for chunk in st.session_state.backend.post_stream(
        "v1/chat_stream", [{"role": "user", "content": user_input, "name": "test"}]
    ):
        yield chunk["content"]


def render_messages():
    for message in st.session_state.gpt["messages"]:
        if not message["content"]:
            continue

        elif message["role"] == "tool":
            continue

        else:
            st.chat_message(name=message["role"]).markdown(message["content"])


st.title("AI Tutor :sparkles:")
st.caption("Keep in mind responses may be inaccurate.")
st.write("---")

if user_input := st.chat_input(
    # random.choice(PLACEHOLDERS), key="current_user_message"  # , on_submit=respond
    "Send a message",
    key="current_user_message",  # , on_submit=respond
):
    # st.chat_message("user").markdown(st.session_state.current_user_message)
    st.chat_message("user").markdown(user_input)

    with st.chat_message("assistant"):
        # st.write_stream(ai(st.session_state.current_user_message))
        st.write_stream(stream_helper(user_input))
