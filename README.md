
# 🛒 CleverMart - Interactive Inventory & POS System

CleverMart is a Python-based graphical application designed to simulate a modern retail experience. Built using `tkinter`, it features a dual-interface system for **guests** and **administrators**, offering a complete inventory management and point-of-sale (POS) solution.

---

## 🚀 Features

### 👤 Guest Interface
- Browse products by category (e.g., Snacks & Sweets, Beverages)
- Add items to cart and proceed to checkout
- Real-time stock indicators (green/yellow/red)
- Automatic price markup (10%)
- Payment processing with change calculation

### 🔐 Admin Interface
- Secure login (default: `admin` / `1234`)
- Inventory management (add, edit, delete products)
- Stock monitoring with restock prompts
- Sales history and profit tracking
- Purchase transaction logs with exportable CSV support

---

## 🧰 Technologies Used

- **Python 3**
- **tkinter** for GUI
- **csv** for data persistence
- **datetime** for transaction timestamps
---
## 🛒 Get Yours Here
python Download_test_clevermart.py
git clone https://github.com/michealtimjoseph/CleverMart.git
cd CleverMart

---

## 🧑‍💻 How to Use

##  As a Guest:
-  Launch the app and click "Start as Guest"
-  Browse products and add to cart
-  Proceed to checkout and enter payment
-  Receive change and confirmation

##  As an Admin:
-  Click "Continue as Admin" and log in with:
-  Username: admin
-  Password: 1234
-  Access:
-  Inventory Management: Add/edit/delete products
-  Stock Monitoring: View and restock low inventory
-  Point of Sale: View sales and transaction history

##  🗂️ File Structure
-  ComprogFinale.py       # Main application file
-  inventory.csv          # Inventory data (auto-generated)
-  transactions.csv       # Transaction history (auto-generated)

##  💾 Data Persistence
-  All inventory and transaction data are stored in CSV files.
-  Changes are saved automatically after each operation.

##  🔮 Future Improvements
-  User authentication with roles
-  Product image support
-  Export reports to PDF
-  Cloud-based inventory sync

##  📬 Contact
For questions or suggestions, feel free to reach out via GitHub Issues.

📄 License
This project is licensed under the MIT License. See the LICENSE file for details.
