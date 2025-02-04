import streamlit as st

st.title(":material/person_play: Tips and Tricks")

st.write("---")

with open("./page/tips.md", "r") as f:
    content = f.read()


st.write(content, unsafe_allow_html=True)
