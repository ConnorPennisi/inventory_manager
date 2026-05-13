import streamlit as st
from datetime import datetime

from data_access import (
    ensure_data_files,
    load_inventory,
    save_inventory,
    load_flags,
    save_flags,
    get_next_id
)
from auth import login_user, register_user
from utils import (
    init_session_state,
    login_session,
    logout_session,
    set_flash,
    show_flash
)
from ui import (
    setup_page,
    render_header,
    render_test_accounts,
    render_user_sidebar,
    owner_navigation,
    employee_navigation,
    render_inventory_card,
    render_flag_card
)


def get_low_stock_items(inventory):
    return [
        item for item in inventory
        if int(item["stock"]) <= int(item["low_stock_threshold"])
    ]


def get_out_of_stock_items(inventory):
    return [
        item for item in inventory
        if int(item["stock"]) == 0
    ]


def find_item_by_id(inventory, item_id):
    for item in inventory:
        if int(item["id"]) == int(item_id):
            return item

    return None


def render_login_page():
    show_flash()

    left_col, right_col = st.columns([1, 1])

    with left_col:
        st.header("Welcome")
        st.write(
            "This app helps a small store manage inventory, log sales, "
            "track low-stock items, and flag inventory issues."
        )
        render_test_accounts()

    with right_col:
        tab1, tab2 = st.tabs(["Login", "Register"])

        with tab1:
            st.subheader("Login")
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")

            if st.button("Login", use_container_width=True):
                success, user, message = login_user(username, password)

                if success:
                    login_session(user)
                    st.rerun()
                else:
                    set_flash(message, "error")
                    st.rerun()

        with tab2:
            st.subheader("Register")
            name = st.text_input("Full Name", key="register_name")
            username = st.text_input("Create Username", key="register_username")
            password = st.text_input("Create Password", type="password", key="register_password")
            role = st.selectbox("Role", ["owner", "employee"], key="register_role")

            if st.button("Create Account", use_container_width=True):
                success, message = register_user(name, username, password, role)
                set_flash(message, "success" if success else "error")
                st.rerun()


def render_owner_dashboard():
    inventory = load_inventory()
    flags = load_flags()
    low_stock_items = get_low_stock_items(inventory)

    total_value = sum(
        float(item["price"]) * int(item["stock"])
        for item in inventory
    )

    st.header("Owner Dashboard")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Products", len(inventory))
    col2.metric("Inventory Value", f"${total_value:,.2f}")
    col3.metric("Low Stock Items", len(low_stock_items))
    col4.metric("Employee Flags", len(flags))

    st.divider()

    st.subheader("Items Needing Attention")

    if low_stock_items:
        for item in low_stock_items:
            render_inventory_card(item)
    else:
        st.success("No low-stock items.")


def render_owner_view_inventory():
    inventory = load_inventory()

    st.header("View Inventory")

    search = st.text_input("Search Inventory", placeholder="Search by name or category")

    shown_items = inventory

    if search.strip():
        shown_items = [
            item for item in inventory
            if search.lower() in item["name"].lower()
            or search.lower() in item["category"].lower()
        ]

    if not shown_items:
        st.info("No matching products found.")
        return

    for item in shown_items:
        render_inventory_card(item)


def render_owner_add_product():
    inventory = load_inventory()

    st.header("Add Product")

    with st.form("add_product_form"):
        name = st.text_input("Product Name")
        category = st.text_input("Category")
        price = st.number_input("Price", min_value=0.0, step=0.50)
        stock = st.number_input("Starting Stock", min_value=0, step=1)
        threshold = st.number_input("Low Stock Threshold", min_value=1, value=5, step=1)

        submitted = st.form_submit_button("Add Product", use_container_width=True)

        if submitted:
            if not name.strip() or not category.strip():
                st.error("Product name and category are required.")
                return

            new_product = {
                "id": get_next_id(inventory),
                "name": name.strip(),
                "category": category.strip(),
                "price": float(price),
                "stock": int(stock),
                "sold": 0,
                "low_stock_threshold": int(threshold),
                "created_by": st.session_state.current_user["username"]
            }

            inventory.append(new_product)
            save_inventory(inventory)

            st.success("Product added successfully.")
            st.rerun()


def render_owner_update_product():
    inventory = load_inventory()

    st.header("Update Product")

    if not inventory:
        st.info("No products available.")
        return

    product_options = {
        f"{item['id']} - {item['name']} | Stock: {item['stock']}": item
        for item in inventory
    }

    selected_label = st.selectbox("Select Product", list(product_options.keys()))
    selected_item = product_options[selected_label]

    with st.form("update_product_form"):
        updated_name = st.text_input("Product Name", value=selected_item["name"])
        updated_category = st.text_input("Category", value=selected_item["category"])
        updated_price = st.number_input(
            "Price",
            min_value=0.0,
            value=float(selected_item["price"]),
            step=0.50
        )
        updated_stock = st.number_input(
            "Stock",
            min_value=0,
            value=int(selected_item["stock"]),
            step=1
        )
        updated_threshold = st.number_input(
            "Low Stock Threshold",
            min_value=1,
            value=int(selected_item["low_stock_threshold"]),
            step=1
        )

        submitted = st.form_submit_button("Save Changes", use_container_width=True)

        if submitted:
            for item in inventory:
                if int(item["id"]) == int(selected_item["id"]):
                    item["name"] = updated_name.strip()
                    item["category"] = updated_category.strip()
                    item["price"] = float(updated_price)
                    item["stock"] = int(updated_stock)
                    item["low_stock_threshold"] = int(updated_threshold)

            save_inventory(inventory)

            st.success("Product updated successfully.")
            st.rerun()


def render_owner_delete_product():
    inventory = load_inventory()

    st.header("Delete Product")

    if not inventory:
        st.info("No products available.")
        return

    product_options = {
        f"{item['id']} - {item['name']} | {item['category']}": item
        for item in inventory
    }

    selected_label = st.selectbox("Select Product to Delete", list(product_options.keys()))
    selected_item = product_options[selected_label]

    st.warning(f"You are about to delete **{selected_item['name']}**.")

    confirm = st.checkbox("I understand this product will be deleted.")

    if st.button("Delete Product", use_container_width=True):
        if not confirm:
            st.error("Check the confirmation box first.")
            return

        updated_inventory = [
            item for item in inventory
            if int(item["id"]) != int(selected_item["id"])
        ]

        save_inventory(updated_inventory)

        st.success("Product deleted.")
        st.rerun()


def render_employee_flags():
    flags = load_flags()

    st.header("Employee Flags")

    if not flags:
        st.info("No employee flags submitted yet.")
        return

    for flag in flags:
        render_flag_card(flag)


def render_employee_dashboard():
    inventory = load_inventory()
    flags = load_flags()
    low_stock_items = get_low_stock_items(inventory)

    st.header("Employee Dashboard")

    col1, col2, col3 = st.columns(3)
    col1.metric("Products Available", len(inventory))
    col2.metric("Low Stock Items", len(low_stock_items))
    col3.metric("Submitted Flags", len(flags))

    st.divider()

    st.subheader("Low Stock Alerts")

    if low_stock_items:
        for item in low_stock_items:
            render_inventory_card(item)
    else:
        st.success("No low-stock items right now.")


def render_employee_catalog():
    inventory = load_inventory()

    st.header("Product Catalog")

    search = st.text_input("Search Products", placeholder="Search by name or category")

    shown_items = inventory

    if search.strip():
        shown_items = [
            item for item in inventory
            if search.lower() in item["name"].lower()
            or search.lower() in item["category"].lower()
        ]

    if not shown_items:
        st.info("No matching products found.")
        return

    for item in shown_items:
        render_inventory_card(item)


def render_employee_log_sale():
    inventory = load_inventory()

    st.header("Log Sale")

    available_items = [
        item for item in inventory
        if int(item["stock"]) > 0
    ]

    if not available_items:
        st.info("No products available for sale.")
        return

    product_options = {
        f"{item['id']} - {item['name']} | Stock: {item['stock']} | ${float(item['price']):.2f}": item
        for item in available_items
    }

    selected_label = st.selectbox("Select Product Sold", list(product_options.keys()))
    selected_item = product_options[selected_label]

    quantity = st.number_input(
        "Quantity Sold",
        min_value=1,
        max_value=int(selected_item["stock"]),
        step=1
    )

    sale_total = float(selected_item["price"]) * int(quantity)
    st.write(f"Sale total: **${sale_total:.2f}**")

    if st.button("Submit Sale", use_container_width=True):
        for item in inventory:
            if int(item["id"]) == int(selected_item["id"]):
                item["stock"] = int(item["stock"]) - int(quantity)
                item["sold"] = int(item.get("sold", 0)) + int(quantity)

        save_inventory(inventory)

        st.success("Sale logged. Inventory updated.")
        st.rerun()


def render_submit_inventory_flag():
    inventory = load_inventory()
    flags = load_flags()

    st.header("Submit Inventory Flag")

    if not inventory:
        st.info("No products available.")
        return

    product_options = {
        f"{item['id']} - {item['name']} | Stock: {item['stock']}": item
        for item in inventory
    }

    selected_label = st.selectbox("Select Product", list(product_options.keys()))
    selected_item = product_options[selected_label]

    reason = st.text_area(
        "Reason",
        value=(
            f"{selected_item['name']} currently has {selected_item['stock']} unit(s) in stock. "
            f"The low-stock threshold is {selected_item['low_stock_threshold']}."
        )
    )

    if st.button("Submit Flag", use_container_width=True):
        new_flag = {
            "id": get_next_id(flags),
            "item_id": selected_item["id"],
            "item_name": selected_item["name"],
            "flagged_by": st.session_state.current_user["username"],
            "reason": reason,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        flags.append(new_flag)
        save_flags(flags)

        st.success("Inventory flag submitted.")
        st.rerun()


def render_inventory_assistant():
    inventory = load_inventory()
    low_stock_items = get_low_stock_items(inventory)
    out_of_stock_items = get_out_of_stock_items(inventory)

    st.header("Inventory Assistant")
    st.caption("Phase 1 simulated AI assistant with 5 hardcoded responses.")

    question = st.selectbox(
        "Choose a question",
        [
            "What items are low on stock?",
            "What items are out of stock?",
            "How many products are in inventory?",
            "What is the most expensive product?",
            "What should we restock today?"
        ]
    )

    if st.button("Ask Assistant", use_container_width=True):
        if question == "What items are low on stock?":
            if low_stock_items:
                names = [
                    f"{item['name']} ({item['stock']} left)"
                    for item in low_stock_items
                ]
                st.write("Low-stock items: " + ", ".join(names))
            else:
                st.write("No items are currently low on stock.")

        elif question == "What items are out of stock?":
            if out_of_stock_items:
                names = [item["name"] for item in out_of_stock_items]
                st.write("Out-of-stock items: " + ", ".join(names))
            else:
                st.write("No items are currently out of stock.")

        elif question == "How many products are in inventory?":
            st.write(f"There are {len(inventory)} products in inventory.")

        elif question == "What is the most expensive product?":
            if inventory:
                most_expensive = max(inventory, key=lambda item: float(item["price"]))
                st.write(
                    f"The most expensive product is {most_expensive['name']} "
                    f"at ${float(most_expensive['price']):.2f}."
                )
            else:
                st.write("No products found.")

        elif question == "What should we restock today?":
            if low_stock_items:
                names = [item["name"] for item in low_stock_items]
                st.write("You should restock: " + ", ".join(names))
            else:
                st.write("No restocking is needed right now.")


def render_owner_app():
    render_user_sidebar(st.session_state.current_user, st.session_state.role)

    if st.sidebar.button("Logout", use_container_width=True):
        logout_session()
        st.rerun()

    page = owner_navigation()
    show_flash()

    if page == "Dashboard":
        render_owner_dashboard()
    elif page == "View Inventory":
        render_owner_view_inventory()
    elif page == "Add Product":
        render_owner_add_product()
    elif page == "Update Product":
        render_owner_update_product()
    elif page == "Delete Product":
        render_owner_delete_product()
    elif page == "Employee Flags":
        render_employee_flags()
    elif page == "Inventory Assistant":
        render_inventory_assistant()


def render_employee_app():
    render_user_sidebar(st.session_state.current_user, st.session_state.role)

    if st.sidebar.button("Logout", use_container_width=True):
        logout_session()
        st.rerun()

    page = employee_navigation()
    show_flash()

    if page == "Dashboard":
        render_employee_dashboard()
    elif page == "Product Catalog":
        render_employee_catalog()
    elif page == "Log Sale":
        render_employee_log_sale()
    elif page == "Submit Inventory Flag":
        render_submit_inventory_flag()
    elif page == "Inventory Assistant":
        render_inventory_assistant()


def main():
    setup_page()
    ensure_data_files()
    init_session_state()
    render_header()

    if not st.session_state.logged_in:
        render_login_page()
        return

    if st.session_state.role == "owner":
        render_owner_app()
    elif st.session_state.role == "employee":
        render_employee_app()
    else:
        st.error("Invalid role. Please log in again.")
        logout_session()
        st.rerun()


main()