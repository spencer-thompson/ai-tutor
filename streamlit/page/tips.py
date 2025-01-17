import streamlit as st

with open("./page/tips.md", "r") as f:
    content = f.read()


st.write(content, unsafe_allow_html=True)
