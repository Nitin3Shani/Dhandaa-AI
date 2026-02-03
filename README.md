# 🏪 ShopInsight Pro - Modular Business Management Platform

A comprehensive, modular business management application for small shops and businesses with AI-powered analytics.

## 📁 Project Structure

```
shopinsight_app/
├── app.py                  # Main application entry point
├── config.py              # Configuration and constants
├── data_manager.py        # Data persistence layer
├── auth.py                # Authentication (login/register)
├── analytics.py           # Analytics calculations & AI insights
├── dashboard.py           # Main dashboard with KPIs
├── sales.py               # Sales management module
├── inventory.py           # Inventory management module
├── orders.py              # Orders management module
├── debts.py               # Debts/receivables management
├── analytics_page.py      # Advanced analytics visualizations
├── user_dashboard.py      # User dashboard orchestration
├── admin_dashboard.py     # Admin panel
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🌟 Features

### Core Modules

#### 1. **Authentication Module** (`auth.py`)
- User registration with business details
- Secure login (password hashing)
- Session management

#### 2. **Sales Management** (`sales.py`)
- Record sales transactions
- Automatic profit calculation
- Customer tracking
- Sales history with export

#### 3. **Inventory Management** (`inventory.py`)
- Add and track inventory items
- Low-stock alerts
- Category-based organization
- Supplier management
- Inventory valuation

#### 4. **Orders Management** (`orders.py`)
- Track pending/completed orders
- Due date monitoring
- Customer order history
- Status-based filtering

#### 5. **Debts & Receivables** (`debts.py`)
- Track receivables (money owed to you)
- Track payables (money you owe)
- Due date alerts
- Payment status tracking

#### 6. **Dashboard** (`dashboard.py`)
- Real-time KPI metrics
- AI-powered insights
- Quick overview charts
- Business health indicators

#### 7. **Advanced Analytics** (`analytics_page.py`)
- Revenue vs profit trends
- Product performance analysis
- Profit margin analysis
- Sales distribution patterns
- Predictive insights
- Growth projections

#### 8. **Admin Panel** (`admin_dashboard.py`)
- View all registered businesses
- Platform statistics
- User activity monitoring
- Business type distribution

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Local Installation

1. **Clone or download the project**
```bash
cd shopinsight_app
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
streamlit run app.py
```

4. **Access the application**
- Open your browser and go to `http://localhost:8501`

### Deploy on Streamlit Cloud (FREE)

1. **Prepare your repository**
   - Create a GitHub repository
   - Upload all files from `shopinsight_app/` to the repository

2. **Deploy**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repository
   - Set main file path: `app.py`
   - Click "Deploy"

3. **Your app will be live!**
   - You'll get a public URL like: `https://yourapp.streamlit.app`

## 🔑 Default Credentials

**Admin Account:**
- Username: `admin`
- Password: `admin123`

**For Users:** Register a new account using the Register tab

## 📖 User Guide

### Getting Started

1. **Register Your Business**
   - Click "Register" tab
   - Fill in your business details
   - Create username and password
   - Submit registration

2. **Login**
   - Use your credentials to login
   - Access your personalized dashboard

3. **Setup Inventory**
   - Navigate to "Inventory" page
   - Add your products with quantities and prices
   - Set reorder levels for low-stock alerts

4. **Record Sales**
   - Go to "Sales" page
   - Enter product details, quantity, and pricing
   - System automatically calculates profit
   - Add customer information (optional)

5. **View Analytics**
   - Check "Dashboard" for quick insights
   - Visit "Analytics" for detailed reports
   - Get AI-powered recommendations

### Module Usage

#### Sales Management
- **Add Sale:** Record each transaction with cost and selling price
- **View History:** See all past sales with filtering options
- **Export Data:** Download sales data as CSV

#### Inventory Management
- **Add Items:** Enter products with categories and reorder levels
- **Monitor Stock:** View items with color-coded status (🟢 In Stock, 🔴 Low Stock)
- **Filter & Search:** Find items by category or stock status
- **Track Value:** See total inventory value in real-time

#### Orders Management
- **Create Orders:** Log customer orders with due dates
- **Track Status:** Monitor pending, completed, and cancelled orders
- **Due Date Alerts:** Get visual warnings for overdue orders (🔴 red highlight)
- **Customer Tracking:** Keep record of all customer orders

#### Debts & Receivables
- **Record Receivables:** Track money customers owe you
- **Record Payables:** Track money you owe to suppliers
- **Due Date Monitoring:** Get alerts for upcoming and overdue payments
- **Payment Status:** Update status as payments are received/made

#### Analytics Features
- **Time Period Selection:** Analyze data for 7, 30, 90 days, or all time
- **Revenue Trends:** Visualize sales patterns over time
- **Product Performance:** Identify best-selling and most profitable products
- **Profit Margins:** See which products have the best margins
- **Predictive Insights:** Get monthly revenue projections
- **Business Health:** Overall performance metrics and recommendations

## 🤖 AI-Powered Insights

The system automatically generates insights including:

1. **Top Performer** - Identifies best-selling products
2. **Profit Margin Analysis** - Alerts on low or excellent margins
3. **Growth Trends** - Detects increasing or declining sales
4. **Debt Alerts** - Warns when debts are too high
5. **Low Stock Alerts** - Notifies when items need restocking
6. **Product Diversity** - Suggests expanding product range

## 💾 Data Storage

All data is stored locally in JSON files:

- `data/users.json` - User accounts
- `data/businesses.json` - Business information
- `data/sales.json` - Sales records
- `data/inventory.json` - Inventory items
- `data/orders.json` - Order tracking
- `data/debts.json` - Debt records

**Note:** Data persists between sessions and is automatically backed up.

## 🔒 Security Features

- Password hashing (SHA-256)
- Session-based authentication
- User data isolation
- Admin/User role separation

## 📊 Analytics Metrics Explained

### Key Performance Indicators (KPIs)
- **Total Revenue:** Sum of all sales amounts
- **Total Profit:** Revenue minus costs
- **Profit Margin:** (Profit / Revenue) × 100%
- **Inventory Value:** Total value of stock on hand
- **Pending Orders:** Value of unfulfilled orders
- **Pending Debts:** Outstanding receivables
- **Net Position:** Revenue minus pending debts

### Advanced Metrics
- **Average Daily Revenue:** Mean revenue per day
- **Recent Trend:** 7-day average vs overall average
- **Projected Monthly:** Estimated revenue for the month
- **Product Performance:** Sales and profit by product
- **Sales Distribution:** Patterns by day of week

## 🎨 Customization

### Modifying Configuration
Edit `config.py` to change:
- Business types
- Inventory categories
- Alert thresholds
- Time periods
- Default settings

### Adding New Features
Each module is independent. To add features:
1. Create a new module file (e.g., `customers.py`)
2. Import in `user_dashboard.py`
3. Add navigation option
4. Update data manager if needed

### Styling
- Streamlit uses default theme
- Can be customized via `.streamlit/config.toml`
- Colors and layouts can be modified in each module

## 🐛 Troubleshooting

### Common Issues

**App won't start:**
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

**Login issues:**
- Verify credentials
- Try default admin account
- Check `data/users.json` file exists

**Data not saving:**
- Ensure `data/` directory exists
- Check file permissions
- Verify JSON files aren't corrupted

**Import errors:**
- Run from the `shopinsight_app/` directory
- All modules must be in same folder
- Check all files are present

## 📈 Best Practices

1. **Daily Usage:**
   - Record sales at end of each day
   - Update inventory as stock arrives
   - Mark orders as completed when fulfilled

2. **Weekly Review:**
   - Check AI insights
   - Review pending orders
   - Follow up on overdue debts
   - Analyze sales trends

3. **Monthly Analysis:**
   - Use Analytics page for deep dive
   - Compare month-over-month performance
   - Adjust strategies based on insights
   - Review profit margins by product

4. **Data Hygiene:**
   - Export data regularly as backup
   - Update inventory quantities
   - Mark completed orders
   - Update debt payment statuses

## 🔄 Backup & Export

All pages with data tables include CSV export:
- Sales data
- Inventory data
- Orders data
- Debts data

**To backup:**
1. Visit each page
2. Click "Download ... Data (CSV)"
3. Store in safe location

## 🚀 Future Enhancements

Potential features you can add:
- PDF report generation
- Email notifications
- Multi-currency support
- Barcode scanning
- Receipt printing
- Customer database
- Expense tracking
- Tax calculations
- Employee management
- Multiple locations/branches

## 📞 Support

For technical issues:
1. Check troubleshooting section
2. Review module comments in code
3. Verify all files are present
4. Check Python and package versions

## 📄 License

Free to use and modify for your business needs!

## 🙏 Credits

Built with:
- [Streamlit](https://streamlit.io/) - Web framework
- [Pandas](https://pandas.pydata.org/) - Data manipulation
- [Plotly](https://plotly.com/) - Interactive visualizations

---

**Happy Business Management! 📊💼**
