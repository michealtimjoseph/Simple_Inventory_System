import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import csv
import datetime

# =============================================================================
# Inventory Manager: Handles CSV‑Based Data Persistence
# =============================================================================
class InventoryManager:
    def __init__(self, csv_file="inventory.csv"):
        self.csv_file = csv_file
        self.items = []
        self.load_inventory_data()

    def load_inventory_data(self):
        try:
            with open(self.csv_file, "r", newline="") as csvfile:
                reader = csv.DictReader(csvfile)
                self.items.clear()
                for row in reader:
                    row["price"] = float(row["price"])
                    row["quantity"] = int(row["quantity"])
                    row["max"] = int(row["max"])
                    if not row.get("category"):
                        row["category"] = "Other"
                    self.items.append(row)
        except FileNotFoundError:
            # No CSV exists; start with an empty inventory.
            pass
        except Exception as e:
            messagebox.showerror("Load Error", f"Error loading inventory data:\n{e}")

    def save_inventory_data(self):
        try:
            with open(self.csv_file, "w", newline="") as csvfile:
                fieldnames = ["name", "price", "quantity", "max", "category"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for item in self.items:
                    writer.writerow(item)
        except Exception as e:
            messagebox.showerror("Save Error", f"Error saving inventory data:\n{e}")

# =============================================================================
# Main Application: CleverMartApp
# =============================================================================
class CleverMartApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CleverMart")
        self.root.geometry("700x500")
        self.root.resizable(False, False)
        self.root.config(bg="gray20")

        self.inventory_manager = InventoryManager()

        self.cart = []                 # Current purchase cart.
        self.sales_history = []        # Detailed per-item sales.
        self.transaction_history = []  # Overall purchase transactions.
        self.load_transaction_data()
        self.current_category = "Snacks & Sweets"
        self.previous_screen = None

        self.product_widgets = []
        self.guest_frame = None
        self.admin_frame = None
        self.inventory_tree = None

        self.setup_welcome_screen()

    # ------------------------------------------------------------------------------
    # Transaction Data Persistence Methods
    # ------------------------------------------------------------------------------
    def load_transaction_data(self):
        try:
            with open("transactions.csv", "r", newline="") as csvfile:
                reader = csv.DictReader(csvfile)
                self.transaction_history.clear()
                for row in reader:
                    row["total_sale"] = float(row["total_sale"])
                    row["total_profit"] = float(row["total_profit"])
                    row["tendered"] = float(row["tendered"])
                    row["change"] = float(row["change"])
                    self.transaction_history.append(row)
        except FileNotFoundError:
            self.transaction_history = []
        except Exception as e:
            messagebox.showerror("Load Error", f"Error loading transactions data:\n{e}")

    def save_transaction_data(self):
        try:
            with open("transactions.csv", "w", newline="") as csvfile:
                fieldnames = ["date", "total_sale", "total_profit", "tendered", "change"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for trans in self.transaction_history:
                    writer.writerow(trans)
        except Exception as e:
            messagebox.showerror("Save Error", f"Error saving transactions data:\n{e}")

    # ------------------------------------------------------------------------------
    # Welcome Screen & Root Clearing Utility
    # ------------------------------------------------------------------------------
    def setup_welcome_screen(self):
        self.clear_root()
        self.welcome_label = tk.Label(self.root, text="Welcome to CleverMart!",
                                      font=("Comic Sans MS", 28, "italic"), fg="white", bg="gray20")
        self.welcome_label.place(relx=0.5, rely=0.2, anchor="center")
        self.guest_button = tk.Button(self.root, text="Start as Guest", font=("Arial", 12),
                                      bg="gray30", fg="white", width=20, height=2,
                                      command=self.start_as_guest)
        self.guest_button.place(relx=0.5, rely=0.4, anchor="center")
        self.admin_button = tk.Button(self.root, text="Continue as Admin", font=("Arial", 12),
                                      bg="gray35", fg="white", width=20, height=2,
                                      command=self.admin_authentication)
        self.admin_button.place(relx=0.5, rely=0.55, anchor="center")
        self.tagline_label = tk.Label(self.root, text="Organized shopping, simplified systems!",
                                      font=("Courier New", 14, "bold"), fg="lightgray", bg="gray20")
        self.tagline_label.place(relx=0.5, rely=0.7, anchor="center")

    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ------------------------------------------------------------------------------
    # Guest Interface & Shop Screen
    # ------------------------------------------------------------------------------
    def start_as_guest(self):
        self.previous_screen = "guest"
        self.clear_root()
        self.guest_frame = tk.Frame(self.root, bg="gray30")
        self.guest_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)
        guest_title = tk.Label(self.guest_frame, text="Welcome to CleverMart",
                               font=("Segoe UI", 30, "bold"), fg="white", bg="gray30")
        guest_title.pack(pady=(20, 10))
        guest_info = tk.Label(self.guest_frame,
                              text="Discover a modern shopping experience with fresh styles and unbeatable deals.",
                              font=("Segoe UI", 14), fg="lightgray", bg="gray30", wraplength=500, justify="center")
        guest_info.pack(pady=(0, 20))
        shop_button = tk.Button(self.guest_frame, text="Shop Now",
                                font=("Arial", 12), bg="gray40", fg="white", width=20, height=2,
                                command=lambda: self.display_shop_screen("Snacks & Sweets"))
        shop_button.pack(pady=(0, 10))
        exit_button = tk.Button(self.guest_frame, text="Exit",
                                font=("Arial", 12), bg="gray50", fg="white", width=20, height=2,
                                command=self.root.quit)
        exit_button.pack(pady=(0, 10))
        return_button = tk.Button(self.guest_frame, text="Return Home",
                                  font=("Arial", 12), bg="gray40", fg="white", width=20, height=2,
                                  command=self.setup_welcome_screen)
        return_button.pack(pady=(0, 10))

    def display_shop_screen(self, selected_category="Snacks & Sweets"):
        self.previous_screen = "guest"
        self.current_category = selected_category
        self.clear_root()

        shop_frame = tk.Frame(self.root, bg="gray20")
        shop_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.95, relheight=0.9)

        top_bar = tk.Frame(shop_frame, bg="gray30")
        top_bar.pack(fill="x", padx=10, pady=10)
        snacks_btn = tk.Button(top_bar, text="Snacks & Sweets", font=("Segoe UI", 12), bg="gray35", fg="white", command=lambda: self.display_shop_screen("Snacks & Sweets"))
        snacks_btn.pack(side="left", padx=5)
        beverages_btn = tk.Button(top_bar, text="Beverages", font=("Segoe UI", 12), bg="gray35", fg="white", command=lambda: self.display_shop_screen("Beverages"))
        beverages_btn.pack(side="left", padx=5)
        cart_btn = tk.Button(top_bar, text="View Cart", font=("Segoe UI", 12), bg="dodgerblue", fg="white", command=self.view_cart)
        cart_btn.pack(side="right", padx=5)

        title_label = tk.Label(shop_frame, text=selected_category, font=("Segoe UI", 20, "bold"), bg="gray20", fg="white")
        title_label.pack(pady=(0, 10))

        canvas = tk.Canvas(shop_frame, bg="gray20", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar = ttk.Scrollbar(shop_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)
        inner_frame = tk.Frame(canvas, bg="gray20")
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")
        inner_frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
        inner_frame.grid_columnconfigure(0, weight=1)
        inner_frame.grid_columnconfigure(1, weight=1)

        filtered_products = [prod for prod in self.inventory_manager.items if prod.get("category") == selected_category]
        if not filtered_products:
            no_prod_label = tk.Label(inner_frame, text="No products available in this category.", font=("Segoe UI", 14), bg="gray20", fg="lightgray")
            no_prod_label.pack(pady=20)
        else:
            max_cols = 2
            for idx, prod in enumerate(filtered_products):
                row = idx // max_cols
                col = idx % max_cols

                max_stock = prod.get("max", prod["quantity"])
                current_stock = prod["quantity"]
                if current_stock >= 0.75 * max_stock:
                    stock_color = "green"
                elif current_stock >= 0.25 * max_stock:
                    stock_color = "yellow"
                else:
                    stock_color = "red"

                card = tk.Frame(inner_frame, bg="gray40", bd=2, relief="solid", padx=15, pady=10)
                card.grid(row=row, column=col, padx=10, pady=10, sticky="n")

                header_frame = tk.Frame(card, bg=stock_color)
                header_frame.pack(fill="x", padx=5, pady=2)
               
                name_label = tk.Label(header_frame, text=prod["name"], font=("Segoe UI", 14, "bold"),bg=stock_color, fg="white")
                name_label.pack(side="left", padx=10)

                content_frame = tk.Frame(card, bg="gray40")
                content_frame.pack(fill="x")
               
                marked_price = prod["price"] * 1.10
               
                price_label = tk.Label(content_frame, text=f"Price: ₱{marked_price:.2f}", font=("Segoe UI", 12),bg="gray40", fg="white")
                price_label.pack(side="left", padx=10)
               
                stock_label = tk.Label(content_frame, text=f"Stock: {current_stock}", font=("Segoe UI", 12), bg="gray40", fg="lightgray")
                stock_label.pack(side="right", padx=10)

                qty_var = tk.IntVar(value=1)
                qty_frame = tk.Frame(card, bg="gray40")
                qty_frame.pack(pady=5)
               
                minus_btn = tk.Button(qty_frame, text="-", font=("Segoe UI", 10), width=3,bg="gray50", fg="white", command=lambda var=qty_var: var.set(max(1, var.get() - 1)))
                minus_btn.pack(side="left", padx=2)
               
                qty_display = tk.Label(qty_frame, textvariable=qty_var, font=("Segoe UI", 10), width=4, bg="gray50", fg="white", relief="solid", bd=1)
                qty_display.pack(side="left", padx=2)
               
                plus_btn = tk.Button(qty_frame, text="+", font=("Segoe UI", 10), width=3, bg="gray50", fg="white", command=lambda var=qty_var: var.set(var.get() + 1))
                plus_btn.pack(side="left", padx=2)

                btn_frame = tk.Frame(card, bg="gray40")
                btn_frame.pack(pady=(5, 10), fill="x")
               
                add_cart_btn = tk.Button(btn_frame, text="Add to Cart", font=("Segoe UI", 12), bg="blue", fg="white", relief="flat", command=lambda p=prod, var=qty_var: self.add_to_cart(p, var.get(), checkout=False))
                add_cart_btn.pack(side="left", expand=True, fill="x", padx=2)
               
                buy_now_btn = tk.Button(btn_frame, text="Buy Now", font=("Segoe UI", 12), bg="green", fg="white", relief="flat",command=lambda p=prod, var=qty_var: self.add_to_cart(p, var.get(), checkout=True))
                buy_now_btn.pack(side="left", expand=True, fill="x", padx=2)

                card.bind("<Enter>", lambda event, frame=card: frame.config(bg="gray50"))
                card.bind("<Leave>", lambda event, frame=card: frame.config(bg="gray40"))

        return_button = tk.Button(shop_frame, text="Return Home", font=("Segoe UI", 14), bg="gray30", fg="white", command=self.setup_welcome_screen)
        return_button.pack(pady=(10, 20))
        self.product_widgets.append(return_button)

    # ------------------------------------------------------------------------------
    # add_to_cart: Accepts a checkout flag.
    # ------------------------------------------------------------------------------
    def add_to_cart(self, product, qty, checkout=False):
        if product["quantity"] < qty:
            messagebox.showerror("Stock Error", f"Insufficient stock for {product['name']}.")
            return
        for item in self.cart:
            if item["name"] == product["name"]:
                item["quantity"] += qty
                messagebox.showinfo("Cart", f"Added {qty} x {product['name']} to your cart!")
                if checkout:
                    self.view_cart()
                return
        self.cart.append({"name": product["name"], "price": product["price"], "quantity": qty})
        messagebox.showinfo("Cart", f"Added {qty} x {product['name']} to your cart!")
        if checkout:
            self.view_cart()

    # ------------------------------------------------------------------------------
    # view_cart: Checkout Screen.
    # ------------------------------------------------------------------------------
    def view_cart(self):
        cart_win = tk.Toplevel(self.root)
        cart_win.title("Checkout")
        cart_win.geometry("500x600")
        cart_win.resizable(False, False)
        cart_win.config(bg="gray20")

        header_frame = tk.Frame(cart_win, bg="gray10")
        header_frame.pack(fill="x")
        header_label = tk.Label(header_frame, text="Checkout", font=("Segoe UI", 20, "bold"), fg="white", bg="gray10", pady=10)
        header_label.pack()

        content_frame = tk.Frame(cart_win, bg="gray20")
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", background="gray30", fieldbackground="gray30", foreground="white")
        style.map("Treeview", background=[('selected', 'gray')])

        tree_frame = tk.Frame(content_frame, bg="gray20")
        tree_frame.pack(fill="both", expand=True)
        columns = ("Product", "Price", "Quantity", "Subtotal")
        cart_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=8)
       
        for col in columns:
            cart_tree.heading(col, text=col)
            cart_tree.column(col, anchor="center", width=100)
        cart_tree.pack(side="left", fill="both", expand=True)
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=cart_tree.yview)
        vsb.pack(side="right", fill="y")
        cart_tree.configure(yscrollcommand=vsb.set)

        total_label = tk.Label(content_frame, text="Total: ₱0.00", font=("Segoe UI", 16, "bold"), fg="white", bg="gray20")
        total_label.pack(pady=(10, 0))

        pay_frame = tk.Frame(content_frame, bg="gray20")
        pay_frame.pack(pady=10)
        
        tendered_label = tk.Label(pay_frame, text="Amount Tendered:", font=("Segoe UI", 12),fg="white", bg="gray20")
        tendered_label.grid(row=0, column=0, padx=5, pady=5)
       
        amount_entry = tk.Entry(pay_frame, font=("Segoe UI", 12), width=10, bg="gray30", fg="white", insertbackground="white")
        amount_entry.grid(row=0, column=1, padx=5, pady=5)
       
        change_label = tk.Label(content_frame, text="Change: ₱0.00", font=("Segoe UI", 16, "bold"),fg="white", bg="gray20")
        change_label.pack(pady=(5, 10))

        button_frame = tk.Frame(content_frame, bg="gray20")
        button_frame.pack(pady=10)
        
        def refresh_cart():
            cart_tree.delete(*cart_tree.get_children())
            new_total = 0
            for item in self.cart:
                marked_price = item["price"] * 1.10
                subtotal = marked_price * item["quantity"]
                new_total += subtotal
                cart_tree.insert("", "end", values=(item["name"], f"₱{marked_price:.2f}", item["quantity"], f"₱{subtotal:.2f}"))
            total_label.config(text=f"Total: ₱{new_total:.2f}")
            return new_total

        def deduct_item():
            selected_item = cart_tree.selection()
            if not selected_item:
                messagebox.showerror("Selection Error", "Please select an item to deduct.")
                return
            item_values = cart_tree.item(selected_item[0], "values")
            product_name = item_values[0]
            for cart_item in self.cart:
                if cart_item["name"] == product_name:
                    if cart_item["quantity"] > 1:
                        cart_item["quantity"] -= 1
                        messagebox.showinfo("Cart", f"Deducted 1 unit of {product_name}.")
                    else:
                        if messagebox.askyesno("Remove Item", f"Do you want to remove {product_name} from the cart?"):
                            self.cart.remove(cart_item)
                    break
            refresh_cart()

        def process_payment():
            try:
                tendered = float(amount_entry.get())
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid amount.")
                return
            current_total = sum(item["price"] * 1.10 * item["quantity"] for item in self.cart)
            if tendered < current_total:
                messagebox.showerror("Payment Error", "Insufficient amount tendered.")
                return
            change = tendered - current_total
            change_label.config(text=f"Change: ₱{change:.2f}")
            for cart_item in self.cart:
                product = next((p for p in self.inventory_manager.items if p["name"] == cart_item["name"]), None)
                if product:
                    product["quantity"] -= cart_item["quantity"]
                    if product["quantity"] <= 0:
                        self.inventory_manager.items.remove(product)
            self.inventory_manager.save_inventory_data()
            for cart_item in self.cart:
                self.sales_history.append({
                    "name": cart_item["name"],
                    "quantity": cart_item["quantity"],
                    "cost": cart_item["price"],
                    "selling_price": cart_item["price"] * 1.10
                })
            transaction = {
                "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "total_sale": current_total,
                "total_profit": sum(cart_item["price"] * 0.10 * cart_item["quantity"] for cart_item in self.cart),
                "tendered": tendered,
                "change": change
            }
            self.transaction_history.append(transaction)
            self.save_transaction_data()
            messagebox.showinfo("Payment Successful", f"Payment accepted. Your change is ₱{change:.2f}.")
            self.cart.clear()
            cart_win.destroy()

        def return_home():
            if messagebox.askyesno("Return Home", "Returning home will clear your cart. Proceed?"):
                self.cart.clear()
                cart_win.destroy()
                self.setup_welcome_screen()

        deduct_btn = tk.Button(button_frame, text="Deduct Item", font=("Segoe UI", 12), bg="#cc6600", fg="white", command=deduct_item)
        clear_cart_btn = tk.Button(button_frame, text="Clear Cart", font=("Segoe UI", 12),bg="#cc0000", fg="white", command=lambda: (self.cart.clear(), refresh_cart()))
        pay_btn = tk.Button(button_frame, text="Process Payment", font=("Segoe UI", 12), bg="#009900", fg="white", command=process_payment)
        return_btn = tk.Button(button_frame, text="Return Home", font=("Segoe UI", 12), bg="gray35", fg="white", command=return_home)

        deduct_btn.grid(row=0, column=0, padx=5, pady=5)
        clear_cart_btn.grid(row=0, column=1, padx=5, pady=5)
        pay_btn.grid(row=0, column=2, padx=5, pady=5)
        return_btn.grid(row=0, column=3, padx=5, pady=5)

        refresh_cart()

    # ------------------------------------------------------------------------------
    # Admin Authentication & Dashboard
    # ------------------------------------------------------------------------------
    def admin_authentication(self):
        auth_win = tk.Toplevel(self.root)
        auth_win.title("Admin Login")
        auth_win.geometry("300x200")
        auth_win.resizable(False, False)
        auth_win.config(bg="gray20")
       
        username_label = tk.Label(auth_win, text="Username:", bg="gray20", fg="white")
        username_label.grid(row=0, column=0, padx=10, pady=(20,5), sticky="w")
       
        username_entry = tk.Entry(auth_win, width=25, bg="gray30", fg="white", insertbackground="white")
        username_entry.grid(row=0, column=1, padx=10, pady=(20,5))
       
        password_label = tk.Label(auth_win, text="Password:", bg="gray20", fg="white")
        password_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
       
        password_entry = tk.Entry(auth_win, width=25, show="*", bg="gray30", fg="white", insertbackground="white")
        password_entry.grid(row=1, column=1, padx=10, pady=5)

        def authenticate():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            if username == "admin" and password == "1234":
                messagebox.showinfo("Login Successful", "Welcome, Admin!")
                auth_win.destroy()
                self.continue_as_admin()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")

        login_btn = tk.Button(auth_win, text="Login", font=("Arial", 12), bg="gray35", fg="white", width=10, command=authenticate)
        login_btn.grid(row=2, column=0, padx=(20, 10), pady=(20, 10))
       
        cancel_btn = tk.Button(auth_win, text="Cancel", font=("Arial", 12),bg="gray50", fg="white", width=10, command=auth_win.destroy)
        cancel_btn.grid(row=2, column=1, padx=(10, 20), pady=(20, 10))

    def continue_as_admin(self):
        self.previous_screen = "admin"
        self.clear_root()
        self.admin_frame = tk.Frame(self.root, bg="gray20")
        self.admin_frame.place(relx=0.5, rely=0.5, anchor="center", width=700, height=500)
       
        admin_title = tk.Label(self.admin_frame, text="CleverMart Admin Dashboard",
                               font=("Segoe UI", 20, "italic"), fg="white", bg="gray20")
        admin_title.pack(pady=(20, 10))
       
        inventory_button = tk.Button(self.admin_frame, text="Inventory Management",
                         font=("Segoe UI", 12), bg="blue", fg="white",
                         width=20, height=2, command=self.inventory_management)
        inventory_button.pack(pady=(15, 5))
       
        pos_button = tk.Button(self.admin_frame, text="Point of Sale",
                       font=("Segoe UI", 12), bg="green", fg="white",
                       width=20, height=2, command=self.pos_interface)
        pos_button.pack(pady=(15, 5))
       
        monitoring_button = tk.Button(self.admin_frame, text="Stock Monitoring",
                          font=("Segoe UI", 12), bg="orange", fg="white",
                          width=20, height=2, command=self.stock_monitoring)
        monitoring_button.pack(pady=(15, 5))
       
        logout_button = tk.Button(self.admin_frame, text="Logout", font=("Segoe UI", 10),
                      bg="red", fg="white", command=self.setup_welcome_screen)
        logout_button.place(relx=0.0, rely=1.0, anchor="sw", x=10, y=-10)

    # ------------------------------------------------------------------------------
    # Inventory Management
    # ------------------------------------------------------------------------------
    def inventory_management(self):
        for widget in self.admin_frame.winfo_children():
            widget.destroy()

        # Center-align the title label
        title_label = tk.Label(self.admin_frame, text="Inventory Management", font=("Segoe UI", 16, "bold"), fg="white", bg="gray20")
        title_label.pack(pady=(10, 20))

        # Add controls frame for search and filter options
        controls_frame = tk.Frame(self.admin_frame, bg="gray20")
        controls_frame.pack(pady=(0, 20))

        search_label = tk.Label(controls_frame, text="Search:", font=("Segoe UI", 10), bg="gray20", fg="white")
        search_label.grid(row=0, column=0, padx=5, pady=5)
        search_entry = tk.Entry(controls_frame, font=("Segoe UI", 10), width=20, bg="gray30", fg="white", insertbackground="white")
        search_entry.grid(row=0, column=1, padx=5, pady=5)

        category_label = tk.Label(controls_frame, text="Category:", font=("Segoe UI", 10), bg="gray20", fg="white")
        category_label.grid(row=0, column=2, padx=5, pady=5)
        category_var = tk.StringVar()
        category_combobox = ttk.Combobox(controls_frame, textvariable=category_var, values=["All", "Snacks & Sweets", "Beverages"], state="readonly", width=15)
        category_combobox.grid(row=0, column=3, padx=5, pady=5)
        category_combobox.current(0)

        search_btn = tk.Button(controls_frame, text="Filter", font=("Segoe UI", 10), bg="blue", fg="white", command=lambda: self.filter_inventory(search_entry.get(), category_var.get()))
        search_btn.grid(row=0, column=4, padx=5, pady=5)

        reset_btn = tk.Button(controls_frame, text="Reset", font=("Segoe UI", 10), bg="blue", fg="white", command=lambda: self.populate_inventory_table())
        reset_btn.grid(row=0, column=5, padx=5, pady=5)

        # Add a treeview for inventory items
        tree_frame = tk.Frame(self.admin_frame, bg="gray20")
        tree_frame.pack(pady=(0, 20), fill="both", expand=True)

        columns = ("Product Name", "Price", "Quantity")
        self.inventory_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")
        self.inventory_tree.heading("Product Name", text="Product Name")
        self.inventory_tree.heading("Price", text="Price")
        self.inventory_tree.heading("Quantity", text="Quantity")
        self.inventory_tree.column("Product Name", anchor="w", width=200)
        self.inventory_tree.column("Price", anchor="center", width=100)
        self.inventory_tree.column("Quantity", anchor="center", width=100)

        tree_vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.inventory_tree.yview)
        self.inventory_tree.configure(yscrollcommand=tree_vsb.set)
        self.inventory_tree.pack(side="left", fill="both", expand=True)
        tree_vsb.pack(side="right", fill="y")

        # Populate the inventory table
        self.populate_inventory_table()

        # Add buttons for inventory actions
        btn_frame = tk.Frame(self.admin_frame, bg="gray20")
        btn_frame.pack(pady=(10, 10))

        add_btn = tk.Button(btn_frame, text="Add Product", font=("Segoe UI", 10), width=15, bg="blue", fg="white", command=self.add_product_window)
        add_btn.grid(row=0, column=0, padx=10, pady=5)

        edit_btn = tk.Button(btn_frame, text="Edit Product", font=("Segoe UI", 10), width=15, bg="green", fg="white", command=self.edit_product_window)
        edit_btn.grid(row=0, column=1, padx=10, pady=5)

        delete_btn = tk.Button(btn_frame, text="Delete Product", font=("Segoe UI", 10), width=15, bg="red", fg="white", command=self.delete_product)
        delete_btn.grid(row=0, column=2, padx=10, pady=5)

        back_btn = tk.Button(btn_frame, text="Back", font=("Segoe UI", 10), width=15, bg="gray40", fg="white", command=self.continue_as_admin)
        back_btn.grid(row=0, column=3, padx=10, pady=5)

    def populate_inventory_table(self):
        if self.inventory_tree:
            self.inventory_tree.delete(*self.inventory_tree.get_children())
            for item in self.inventory_manager.items:
                self.inventory_tree.insert("", "end", values=(item["name"], f"₱{item['price']:.2f}", item["quantity"]))

    def filter_inventory(self, query, category):
        if self.inventory_tree:
            self.inventory_tree.delete(*self.inventory_tree.get_children())
            for item in self.inventory_manager.items:
                if query.lower() in item["name"].lower() and (category == "All" or item["category"] == category):
                    self.inventory_tree.insert("", "end", values=(item["name"], f"₱{item['price']:.2f}", item["quantity"]))

    # ------------------------------------------------------------------------------
    # Stock Monitoring with Restock Functionality
    # ------------------------------------------------------------------------------
    def stock_monitoring(self):
        for widget in self.admin_frame.winfo_children():
            widget.destroy()
        title_label = tk.Label(self.admin_frame, text="Stock Monitoring",
                               font=("Segoe UI", 16, "bold"), fg="white", bg="gray20")
        title_label.pack(pady=5)
        columns = ("Product Name", "Current Stock", "Max Stock", "Status")
        stock_tree = ttk.Treeview(self.admin_frame, columns=columns, show="headings", selectmode="browse")
        for col in columns:
            stock_tree.heading(col, text=col)
            if col == "Product Name":
                stock_tree.column(col, width=200, anchor="w")
            else:
                stock_tree.column(col, width=100, anchor="center")
        stock_tree.pack(pady=5, padx=5, expand=True, fill="both")
        
        stock_tree.tag_configure("Sufficient stock", background="green")
        stock_tree.tag_configure("Moderate stock", background="yellow")
        stock_tree.tag_configure("Nearly out of stock", background="red")
        
        for product in self.inventory_manager.items:
            max_stock = product.get("max", product["quantity"])
            current = product["quantity"]
            if current >= 0.75 * max_stock:
                tag = "Sufficient stock"
            elif current >= 0.25 * max_stock:
                tag = "Moderate stock"
            else:
                tag = "Nearly out of stock"
            stock_tree.insert("", "end", values=(product["name"], current, max_stock, tag.capitalize()), tags=(tag,))
        
        btn_frame = tk.Frame(self.admin_frame, bg="gray20")
        btn_frame.pack(pady=5)
        
        def restock_item():
            selected = stock_tree.selection()
            if not selected:
                messagebox.showerror("Selection Error", "Please select a product to restock.")
                return
            item_id = selected[0]
            item_values = stock_tree.item(item_id, "values")
            product_name = item_values[0]
            status = item_values[3].lower()  # e.g., "nearly out of stock"
            if status != "nearly out of stock":
                messagebox.showinfo("Info", f"Product '{product_name}' does not require restocking.")
                return
            add_qty = simpledialog.askinteger("Restock Item", f"Enter quantity to add for '{product_name}':", minvalue=1)
            if add_qty is None:
                return
            for product in self.inventory_manager.items:
                if product["name"] == product_name:
                    product["quantity"] += add_qty
                    break
            self.inventory_manager.save_inventory_data()
            messagebox.showinfo("Success", f"Product '{product_name}' restocked with {add_qty} units.")
            self.stock_monitoring()
        
        restock_btn = tk.Button(btn_frame, text="Restock Item", font=("Segoe UI", 10), bg="blue", fg="white", command=restock_item)
        restock_btn.grid(row=0, column=0, padx=10, pady=5)
        back_btn = tk.Button(btn_frame, text="Back", font=("Segoe UI", 10), bg="gray40", fg="white", command=self.continue_as_admin)
        back_btn.grid(row=0, column=1, padx=10, pady=5)

    # ------------------------------------------------------------------------------
    # pos_interface: Sales History and Aggregated Summary
    # ------------------------------------------------------------------------------
    def pos_interface(self):
        for widget in self.admin_frame.winfo_children():
            widget.destroy()
        pos_title = tk.Label(self.admin_frame, text="Sales History",
                             font=("Segoe UI", 20, "bold"), fg="white", bg="gray20")
        pos_title.pack(pady=10)
        total_sales = sum(t["total_sale"] for t in self.transaction_history)
        total_profit = sum(t["total_profit"] for t in self.transaction_history)
        summary_label = tk.Label(self.admin_frame, text=f"Total Sales: ₱{total_sales:.2f}    Total Profit: ₱{total_profit:.2f}", font=("Segoe UI", 16, "bold"), bg="gray20", fg="white")
        summary_label.pack(pady=5)
        if not self.sales_history:
            no_sales_label = tk.Label(self.admin_frame, text="No sales have been recorded.", font=("Segoe UI", 14), bg="gray20", fg="lightgray")
            no_sales_label.pack(pady=20)
        else:
            columns = ("Product", "Quantity", "Cost Price", "Selling Price", "Profit")
            sales_tree = ttk.Treeview(self.admin_frame, columns=columns, show="headings", height=10)
            for col in columns:
                sales_tree.heading(col, text=col)
                sales_tree.column(col, anchor="center", width=100)
            sales_tree.pack(pady=10, padx=10, fill="both", expand=True)
            for sale in self.sales_history:
                profit = (sale["selling_price"] - sale["cost"]) * sale["quantity"]
                sales_tree.insert("", "end", values=(
                    sale["name"],
                    sale["quantity"],
                    f"₱{sale['cost']:.2f}",
                    f"₱{sale['selling_price']:.2f}",
                    f"₱{profit:.2f}"))
        view_history_btn = tk.Button(self.admin_frame, text="View Purchase History", font=("Segoe UI", 10), bg="#0055aa", fg="white", command=self.view_purchase_history)
        view_history_btn.pack(pady=5)
        back_button = tk.Button(self.admin_frame, text="Back", font=("Segoe UI", 10),bg="gray40", fg="white", command=self.continue_as_admin)
        back_button.pack(pady=5)

    # ------------------------------------------------------------------------------
    # view_purchase_history: Displays overall purchase transactions
    # ------------------------------------------------------------------------------
    def view_purchase_history(self):
        trans_win = tk.Toplevel(self.root)
        trans_win.title("Purchase History")
        trans_win.geometry("500x350")
        trans_win.resizable(False, False)
        trans_win.config(bg="gray20")
        trans_frame = tk.Frame(trans_win, bg="gray20")
        trans_frame.pack(pady=10, padx=10, fill="both", expand=True)
        columns = ("Date", "Total Sale", "Total Profit", "Tendered", "Change")
        trans_tree = ttk.Treeview(trans_frame, columns=columns, show="headings")

        for col in columns:
            trans_tree.heading(col, text=col)
            trans_tree.column(col, anchor="center", width=100)
        trans_tree.pack(side="left", fill="both", expand=True)
        trans_scroll = ttk.Scrollbar(trans_frame, orient="vertical", command=trans_tree.yview)
        trans_scroll.pack(side="right", fill="y")
        trans_tree.configure(yscrollcommand=trans_scroll.set)
        for trans in self.transaction_history:
            trans_tree.insert("", "end", values=(
                trans["date"],
                f"₱{trans['total_sale']:.2f}",
                f"₱{trans['total_profit']:.2f}",
                f"₱{trans['tendered']:.2f}",
                f"₱{trans['change']:.2f}" ))
        def clear_history():
            if messagebox.askyesno("Clear History", "Are you sure you want to clear the purchase history?"):
                self.transaction_history.clear()
                self.save_transaction_data()
                trans_tree.delete(*trans_tree.get_children())
                messagebox.showinfo("Cleared", "Purchase history has been cleared.")
        clear_btn = tk.Button(trans_win, text="Clear Purchase History", font=("Segoe UI", 10), bg="red", fg="white", command=clear_history)
        clear_btn.pack(pady=5)

    # ------------------------------------------------------------------------------
    # Add Product Window 
    # ------------------------------------------------------------------------------
    def add_product_window(self):
        add_win = tk.Toplevel(self.root)
        add_win.title("Add Product")
        add_win.geometry("300x300")
        add_win.resizable(False, False)
        add_win.config(bg="gray20")
        name_label = tk.Label(add_win, text="Product Name:", bg="gray20", fg="white")
        name_label.grid(row=0, column=0, padx=10, pady=(20,5), sticky="w")
        name_entry = tk.Entry(add_win, width=25, bg="gray30", fg="white", insertbackground="white")
        name_entry.grid(row=0, column=1, padx=10, pady=(20,5))
        price_label = tk.Label(add_win, text="Price:", bg="gray20", fg="white")
        price_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        price_entry = tk.Entry(add_win, width=25, bg="gray30", fg="white", insertbackground="white")
        price_entry.grid(row=1, column=1, padx=10, pady=5)
        quantity_label = tk.Label(add_win, text="Quantity:", bg="gray20", fg="white")
        quantity_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        quantity_entry = tk.Entry(add_win, width=25, bg="gray30", fg="white", insertbackground="white")
        quantity_entry.grid(row=2, column=1, padx=10, pady=5)
        category_label = tk.Label(add_win, text="Category:", bg="gray20", fg="white")
        category_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        category_var = tk.StringVar()
        category_combobox = ttk.Combobox(add_win, textvariable=category_var, values=["Snacks & Sweets", "Beverages"],state="readonly", width=22)
        category_combobox.grid(row=3, column=1, padx=10, pady=5)
        category_combobox.current(0)
        
        def submit():
            name = name_entry.get().strip()
            price_str = price_entry.get().strip()
            quantity_str = quantity_entry.get().strip()
            category = category_var.get()
            if not name:
                messagebox.showerror("Input Error", "Product name cannot be empty.")
                return
            for product in self.inventory_manager.items:
                if product["name"].lower() == name.lower():
                    messagebox.showerror("Duplicate Error", "A product with this name already exists.")
                    name_entry.delete(0, tk.END)
                    name_entry.focus()
                    return
            try:
                price = float(price_str)
                if price <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Input Error", "Price must be a non-negative number or zero.")
                price_entry.delete(0, tk.END)
                price_entry.focus()
                return
            try:
                quantity = int(quantity_str)
                if quantity <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Input Error", "Quantity must be a non-negative integer or zero.")
                quantity_entry.delete(0, tk.END)
                quantity_entry.focus()
                return
            new_item = {"name": name, "price": price, "quantity": quantity, "max": quantity, "category": category}
            self.inventory_manager.items.append(new_item)
            if self.inventory_tree:
                self.inventory_tree.insert("", "end", values=(name, f"₱{price:.2f}", quantity))
            messagebox.showinfo("Success", "Product added successfully!")
            self.inventory_manager.save_inventory_data()
            if messagebox.askyesno("Continue?", "Product added. Do you want to add another product?"):
                name_entry.delete(0, tk.END)
                price_entry.delete(0, tk.END)
                quantity_entry.delete(0, tk.END)
                category_combobox.current(0)
                name_entry.focus()
            else:
                add_win.destroy()

        submit_btn = tk.Button(add_win, text="Add Product", font=("Segoe UI", 10),bg="blue", fg="white", command=submit)
        submit_btn.grid(row=4, column=0, columnspan=2, pady=(15,5))
        cancel_btn = tk.Button(add_win, text="Cancel", font=("Segoe UI", 10),bg="red", fg="white", command=add_win.destroy)
        cancel_btn.grid(row=5, column=0, columnspan=2, pady=(0,20))

    # ------------------------------------------------------------------------------
    # Edit Product Window
    # ------------------------------------------------------------------------------
    def edit_product_window(self):
        selected = self.inventory_tree.selection()
        if not selected:
            messagebox.showerror("Selection Error", "Please select a product to edit.")
            return
        item_id = selected[0]
        selected_values = self.inventory_tree.item(item_id, "values")
        original_name = selected_values[0]
        original_price = float(selected_values[1].replace("₱", ""))
        original_quantity = int(selected_values[2])
        current_category = "Snacks & Sweets"
        for prod in self.inventory_manager.items:
            if prod["name"] == original_name:
                current_category = prod.get("category", "Snacks & Sweets")
                break
        edit_win = tk.Toplevel(self.root)
        edit_win.title("Edit Product")
        edit_win.geometry("300x300")
        edit_win.resizable(False, False)
        edit_win.config(bg="gray20")
        name_label = tk.Label(edit_win, text="Product Name:", bg="gray20", fg="white")
        name_label.grid(row=0, column=0, padx=10, pady=(20,5), sticky="w")
        name_entry = tk.Entry(edit_win, width=25, bg="gray30", fg="white", insertbackground="white")
        name_entry.grid(row=0, column=1, padx=10, pady=(20,5))
        name_entry.insert(0, original_name)
        price_label = tk.Label(edit_win, text="Price:", bg="gray20", fg="white")
        price_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        price_entry = tk.Entry(edit_win, width=25, bg="gray30", fg="white", insertbackground="white")
        price_entry.grid(row=1, column=1, padx=10, pady=5)
        price_entry.insert(0, str(original_price))
        quantity_label = tk.Label(edit_win, text="Quantity:", bg="gray20", fg="white")
        quantity_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        quantity_entry = tk.Entry(edit_win, width=25, bg="gray30", fg="white", insertbackground="white")
        quantity_entry.grid(row=2, column=1, padx=10, pady=5)
        quantity_entry.insert(0, str(original_quantity))
        category_label = tk.Label(edit_win, text="Category:", bg="gray20", fg="white")
        category_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        category_var = tk.StringVar()
        category_combobox = ttk.Combobox(edit_win, textvariable=category_var,
                                         values=["Snacks & Sweets", "Beverages"],
                                         state="readonly", width=22)
        category_combobox.grid(row=3, column=1, padx=10, pady=5)
        category_combobox.set(current_category)

        def submit_edit():
            new_name = name_entry.get().strip()
            new_price_str = price_entry.get().strip()
            new_quantity_str = quantity_entry.get().strip()
            new_category = category_var.get()
            if not new_name:
                messagebox.showerror("Input Error", "Product name cannot be empty.")
                return
            try:
                new_price = float(new_price_str)
                if new_price <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Input Error", "Price must be a non-negative number or zero.")
                return
            try:
                new_quantity = int(new_quantity_str)
                if new_quantity <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Input Error", "Quantity must be a non-negative integer or zero.")
                return
            self.inventory_tree.item(item_id, values=(new_name, f"₱{new_price:.2f}", new_quantity))
            for product in self.inventory_manager.items:
                if product["name"] == original_name:
                    product["name"] = new_name
                    product["price"] = new_price
                    product["quantity"] = new_quantity
                    product["max"] = new_quantity
                    product["category"] = new_category
                    break
            messagebox.showinfo("Success", "Product updated successfully!")
            self.inventory_manager.save_inventory_data()
            edit_win.destroy()

        submit_btn = tk.Button(edit_win, text="Save Changes", font=("Segoe UI", 10),
                       bg="blue", fg="white", command=submit_edit)
        submit_btn.grid(row=4, column=0, columnspan=2, pady=(15,5))
        cancel_btn = tk.Button(edit_win, text="Cancel", font=("Segoe UI", 10),
                       bg="red", fg="white", command=edit_win.destroy)
        cancel_btn.grid(row=5, column=0, columnspan=2, pady=(0,20))

    # ------------------------------------------------------------------------------
    # Delete Product 
    # ------------------------------------------------------------------------------
    def delete_product(self):
        selected = self.inventory_tree.selection()
        if not selected:
            messagebox.showerror("Selection Error", "Please select a product to delete.")
            return
        item_id = selected[0]
        selected_values = self.inventory_tree.item(item_id, "values")
        product_name = selected_values[0]
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{product_name}'?"):
            self.inventory_tree.delete(item_id)
            for i, product in enumerate(self.inventory_manager.items):
                if product["name"] == product_name:
                    del self.inventory_manager.items[i]
                    break
            messagebox.showinfo("Success", f"Product '{product_name}' deleted successfully!")
            self.inventory_manager.save_inventory_data()

# =============================================================================
# Main Loop
# =============================================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = CleverMartApp(root)
    root.mainloop()
