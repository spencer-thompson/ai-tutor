import streamlit as st

st.title("User Settings")
st.caption("* Customize your chat experience")
st.write("---")

for course in st.session_state.user["courses"]:
    st.toggle(course["name"])
