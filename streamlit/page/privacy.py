import streamlit as st

with open("./page/privacy_policy.md", "r") as f:
    content = f.read()

st.write(content)
