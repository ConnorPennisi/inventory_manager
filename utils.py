import streamlit as st


def init_session_state():
    defaults = {
        "logged_in": False,
        "user": None,
        "role": None,
        "page": "login",
        "selected_item_id": None,
        "flash_message": "",
        "flash_type": "info"
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def login_session(user):
    st.session_state.logged_in = True
    st.session_state.user = user
    st.session_state.role = user["role"]
    st.session_state.page = "dashboard"
    st.session_state.flash_message = f"Welcome, {user['name']}!"
    st.session_state.flash_type = "success"


def logout_session():
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None
    st.session_state.page = "login"
    st.session_state.selected_item_id = None
    st.session_state.flash_message = "You have been logged out."
    st.session_state.flash_type = "info"


def set_flash(message, message_type="info"):
    st.session_state.flash_message = message
    st.session_state.flash_type = message_type


def show_flash():
    if st.session_state.flash_message:
        if st.session_state.flash_type == "success":
            st.success(st.session_state.flash_message)
        elif st.session_state.flash_type == "error":
            st.error(st.session_state.flash_message)
        else:
            st.info(st.session_state.flash_message)

        st.session_state.flash_message = ""
        st.session_state.flash_type = "info"
