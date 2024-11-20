import streamlit as st

st.title("User Settings")
st.caption("* Customize your chat experience")
st.write("---")

col1, col2 = st.columns(2)

# with col1:
#     st.session_state.user_settings["show_courses"] = st.toggle("Show Course Bubbles")

for course in st.session_state.user["courses"]:
    st.session_state.user["settings"].get("shown_courses")[str(course["id"])] = st.checkbox(
        " ".join(course["name"].split("|")[0].split("-")[0:2]),
        value=st.session_state.user["settings"].get("shown_courses").get(str(course["id"])),
    )

st.session_state.backend.post("user_settings", st.session_state.user["settings"])
