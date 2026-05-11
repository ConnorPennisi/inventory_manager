from data_access import get_users, save_users, get_next_id


def register_user(name, username, password, role):
    users = get_users()

    if not name.strip() or not username.strip() or not password.strip():
        return False, "All fields are required."

    if role not in ["owner", "employee"]:
        return False, "Invalid role selected."

    for user in users:
        if user["username"].lower() == username.lower():
            return False, "Username already exists."

    users.append({
        "id": get_next_id(users),
        "name": name.strip(),
        "username": username.strip(),
        "password": password,
        "role": role
    })

    save_users(users)
    return True, "Registration successful. Please log in."


def login_user(username, password):
    users = get_users()

    for user in users:
        if user["username"] == username and user["password"] == password:
            return True, user

    return False, None
