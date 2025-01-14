import streamlit as st

with open("./page/about.md", "r") as f:
    content = f.read()

st.write(content)
