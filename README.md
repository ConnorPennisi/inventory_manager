# Small Business Inventory Manager

A Streamlit-based internal operations portal for a small retail business. This app helps a shop track inventory, manage products, log sales, and monitor low-stock items through two role-based dashboards: **Owner** and **Employee**.

## Project Overview

This project was built as a Phase 1 MVP for a MISY350 course project. The goal of the MVP is to demonstrate:

- User registration and login
- Session state management
- Role-based routing
- JSON-based data storage
- Meaningful CRUD operations
- A usable workflow for both user roles

## Roles

### Shop Owner
The owner can:
- Add new products
- Update product details
- Restock inventory by editing stock values
- Delete discontinued products
- Review employee low-stock flags

### Employee
The employee can:
- View the current product catalog
- Log daily sales
- Reduce inventory when sales are recorded
- Flag items that are running dangerously low
- Use the Phase 1 simulated inventory assistant

## Features

- **Authentication system**
  - Register a new account
  - Log in with valid credentials
  - Log out securely using session state

- **Session state**
  - Keeps users logged in during the app session
  - Stores current user and role
  - Supports a smoother multi-step workflow

- **Role-based dashboards**
  - Owners and employees are sent to different interfaces after login
  - Each role has access only to the actions relevant to their workflow

- **JSON-backed storage**
  - User records are stored in `data/users.json`
  - Inventory records are stored in `data/inventory.json`
  - Employee flags are stored in `data/flags.json`

- **CRUD operations**
  - Owner: create, update, and delete inventory items
  - Employee: read inventory, log sales, and submit low-stock flags

- **Phase 1 simulated AI assistant**
  - Includes 5 hardcoded question/response options
  - Uses current JSON inventory data to generate simple responses

## Project Structure

```text
inventory_manager/
├── app.py
├── auth.py
├── data_access.py
├── ui.py
├── utils.py
├── requirements.txt
├── .gitignore
└── data/
    ├── users.json
    ├── inventory.json
    └── flags.json
