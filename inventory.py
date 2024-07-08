import sqlite3
import datetime
import tkinter as tk
from tkinter import messagebox, ttk

# Setup the database
def setup_database():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        quantity INTEGER,
        sale_date TEXT,
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    )
    ''')
    
    conn.commit()
    conn.close()

# Run database setup
setup_database()

def add_product(name, quantity, price):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO products (name, quantity, price)
    VALUES (?, ?, ?)
    ''', (name, quantity, price))
    
    conn.commit()
    conn.close()

def update_product(product_id, name, quantity, price):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    UPDATE products
    SET name = ?, quantity = ?, price = ?
    WHERE product_id = ?
    ''', (name, quantity, price, product_id))
    
    conn.commit()
    conn.close()

def delete_product(product_id):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    DELETE FROM products
    WHERE product_id = ?
    ''', (product_id,))
    
    conn.commit()
    conn.close()

def record_sale(product_id, quantity):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    sale_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute('''
    INSERT INTO sales (product_id, quantity, sale_date)
    VALUES (?, ?, ?)
    ''', (product_id, quantity, sale_date))
    
    cursor.execute('''
    UPDATE products
    SET quantity = quantity - ?
    WHERE product_id = ?
    ''', (quantity, product_id))
    
    conn.commit()
    conn.close()

def generate_inventory_report():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT * FROM products
    ''')
    
    products = cursor.fetchall()
    
    for product in products:
        print(f"Product ID: {product[0]}, Name: {product[1]}, Quantity: {product[2]}, Price: {product[3]}")
    
    conn.close()

def generate_sales_report():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT * FROM sales
    ''')
    
    sales = cursor.fetchall()
    
    for sale in sales:
        print(f"Sale ID: {sale[0]}, Product ID: {sale[1]}, Quantity: {sale[2]}, Sale Date: {sale[3]}")
    
    conn.close()

# Tkinter GUI
class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management")
        
        # Product management frame
        self.frame = ttk.LabelFrame(self.root, text="Product Management")
        self.frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        ttk.Label(self.frame, text="Product ID:").grid(row=0, column=0, padx=5, pady=5)
        self.product_id_entry = ttk.Entry(self.frame)
        self.product_id_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.frame, text="Name:").grid(row=1, column=0, padx=5, pady=5)
        self.name_entry = ttk.Entry(self.frame)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self.frame, text="Quantity:").grid(row=2, column=0, padx=5, pady=5)
        self.quantity_entry = ttk.Entry(self.frame)
        self.quantity_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(self.frame, text="Price:").grid(row=3, column=0, padx=5, pady=5)
        self.price_entry = ttk.Entry(self.frame)
        self.price_entry.grid(row=3, column=1, padx=5, pady=5)
        
        self.add_button = ttk.Button(self.frame, text="Add Product", command=self.add_product)
        self.add_button.grid(row=4, column=0, padx=5, pady=5)
        
        self.update_button = ttk.Button(self.frame, text="Update Product", command=self.update_product)
        self.update_button.grid(row=4, column=1, padx=5, pady=5)
        
        self.delete_button = ttk.Button(self.frame, text="Delete Product", command=self.delete_product)
        self.delete_button.grid(row=5, column=0, padx=5, pady=5)
        
        self.record_sale_button = ttk.Button(self.frame, text="Record Sale", command=self.record_sale)
        self.record_sale_button.grid(row=5, column=1, padx=5, pady=5)
        
        # Report generation frame
        self.report_frame = ttk.LabelFrame(self.root, text="Reports")
        self.report_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        
        self.inventory_report_button = ttk.Button(self.report_frame, text="Generate Inventory Report", command=self.generate_inventory_report)
        self.inventory_report_button.grid(row=0, column=0, padx=5, pady=5)
        
        self.sales_report_button = ttk.Button(self.report_frame, text="Generate Sales Report", command=self.generate_sales_report)
        self.sales_report_button.grid(row=0, column=1, padx=5, pady=5)
    
    def add_product(self):
        name = self.name_entry.get()
        quantity = int(self.quantity_entry.get())
        price = float(self.price_entry.get())
        add_product(name, quantity, price)
        messagebox.showinfo("Success", "Product added successfully!")
    
    def update_product(self):
        product_id = int(self.product_id_entry.get())
        name = self.name_entry.get()
        quantity = int(self.quantity_entry.get())
        price = float(self.price_entry.get())
        update_product(product_id, name, quantity, price)
        messagebox.showinfo("Success", "Product updated successfully!")
    
    def delete_product(self):
        product_id = int(self.product_id_entry.get())
        delete_product(product_id)
        messagebox.showinfo("Success", "Product deleted successfully!")
    
    def record_sale(self):
        product_id = int(self.product_id_entry.get())
        quantity = int(self.quantity_entry.get())
        record_sale(product_id, quantity)
        messagebox.showinfo("Success", "Sale recorded successfully!")
    
    def generate_inventory_report(self):
        generate_inventory_report()
        messagebox.showinfo("Report", "Inventory report generated! Check the console.")
    
    def generate_sales_report(self):
        generate_sales_report()
        messagebox.showinfo("Report", "Sales report generated! Check the console.")

if __name__ == "__main__":
    setup_database()
    
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()
