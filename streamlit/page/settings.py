import streamlit as st

st.title("User Settings")
st.caption("* Customize your chat experience")
st.write("---")

col1, col2 = st.columns(2)

st.session_state.user["settings"]["bio"] = st.text_area(
    "bio",
    value=st.session_state.user["settings"].get("bio") if st.session_state.user["settings"].get("bio") else "",
    max_chars=280,
    help="Info about you for the tutor",
    placeholder="What do you want the tutor to know about you?",
    label_visibility="collapsed",
)


st.subheader("First Message")
st.caption("* Uncheck to stop the Tutor from sending the first message.")

# if first_message := st.session_state.user["settings"].get("first_message") is not None:
#     st.session_state.user["settings"]["first_message"] = st.checkbox("Tutor", value=first_message )
#
# else:
#     st.session_state.user["settings"]["first_message"] = st.checkbox("Tutor", value=True)
st.session_state.user["settings"]["first_message"] = st.checkbox(
    "Tutor",
    value=st.session_state.user["settings"].get("first_message")
    if st.session_state.user["settings"].get("first_message") is not None
    else True,
)

st.subheader("Shown Courses")
st.caption("* Show only selected courses in the chat interface.")

for course in st.session_state.user["courses"]:
    st.session_state.user["settings"].get("shown_courses")[str(course["id"])] = st.checkbox(
        " ".join(course["name"].split("|")[0].split("-")[0:2]),
        value=st.session_state.user["settings"].get("shown_courses").get(str(course["id"])),
    )

st.session_state.backend.post("user_settings", st.session_state.user["settings"])
