from data_access import load_users, save_users, get_next_id


def find_user_by_username(username):
    users = load_users()

    for user in users:
        if user["username"].lower() == username.lower():
            return user

    return None


def login_user(username, password):
    if not username.strip() or not password.strip():
        return False, None, "Username and password are required."

    user = find_user_by_username(username)

    if user is None:
        return False, None, "No account found with that username."

    if user["password"] != password:
        return False, None, "Incorrect password."

    return True, user, "Login successful."


def register_user(name, username, password, role):
    users = load_users()

    if not name.strip():
        return False, "Name is required."

    if not username.strip():
        return False, "Username is required."

    if not password.strip():
        return False, "Password is required."

    if role not in ["owner", "employee"]:
        return False, "Invalid role selected."

    existing_user = find_user_by_username(username)

    if existing_user:
        return False, "That username already exists."

    new_user = {
        "id": get_next_id(users),
        "name": name.strip(),
        "username": username.strip(),
        "password": password.strip(),
        "role": role
    }

    users.append(new_user)
    save_users(users)

    return True, "Account created successfully. Please log in."