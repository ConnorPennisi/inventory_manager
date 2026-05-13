import streamlit as st


def setup_page():
    st.set_page_config(
        page_title="Store Inventory Portal - Phase 1",
        page_icon="📦",
        layout="wide"
    )


def render_header():
    st.title("Store Inventory Portal")
    st.caption("Phase 1 MVP: inventory tracking for a small retail shop.")


def render_test_accounts():
    st.info(
        """
        **Test Accounts**

        **Owner**
        - Username: `owner`
        - Password: `owner123`

        **Employee**
        - Username: `employee`
        - Password: `employee123`
        """
    )


def render_user_sidebar(user, role):
    with st.sidebar:
        st.subheader("Current User")
        st.write(f"**Name:** {user['name']}")
        st.write(f"**Role:** {role.title()}")


def owner_navigation():
    with st.sidebar:
        st.divider()
        return st.radio(
            "Owner Navigation",
            [
                "Dashboard",
                "View Inventory",
                "Add Product",
                "Update Product",
                "Delete Product",
                "Employee Flags",
                "Inventory Assistant"
            ]
        )


def employee_navigation():
    with st.sidebar:
        st.divider()
        return st.radio(
            "Employee Navigation",
            [
                "Dashboard",
                "Product Catalog",
                "Log Sale",
                "Submit Inventory Flag",
                "Inventory Assistant"
            ]
        )


def render_inventory_card(item):
    with st.container(border=True):
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.write(f"**{item['name']}**")
            st.caption(item["category"])

        with col2:
            st.write(f"Price: **${float(item['price']):.2f}**")

        with col3:
            st.write(f"Stock: **{item['stock']}**")
            st.write(f"Sold: **{item.get('sold', 0)}**")

        with col4:
            if int(item["stock"]) == 0:
                st.error("Out of Stock")
            elif int(item["stock"]) <= int(item["low_stock_threshold"]):
                st.warning("Low Stock")
            else:
                st.success("In Stock")


def render_flag_card(flag):
    with st.container(border=True):
        st.write(f"**Item:** {flag['item_name']}")
        st.write(f"**Flagged By:** {flag['flagged_by']}")
        st.write(f"**Reason:** {flag['reason']}")
        st.caption(f"Submitted: {flag['created_at']}")