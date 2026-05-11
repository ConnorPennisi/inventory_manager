import json
import os
from datetime import datetime

USERS_FILE = "data/users.json"
INVENTORY_FILE = "data/inventory.json"
FLAGS_FILE = "data/flags.json"


def ensure_file(path, default_data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(default_data, f, indent=2)


def init_data_files():
    ensure_file(USERS_FILE, [])
    ensure_file(INVENTORY_FILE, [])
    ensure_file(FLAGS_FILE, [])


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def get_users():
    return load_json(USERS_FILE)


def save_users(users):
    save_json(USERS_FILE, users)


def get_inventory():
    return load_json(INVENTORY_FILE)


def save_inventory(items):
    save_json(INVENTORY_FILE, items)


def get_flags():
    return load_json(FLAGS_FILE)


def save_flags(flags):
    save_json(FLAGS_FILE, flags)


def get_next_id(records):
    if not records:
        return 1
    return max(record["id"] for record in records) + 1


def add_inventory_item(name, category, price, stock, low_stock_threshold, created_by):
    items = get_inventory()
    item = {
        "id": get_next_id(items),
        "name": name.strip(),
        "category": category.strip(),
        "price": float(price),
        "stock": int(stock),
        "sold": 0,
        "low_stock_threshold": int(low_stock_threshold),
        "created_by": created_by
    }
    items.append(item)
    save_inventory(items)


def update_inventory_item(item_id, name, category, price, stock, low_stock_threshold):
    items = get_inventory()
    for item in items:
        if item["id"] == item_id:
            item["name"] = name.strip()
            item["category"] = category.strip()
            item["price"] = float(price)
            item["stock"] = int(stock)
            item["low_stock_threshold"] = int(low_stock_threshold)
            break
    save_inventory(items)


def delete_inventory_item(item_id):
    items = get_inventory()
    updated_items = [item for item in items if item["id"] != item_id]
    save_inventory(updated_items)


def log_sale(item_id, quantity, employee_username):
    items = get_inventory()

    for item in items:
        if item["id"] == item_id:
            if quantity <= 0:
                return False, "Quantity must be greater than 0."

            if item["stock"] < quantity:
                return False, "Not enough stock available."

            item["stock"] -= quantity
            item["sold"] += quantity
            save_inventory(items)
            return True, f"{employee_username} logged a sale of {quantity} for {item['name']}."

    return False, "Item not found."


def add_flag(item_id, flagged_by, reason):
    flags = get_flags()
    flags.append({
        "id": get_next_id(flags),
        "item_id": item_id,
        "flagged_by": flagged_by,
        "reason": reason.strip(),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    save_flags(flags)
