import streamlit as st

st.header("AI Tutor")

hello_world = st.session_state.backend.get()
st.write(hello_world)

users = st.session_state.backend.get("test_user")
st.write(users)

chat = st.session_state.backend.post("v1/chat", [{"role": "user", "content": "tell me a joke", "name": "test"}])
st.write(chat)
