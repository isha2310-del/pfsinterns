import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

def create_database():
    conn = sqlite3.connect('hotel.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Guests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guest_id INTEGER,
            room_number INTEGER,
            check_in DATE,
            check_out DATE,
            FOREIGN KEY(guest_id) REFERENCES Guests(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guest_id INTEGER,
            amount REAL,
            date DATE,
            FOREIGN KEY(guest_id) REFERENCES Guests(id)
        )
    ''')
    conn.commit()
    conn.close()

class HotelManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System")

        self.create_widgets()

    def create_widgets(self):
        tab_control = ttk.Notebook(self.root)
        
        self.guest_tab = ttk.Frame(tab_control)
        self.reservation_tab = ttk.Frame(tab_control)
        self.invoice_tab = ttk.Frame(tab_control)
        
        tab_control.add(self.guest_tab, text='Guests')
        tab_control.add(self.reservation_tab, text='Reservations')
        tab_control.add(self.invoice_tab, text='Invoices')
        
        tab_control.pack(expand=1, fill='both')
        
        self.create_guest_tab()
        self.create_reservation_tab()
        self.create_invoice_tab()

    def create_guest_tab(self):
        self.guest_list = ttk.Treeview(self.guest_tab, columns=("ID", "Name", "Email", "Phone"), show="headings")
        self.guest_list.heading("ID", text="ID")
        self.guest_list.heading("Name", text="Name")
        self.guest_list.heading("Email", text="Email")
        self.guest_list.heading("Phone", text="Phone")
        self.guest_list.pack()

        self.refresh_guest_list()

        ttk.Button(self.guest_tab, text="Add Guest", command=self.add_guest).pack()
        ttk.Button(self.guest_tab, text="Update Guest", command=self.update_guest).pack()
        ttk.Button(self.guest_tab, text="Delete Guest", command=self.delete_guest).pack()

    def refresh_guest_list(self):
        for i in self.guest_list.get_children():
            self.guest_list.delete(i)

        conn = sqlite3.connect('hotel.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Guests")
        for row in cursor.fetchall():
            self.guest_list.insert("", "end", values=row)
        conn.close()

    def add_guest(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Guest")

        ttk.Label(add_window, text="Name:").grid(row=0, column=0)
        name_entry = ttk.Entry(add_window)
        name_entry.grid(row=0, column=1)

        ttk.Label(add_window, text="Email:").grid(row=1, column=0)
        email_entry = ttk.Entry(add_window)
        email_entry.grid(row=1, column=1)

        ttk.Label(add_window, text="Phone:").grid(row=2, column=0)
        phone_entry = ttk.Entry(add_window)
        phone_entry.grid(row=2, column=1)

        def save_guest():
            name = name_entry.get()
            email = email_entry.get()
            phone = phone_entry.get()

            if not name or not email or not phone:
                messagebox.showwarning("Warning", "All fields are required.")
                return

            conn = sqlite3.connect('hotel.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Guests (name, email, phone) VALUES (?, ?, ?)", (name, email, phone))
            conn.commit()
            conn.close()

            add_window.destroy()
            self.refresh_guest_list()

        ttk.Button(add_window, text="Save", command=save_guest).grid(row=3, column=0, columnspan=2)

    def update_guest(self):
        
        pass

    def delete_guest(self):
        selected_item = self.guest_list.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Select a guest to delete.")
            return

        guest_id = self.guest_list.item(selected_item[0])["values"][0]

        conn = sqlite3.connect('hotel.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Guests WHERE id = ?", (guest_id,))
        conn.commit()
        conn.close()

        self.refresh_guest_list()

    def create_reservation_tab(self):
        
        pass

    def create_invoice_tab(self):
        
        pass

if __name__ == "__main__":
    create_database()
    root = tk.Tk()
    app = HotelManagementApp(root)
    root.mainloop()
