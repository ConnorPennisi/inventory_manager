import streamlit as st


def init_session_state():
    defaults = {
        "logged_in": False,
        "current_user": None,
        "role": None,
        "flash_message": "",
        "flash_type": "info"
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def login_session(user):
    st.session_state.logged_in = True
    st.session_state.current_user = user
    st.session_state.role = user["role"]
    set_flash(f"Welcome, {user['name']}!", "success")


def logout_session():
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.session_state.role = None
    set_flash("You have been logged out.", "info")


def set_flash(message, message_type="info"):
    st.session_state.flash_message = message
    st.session_state.flash_type = message_type


def show_flash():
    if not st.session_state.flash_message:
        return

    if st.session_state.flash_type == "success":
        st.success(st.session_state.flash_message)
    elif st.session_state.flash_type == "error":
        st.error(st.session_state.flash_message)
    elif st.session_state.flash_type == "warning":
        st.warning(st.session_state.flash_message)
    else:
        st.info(st.session_state.flash_message)

    st.session_state.flash_message = ""
    st.session_state.flash_type = "info"