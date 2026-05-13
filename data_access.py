import json
from pathlib import Path


DATA_DIR = Path("data")
USERS_FILE = DATA_DIR / "users.json"
INVENTORY_FILE = DATA_DIR / "inventory.json"
FLAGS_FILE = DATA_DIR / "flags.json"


DEFAULT_USERS = [
    {
        "id": 1,
        "name": "Owner Demo",
        "username": "owner",
        "password": "owner123",
        "role": "owner"
    },
    {
        "id": 2,
        "name": "Employee Demo",
        "username": "employee",
        "password": "employee123",
        "role": "employee"
    }
]


DEFAULT_INVENTORY = [
    {
        "id": 1,
        "name": "Hammer",
        "category": "Tools",
        "price": 12.99,
        "stock": 20,
        "sold": 0,
        "low_stock_threshold": 5,
        "created_by": "owner"
    },
    {
        "id": 2,
        "name": "Screwdriver Set",
        "category": "Tools",
        "price": 18.5,
        "stock": 8,
        "sold": 0,
        "low_stock_threshold": 5,
        "created_by": "owner"
    },
    {
        "id": 3,
        "name": "Drill Bits Pack",
        "category": "Hardware",
        "price": 9.99,
        "stock": 4,
        "sold": 0,
        "low_stock_threshold": 5,
        "created_by": "owner"
    },
    {
        "id": 4,
        "name": "Work Gloves",
        "category": "Safety",
        "price": 7.49,
        "stock": 3,
        "sold": 0,
        "low_stock_threshold": 6,
        "created_by": "owner"
    },
    {
        "id": 5,
        "name": "Tape Measure",
        "category": "Tools",
        "price": 11.25,
        "stock": 15,
        "sold": 0,
        "low_stock_threshold": 5,
        "created_by": "owner"
    }
]


def ensure_data_files():
    DATA_DIR.mkdir(exist_ok=True)

    if not USERS_FILE.exists():
        save_json(USERS_FILE, DEFAULT_USERS)

    if not INVENTORY_FILE.exists():
        save_json(INVENTORY_FILE, DEFAULT_INVENTORY)

    if not FLAGS_FILE.exists():
        save_json(FLAGS_FILE, [])


def load_json(file_path):
    if not file_path.exists():
        return []

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(file_path, data):
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def get_next_id(records):
    if not records:
        return 1

    return max(record["id"] for record in records) + 1


def load_users():
    return load_json(USERS_FILE)


def save_users(users):
    save_json(USERS_FILE, users)


def load_inventory():
    return load_json(INVENTORY_FILE)


def save_inventory(inventory):
    save_json(INVENTORY_FILE, inventory)


def load_flags():
    return load_json(FLAGS_FILE)


def save_flags(flags):
    save_json(FLAGS_FILE, flags)