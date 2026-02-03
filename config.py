"""
Configuration file for ShopInsight Pro
Contains all constants, file paths, and configuration settings
"""

from pathlib import Path

# File paths for data storage
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

USERS_FILE = DATA_DIR / "users.json"
BUSINESSES_FILE = DATA_DIR / "businesses.json"
SALES_FILE = DATA_DIR / "sales.json"
INVENTORY_FILE = DATA_DIR / "inventory.json"
ORDERS_FILE = DATA_DIR / "orders.json"
DEBTS_FILE = DATA_DIR / "debts.json"

# Business types
BUSINESS_TYPES = [
    "Retail Shop",
    "Restaurant",
    "Grocery Store",
    "Electronics",
    "Clothing",
    "Services",
    "Other"
]

# Order statuses
ORDER_STATUSES = ["Pending", "Completed", "Cancelled"]

# Debt statuses
DEBT_STATUSES = ["Pending", "Partially Paid", "Paid"]

# Debt types
DEBT_TYPES = ["Receivable (They owe you)", "Payable (You owe them)"]

# Inventory categories
INVENTORY_CATEGORIES = [
    "Electronics",
    "Clothing",
    "Food",
    "Accessories",
    "Raw Materials",
    "Finished Goods",
    "Other"
]

# Analytics time periods
TIME_PERIODS = ["Last 7 Days", "Last 30 Days", "Last 90 Days", "All Time"]

# Default admin credentials
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "admin123"

# App settings
APP_NAME = "ShopInsight Pro"
APP_ICON = "📊"
APP_TAGLINE = "Business Analytics & Management Platform"

# Thresholds for insights
LOW_PROFIT_MARGIN_THRESHOLD = 20  # %
HIGH_PROFIT_MARGIN_THRESHOLD = 40  # %
DEBT_WARNING_RATIO = 0.3  # 30% of revenue
LOW_STOCK_THRESHOLD = 10  # units
SALES_GROWTH_THRESHOLD = 1.2  # 20% growth
SALES_DECLINE_THRESHOLD = 0.8  # 20% decline
