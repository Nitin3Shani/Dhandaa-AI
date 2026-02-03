"""
Data management utilities
Handles all file operations and data persistence
"""

import json
import hashlib
from datetime import datetime
from config import (
    USERS_FILE, BUSINESSES_FILE, SALES_FILE, 
    INVENTORY_FILE, ORDERS_FILE, DEBTS_FILE,
    DEFAULT_ADMIN_USERNAME, DEFAULT_ADMIN_PASSWORD
)

def load_json(filepath):
    """Load data from JSON file"""
    if filepath.exists():
        with open(filepath, 'r') as f:
            return json.load(f)
    return {}

def save_json(filepath, data):
    """Save data to JSON file"""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def init_data_files():
    """Initialize all data files with default data"""
    # Initialize users file with admin account
    if not USERS_FILE.exists():
        save_json(USERS_FILE, {
            DEFAULT_ADMIN_USERNAME: {
                "password": hash_password(DEFAULT_ADMIN_PASSWORD),
                "type": "admin",
                "created_at": str(datetime.now())
            }
        })
    
    # Initialize other data files
    for file in [BUSINESSES_FILE, SALES_FILE, INVENTORY_FILE, ORDERS_FILE, DEBTS_FILE]:
        if not file.exists():
            save_json(file, {})

def get_user_data(username, data_type):
    """Get data for specific user and data type"""
    file_map = {
        'sales': SALES_FILE,
        'inventory': INVENTORY_FILE,
        'orders': ORDERS_FILE,
        'debts': DEBTS_FILE
    }
    
    if data_type not in file_map:
        return []
    
    data = load_json(file_map[data_type])
    return data.get(username, [])

def save_user_data(username, data_type, new_data):
    """Save data for specific user and data type"""
    file_map = {
        'sales': SALES_FILE,
        'inventory': INVENTORY_FILE,
        'orders': ORDERS_FILE,
        'debts': DEBTS_FILE
    }
    
    if data_type not in file_map:
        return False
    
    all_data = load_json(file_map[data_type])
    
    if username not in all_data:
        all_data[username] = []
    
    all_data[username].append(new_data)
    save_json(file_map[data_type], all_data)
    return True

def update_user_data(username, data_type, updated_list):
    """Update entire data list for a user"""
    file_map = {
        'sales': SALES_FILE,
        'inventory': INVENTORY_FILE,
        'orders': ORDERS_FILE,
        'debts': DEBTS_FILE
    }
    
    if data_type not in file_map:
        return False
    
    all_data = load_json(file_map[data_type])
    all_data[username] = updated_list
    save_json(file_map[data_type], all_data)
    return True

# Initialize data files on module import
init_data_files()
