import streamlit as st


def app_header():
    st.set_page_config(
        page_title="Small Business Inventory Manager",
        page_icon="📦",
        layout="wide"
    )
    st.title("Small Business Inventory Manager")
    st.caption("Internal operations portal for Shop Owners and Employees")


def auth_sidebar():
    with st.sidebar:
        st.subheader("Welcome")
        st.write("Please log in or register to continue.")
        st.divider()
        st.write("**Roles:**")
        st.write("- Owner: manage inventory")
        st.write("- Employee: view catalog, log sales, flag low stock")


def user_sidebar(user, role):
    with st.sidebar:
        st.subheader("Account")
        st.write(f"**Name:** {user['name']}")
        st.write(f"**Username:** {user['username']}")
        st.write(f"**Role:** {role.title()}")

        st.divider()
        st.subheader("Role Access")

        if role == "owner":
            st.write("- Add products")
            st.write("- Update products")
            st.write("- Restock inventory")
            st.write("- Delete discontinued items")
            st.write("- Review employee flags")
        elif role == "employee":
            st.write("- View current catalog")
            st.write("- Log daily sales")
            st.write("- Flag low-stock items")
            st.write("- Use the Phase 1 assistant")
