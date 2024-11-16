
import streamlit as st


def runner():
    completion = ""
    for chunk in st.session_state.backend.post_stream("v1/chat_stream", st.session_state.messages):
        # for each 'chunk that is received from the backend
    
        yield chunk["content"]
        # yield the chunk
        completion += chunk["content"]
        # Now add the chunk's "content" to the completed string

    st.session_state.messages.append({"role": "assistant", "content": completion})
# After all the chuncks have been processed, add a new 'message' with all of the content to it


def render_messages():
    for message in st.session_state.messages:
        # st.session_state.messages contains a list of messages, we are iterating over them,
        if not message["content"]:
            continue
        # if there isn't any content in the message then skip to the next message

        elif message["role"] == "tool":
            continue
        # Skip the message if the role is a 'tool'

        else:
            st.chat_message(name=message["role"]).markdown(message["content"])
            # for all others create a chat message that contains the role and content
            # this is called everytime to re-render all of the messages

if "messages" not in st.session_state:
    st.session_state.messages = []
    # create the st.session_state.messages variable to hold onto all the messages of assistant and user

if st.sidebar.button("New Chat", use_container_width=True):
    # if the user opens up a new chat, clear all of the messages out of our session_state variable
    st.session_state.messages = []

st.title("AI Tutor :sparkles:")
st.caption("* Keep in mind responses may be inaccurate.")
st.write("---")

render_messages()
# this is called everytime a message is sent to display all of the messages again

if user_input := st.chat_input("Send a message", key="current_user_message"):
    # user ???
    st.chat_message("user").markdown(user_input)
    # display the chat_message in markdown form
    st.session_state.messages.append(
        {"role": "user", "content": user_input, "name": st.session_state.user["user"]},
    )
    # add this new input as a new message in the session state

    with st.chat_message("assistant"):
        # have gpt start to respond
        st.write_stream(runner())
        # and display each new content chunk as it is displayed


if st.session_state.messages:
    # if there are messages
    st.feedback(options="stars")  # TODO: Hook up
    # allow the user to rate the messages
