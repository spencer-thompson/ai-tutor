import streamlit as st

st.header("Session State")
st.write("---")
st.write(st.session_state)


st.subheader("Cookies")
st.write("---")
st.write(st.context.cookies)
st.subheader("Headers")
st.write("---")
st.write(st.context.headers)
st.subheader("Query Params")
st.write("---")
st.write(st.query_params)
