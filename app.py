import streamlit as st

from auth import register_user, login_user
from data_access import (
    init_data_files,
    get_inventory,
    get_flags,
    add_inventory_item,
    update_inventory_item,
    delete_inventory_item,
    log_sale,
    add_flag
)
from ui import app_header, auth_sidebar, user_sidebar
from utils import init_session_state, login_session, logout_session, set_flash, show_flash


init_data_files()
app_header()
init_session_state()


def render_inventory_table(items):
    if not items:
        st.info("No inventory items found.")
        return
    st.dataframe(items, use_container_width=True)


def render_phase1_chatbot():
    st.subheader("Inventory Assistant")
    st.caption("Phase 1 simulated AI with hardcoded responses")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    question = st.selectbox(
        "Ask a question",
        [
            "What items are low on stock?",
            "What is the total number of products?",
            "Which items have sold the most?",
            "How many items are out of stock?",
            "Show me all categories."
        ]
    )

    if st.button("Ask Assistant", use_container_width=True):
        inventory = get_inventory()

        if question == "What items are low on stock?":
            low_items = [
                item["name"]
                for item in inventory
                if item["stock"] <= item["low_stock_threshold"]
            ]
            answer = ", ".join(low_items) if low_items else "No items are currently low on stock."

        elif question == "What is the total number of products?":
            answer = f"There are {len(inventory)} products in the system."

        elif question == "Which items have sold the most?":
            top_items = sorted(inventory, key=lambda x: x["sold"], reverse=True)[:3]
            answer = ", ".join(
                [f"{item['name']} ({item['sold']})" for item in top_items]
            ) if top_items else "No sales data yet."

        elif question == "How many items are out of stock?":
            out_items = [item["name"] for item in inventory if item["stock"] == 0]
            answer = (
                f"{len(out_items)} item(s) are out of stock: {', '.join(out_items)}"
                if out_items else "No items are out of stock."
            )

        else:
            categories = sorted(set(item["category"] for item in inventory))
            answer = ", ".join(categories) if categories else "No categories found."

        st.session_state.chat_history.append({"role": "user", "content": question})
        st.session_state.chat_history.append({"role": "assistant", "content": answer})

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])


def render_login_register():
    auth_sidebar()
    show_flash()

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        with st.form("login_form"):
            st.subheader("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Log In", use_container_width=True)

            if submitted:
                success, user = login_user(username, password)
                if success:
                    login_session(user)
                    st.rerun()
                else:
                    set_flash("Invalid username or password.", "error")
                    st.rerun()

    with tab2:
        with st.form("register_form"):
            st.subheader("Register")
            name = st.text_input("Full Name")
            username = st.text_input("Create Username")
            password = st.text_input("Create Password", type="password")
            role = st.selectbox("Role", ["owner", "employee"])
            submitted = st.form_submit_button("Register", use_container_width=True)

            if submitted:
                ok, message = register_user(name, username, password, role)
                set_flash(message, "success" if ok else "error")
                st.rerun()


def render_owner_dashboard():
    user_sidebar(st.session_state.user, st.session_state.role)
    show_flash()

    st.header("Owner Dashboard")

    items = get_inventory()
    flags = get_flags()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Products", len(items))
    col2.metric("Low Stock Items", sum(1 for i in items if i["stock"] <= i["low_stock_threshold"]))
    col3.metric("Flags Submitted", len(flags))

    st.divider()

    tab1, tab2, tab3, tab4 = st.tabs(["Inventory", "Add Product", "Update/Delete", "Flags"])

    with tab1:
        st.subheader("Current Inventory")
        render_inventory_table(items)

    with tab2:
        with st.form("add_product_form"):
            st.subheader("Add Product")
            name = st.text_input("Product Name")
            category = st.text_input("Category")
            price = st.number_input("Price", min_value=0.0, step=0.5)
            stock = st.number_input("Starting Stock", min_value=0, step=1)
            low_stock_threshold = st.number_input("Low Stock Threshold", min_value=1, step=1, value=5)
            submitted = st.form_submit_button("Add Product", use_container_width=True)

            if submitted:
                add_inventory_item(
                    name=name,
                    category=category,
                    price=price,
                    stock=stock,
                    low_stock_threshold=low_stock_threshold,
                    created_by=st.session_state.user["username"]
                )
                set_flash("Product added successfully.", "success")
                st.rerun()

    with tab3:
        st.subheader("Update or Delete Product")

        if items:
            item_options = {f"{item['id']} - {item['name']}": item for item in items}
            selected_label = st.selectbox("Select Product", list(item_options.keys()))
            selected_item = item_options[selected_label]

            with st.form("update_product_form"):
                name = st.text_input("Product Name", value=selected_item["name"])
                category = st.text_input("Category", value=selected_item["category"])
                price = st.number_input("Price", min_value=0.0, step=0.5, value=float(selected_item["price"]))
                stock = st.number_input("Stock", min_value=0, step=1, value=int(selected_item["stock"]))
                low_stock_threshold = st.number_input(
                    "Low Stock Threshold",
                    min_value=1,
                    step=1,
                    value=int(selected_item["low_stock_threshold"])
                )

                col_a, col_b = st.columns(2)
                update_clicked = col_a.form_submit_button("Update Product", use_container_width=True)
                delete_clicked = col_b.form_submit_button("Delete Product", use_container_width=True)

                if update_clicked:
                    update_inventory_item(
                        selected_item["id"],
                        name,
                        category,
                        price,
                        stock,
                        low_stock_threshold
                    )
                    set_flash("Product updated successfully.", "success")
                    st.rerun()

                if delete_clicked:
                    delete_inventory_item(selected_item["id"])
                    set_flash("Product deleted successfully.", "success")
                    st.rerun()
        else:
            st.info("No products available to update or delete.")

    with tab4:
        st.subheader("Employee Flags")
        if flags:
            st.dataframe(flags, use_container_width=True)
        else:
            st.info("No flags submitted yet.")


def render_employee_dashboard():
    user_sidebar(st.session_state.user, st.session_state.role)
    show_flash()

    st.header("Employee Dashboard")

    items = get_inventory()

    col1, col2 = st.columns(2)
    col1.metric("Items in Catalog", len(items))
    col2.metric("Dangerously Low", sum(1 for i in items if i["stock"] <= i["low_stock_threshold"]))

    st.divider()

    tab1, tab2, tab3, tab4 = st.tabs(["Catalog", "Log Sale", "Low Stock", "Assistant"])

    with tab1:
        st.subheader("Current Catalog")
        render_inventory_table(items)

    with tab2:
        st.subheader("Log Daily Sale")
        if items:
            item_options = {
                f"{item['id']} - {item['name']} (stock: {item['stock']})": item
                for item in items
            }
            selected_label = st.selectbox("Choose Item", list(item_options.keys()))
            selected_item = item_options[selected_label]
            quantity = st.number_input("Quantity Sold", min_value=1, step=1)

            if st.button("Submit Sale", use_container_width=True):
                success, message = log_sale(
                    selected_item["id"],
                    int(quantity),
                    st.session_state.user["username"]
                )
                set_flash(message, "success" if success else "error")
                st.rerun()
        else:
            st.info("No inventory available.")

    with tab3:
        st.subheader("Flag Low Stock Item")
        low_items = [item for item in items if item["stock"] <= item["low_stock_threshold"]]

        if low_items:
            item_options = {f"{item['id']} - {item['name']}": item for item in low_items}
            selected_label = st.selectbox("Low Stock Item", list(item_options.keys()), key="flag_item")
            selected_item = item_options[selected_label]
            reason = st.text_area("Reason / Note", placeholder="Explain why this item needs attention...")

            if st.button("Submit Flag", use_container_width=True):
                add_flag(
                    item_id=selected_item["id"],
                    flagged_by=st.session_state.user["username"],
                    reason=reason if reason.strip() else "Low stock alert"
                )
                set_flash("Low stock flag submitted.", "success")
                st.rerun()
        else:
            st.success("No low-stock items need attention right now.")

    with tab4:
        render_phase1_chatbot()


def render_authenticated_app():
    top_col1, top_col2 = st.columns([8, 2])

    with top_col2:
        if st.button("Log Out", use_container_width=True):
            logout_session()
            st.rerun()

    if st.session_state.role == "owner":
        render_owner_dashboard()
    elif st.session_state.role == "employee":
        render_employee_dashboard()
    else:
        st.error("Unknown role. Please log in again.")
        logout_session()
        st.rerun()


if not st.session_state.logged_in:
    render_login_register()
else:
    render_authenticated_app()
