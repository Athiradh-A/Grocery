import customtkinter as ctk
from tkinter import messagebox, simpledialog
import mysql.connector as db
import random
from datetime import datetime
from decimal import Decimal

ADMIN_PASS = "9215627"

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Fresh Groces")
app.geometry("1100x700")
app.configure(bg="#f6f6f6")

sidebar = ctk.CTkFrame(app, width=220, corner_radius=0, fg_color="#fff")
sidebar.pack(side="left", fill="y")
content = ctk.CTkFrame(app, corner_radius=0, fg_color="#fff")
content.pack(side="right", expand=True, fill="both")

def clear_content():
    for widget in content.winfo_children():
        widget.destroy()

# ----------- Checkout Section ----------------

def get_available_items():
    try:
        conn = db.connect(host='localhost', user='root', passwd='admin', database="Grocery")
        cursor = conn.cursor()
        cursor.execute("SELECT Item_name FROM Items WHERE Qty > 0 ORDER BY Item_name")
        items = [row[0] for row in cursor.fetchall()]
        conn.close()
        return items
    except Exception as e:
        messagebox.showerror("DB Error", f"Could not load items: {e}")
        return []

def show_checkout():
    clear_content()
    ctk.CTkLabel(content, text="Checkout Section", font=("Futura", 24, "bold")).pack(pady=18)
    selected_item = ctk.StringVar(value="Select item")
    quantity_var = ctk.StringVar()
    bill_items = []
    total_amount_var = ctk.StringVar(value="0.00")

    form_frame = ctk.CTkFrame(content, fg_color="#f5f5f5", corner_radius=0)
    form_frame.pack(pady=10, padx=10, fill="x")

    ctk.CTkLabel(form_frame, text="Item:", font=("Futura", 15)).grid(row=0, column=0, padx=15, pady=12, sticky="w")
    item_dropdown = ctk.CTkComboBox(form_frame, values=get_available_items(), variable=selected_item, width=250)
    item_dropdown.grid(row=0, column=1, padx=15, pady=12, sticky="w")
    ctk.CTkLabel(form_frame, text="Quantity:", font=("Futura", 15)).grid(row=1, column=0, padx=15, pady=12, sticky="w")
    qty_entry = ctk.CTkEntry(form_frame, textvariable=quantity_var, width=250)
    qty_entry.grid(row=1, column=1, padx=15, pady=12, sticky="w")

    bill_frame = ctk.CTkFrame(content, fg_color="#eee", corner_radius=0)
    bill_frame.pack(padx=10, pady=10, fill="x")
    bill_labels = []

    def update_bill_preview():
        for lb in bill_labels:
            lb.destroy()
        bill_labels.clear()
        headers = ["Item", "Qty", "Rate (₹)", "Amount (₹)"]
        for i, head in enumerate(headers):
            lb = ctk.CTkLabel(bill_frame, text=head, font=("Futura", 14, "bold"), width=150)
            lb.grid(row=0, column=i, padx=12)
            bill_labels.append(lb)
        for idx, item in enumerate(bill_items, start=1):
            for col_idx, key in enumerate(["item", "qty", "rate", "amt"]):
                val = item[key]
                # .quantize for decimals, .normalize() trims trailing zeros
                if key == "qty":
                    val = f"{val.normalize():.3f}"
                elif key in ("rate", "amt"):
                    val = f"{val.normalize():.2f}"
                lb = ctk.CTkLabel(bill_frame, text=str(val), font=("Futura", 13), width=150)
                lb.grid(row=idx, column=col_idx, padx=12)
                bill_labels.append(lb)
        total = sum(x["amt"] for x in bill_items)
        total_amount_var.set(f"{total:.2f}")
        total_lb = ctk.CTkLabel(bill_frame, text=f"Total: ₹ {total:.2f}", font=("Futura", 16, "bold"))
        total_lb.grid(row=len(bill_items)+1, column=0, columnspan=4, pady=12, sticky="w", padx=12)
        bill_labels.append(total_lb)

    def add_to_bill():
        item = selected_item.get()
        if item == "Select item":
            messagebox.showinfo("Input Error", "Please select an item.")
            return
        try:
            qty = Decimal(str(quantity_var.get()))
            if qty <= 0:
                raise ValueError
        except Exception:
            messagebox.showinfo("Input Error", "Enter a valid positive quantity (decimal allowed).")
            return
        try:
            conn = db.connect(host='localhost', user='root', passwd='admin', database="Grocery")
            cursor = conn.cursor()
            cursor.execute("SELECT Price, Qty FROM Items WHERE Item_name=%s", (item,))
            row = cursor.fetchone()
            conn.close()
            if row is None:
                messagebox.showerror("Item Error", "Item not found in inventory.")
                return
            # ALWAYS wrap from DB fetch as string for Decimal math
            price, stock_qty = row
            price = Decimal(str(price))
            stock_qty = Decimal(str(stock_qty))
            if stock_qty < qty:
                messagebox.showerror("Stock Error", f"Only {stock_qty} of '{item}' available.")
                return
            for b_item in bill_items:
                if b_item["item"] == item:
                    b_item["qty"] += qty
                    b_item["amt"] = b_item["rate"] * b_item["qty"]
                    update_bill_preview()
                    return
            amt = price * qty
            bill_items.append({"item": item, "qty": qty, "rate": price, "amt": amt})
            update_bill_preview()
            quantity_var.set("")
            selected_item.set("Select item")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    ctk.CTkButton(form_frame, text="Add to Bill", command=add_to_bill, fg_color="#3399ff").grid(row=2, column=0, columnspan=2, pady=15)

    def finalize_bill():
        if not bill_items:
            messagebox.showinfo("Empty Bill", "Add items before finalizing.")
            return
        bill_no = random.randint(100000, 999999)
        now = datetime.now().strftime("%d/%m/%Y %H:%M")
        subtotal = sum(x["amt"] for x in bill_items)
        tax = (subtotal * Decimal("0.035")).quantize(Decimal("0.01"))
        total = subtotal + tax
        receipt_lines = [
            "        FRESH GROCERY MART",
            "     12 Market Street, Suite 23",
            "      Cityville, NY 12345",
            "         Phone: 555-632-8585",
            "."*38
        ]
        for itm in bill_items:
            name = str(itm["item"])[:18]
            qty = f"{itm['qty'].normalize():.3f}".rstrip('0').rstrip('.')
            amt = f"{itm['amt'].normalize():.2f}"
            receipt_lines.append(f"{name.ljust(14)} x{qty:>6}   ₹{amt:>8}")
        receipt_lines += [
            "",
            f"{'Sub Total':<24}₹{subtotal.normalize():.2f}",
            f"{'Sales Tax':<24}₹{tax:.2f}",
            "."*38,
            f"{'TOTAL':<16}    ₹{total.normalize():.2f}",
            "."*38,
            f"Paid By:{'Credit':>18}",
            "."*38,
            f"Bill No: {bill_no}",
            f"Date: {now}",
            "",
            "Thank You For Supporting",
            "Local Business!".center(38)
        ]
        bill_win = ctk.CTkToplevel(app)
        bill_win.title(f"Receipt #{bill_no}")
        bill_win.geometry("420x600")
        bill_win.resizable(True, True)
        receipt_box = ctk.CTkTextbox(bill_win, width=400, height=580, font=("Futura New", 13))
        receipt_box.pack(padx=10, pady=10, expand=True, fill="both")
        receipt_box.insert("end", "\n".join(receipt_lines))
        receipt_box.configure(state="disabled")
        bill_items.clear()
        update_bill_preview()

    ctk.CTkButton(content, text="Finalize Bill", command=finalize_bill, fg_color="#34a853", font=("Futura", 18, "bold")).pack(pady=10)

# ---------- Admin Password ----------
def prompt_admin_password():
    pw = simpledialog.askstring("Admin Login", "Enter admin password:", show="*")
    return pw == ADMIN_PASS

# ------------- Employee Management -------------
def show_employee():
    clear_content()
    ctk.CTkLabel(content, text="Employee Records (Admin Only)", font=("Futura", 24, "bold")).pack(pady=20)
    if not prompt_admin_password():
        ctk.CTkLabel(content, text="Access Denied", font=("Futura", 16), text_color="red").pack(pady=40)
        return
    emp_list = []
    def load_employees():
        nonlocal emp_list
        try:
            conn = db.connect(host='localhost', user='root', passwd='admin', database="Grocery")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Employee")
            emp_list = cursor.fetchall()
            conn.close()
        except Exception as e:
            messagebox.showerror("DB Error", f"Error loading employees: {e}")
            emp_list = []
    def refresh_employee_table():
        for widget in table_frame.winfo_children():
            widget.destroy()
        headers = ["ID", "Name", "Age", "Salary", "Phone"]
        for c, head in enumerate(headers):
            ctk.CTkLabel(table_frame, text=head, font=("Futura", 13, "bold"), width=100).grid(row=0, column=c, padx=10)
        for r, emp in enumerate(emp_list, start=1):
            for c, val in enumerate(emp):
                ctk.CTkLabel(table_frame, text=str(val), font=("Futura", 12), width=100).grid(row=r, column=c, padx=10)
    def add_employee():
        win = ctk.CTkToplevel(app)
        win.title("Add Employee")
        win.geometry("350x400")
        entries = {}
        fields = ["Employee Id", "Name", "Age", "Salary", "Phone"]
        for i, field in enumerate(fields):
            ctk.CTkLabel(win, text=field).pack(pady=(12 if i==0 else 6, 2))
            entry = ctk.CTkEntry(win, width=280)
            entry.pack()
            entries[field] = entry
        def save():
            try:
                data = (
                    entries["Employee Id"].get(), entries["Name"].get(),
                    int(entries["Age"].get()), float(entries["Salary"].get()),
                    entries["Phone"].get()
                )
                conn = db.connect(host='localhost', user='root', passwd='admin', database="Grocery")
                cursor = conn.cursor()
                cursor.execute("INSERT INTO Employee VALUES (%s,%s,%s,%s,%s)", data)
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Employee added!")
                win.destroy()
                load_employees(); refresh_employee_table()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        ctk.CTkButton(win, text="Save", command=save, fg_color="#34a853").pack(pady=20)
    control_frame = ctk.CTkFrame(content)
    control_frame.pack(pady=12)
    ctk.CTkButton(control_frame, text="Add Employee", fg_color="#3399ff", command=add_employee).pack(side="left", padx=8)
    table_frame = ctk.CTkFrame(content, fg_color="#f1f4f7", corner_radius=0)
    table_frame.pack(padx=10, pady=10, fill="both", expand=True)
    load_employees(); refresh_employee_table()

# --------------- Inventory Management -------------
def show_inventory():
    clear_content()
    ctk.CTkLabel(content, text="Inventory Management (Admin Only)", font=("Futura", 24, "bold")).pack(pady=20)
    if not prompt_admin_password():
        ctk.CTkLabel(content, text="Access Denied", font=("Futura", 16), text_color="red").pack(pady=40)
        return
    inv_list = []
    def load_inventory():
        nonlocal inv_list
        try:
            conn = db.connect(host='localhost', user='root', passwd='admin', database="Grocery")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Items")
            inv_list = cursor.fetchall()
            conn.close()
        except Exception as e:
            messagebox.showerror("DB Error", f"Error loading inventory: {e}")
            inv_list = []
    def refresh_inventory_table():
        for widget in table_frame.winfo_children():
            widget.destroy()
        headers = ["Code", "Name", "Qty", "Price"]
        for c, head in enumerate(headers):
            ctk.CTkLabel(table_frame, text=head, font=("Futura", 13, "bold"), width=100).grid(row=0, column=c, padx=10)
        for r, item in enumerate(inv_list, start=1):
            for c, val in enumerate(item):
                ctk.CTkLabel(table_frame, text=str(val), font=("Futura", 12), width=100).grid(row=r, column=c, padx=10)
    def add_item():
        win = ctk.CTkToplevel(app)
        win.title("Add Item")
        win.geometry("350x400")
        entries = {}
        fields = ["Item Code", "Item Name", "Quantity", "Price"]
        for i, field in enumerate(fields):
            ctk.CTkLabel(win, text=field).pack(pady=(12 if i==0 else 6, 2))
            entry = ctk.CTkEntry(win, width=280)
            entry.pack()
            entries[field] = entry
        def save():
            try:
                data = (
                    entries["Item Code"].get(), entries["Item Name"].get(),
                    Decimal(entries["Quantity"].get()),
                    Decimal(entries["Price"].get())
                )
                conn = db.connect(host='localhost', user='root', passwd='admin', database="Grocery")
                cursor = conn.cursor()
                cursor.execute("INSERT INTO Items VALUES (%s,%s,%s,%s)", data)
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Item added!")
                win.destroy()
                load_inventory(); refresh_inventory_table()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        ctk.CTkButton(win, text="Save", command=save, fg_color="#34a853").pack(pady=20)
    control_frame = ctk.CTkFrame(content)
    control_frame.pack(pady=12)
    ctk.CTkButton(control_frame, text="Add Item", fg_color="#3399ff", command=add_item).pack()
    table_frame = ctk.CTkFrame(content, fg_color="#f1f4f7", corner_radius=0)
    table_frame.pack(padx=10, pady=10, fill="both", expand=True)
    load_inventory(); refresh_inventory_table()

# ------------- Show Items & Prices (read-only) -------------
def show_items():
    clear_content()
    ctk.CTkLabel(content, text="Available Items and Prices", font=("Futura", 24, "bold")).pack(pady=20)
    try:
        conn = db.connect(host='localhost', user='root', passwd='admin', database="Grocery")
        cursor = conn.cursor()
        cursor.execute("SELECT Item_name, Price FROM Items")
        rows = cursor.fetchall()
        conn.close()
    except Exception as e:
        messagebox.showerror("DB Error", f"Error fetching items: {e}")
        return
    table_frame = ctk.CTkFrame(content, fg_color="#f5f7fa", corner_radius=0)
    table_frame.pack(padx=20, pady=10, fill="both", expand=True)
    ctk.CTkLabel(table_frame, text="Item Name", font=("Futura", 15, "bold"), width=200).grid(row=0, column=0, padx=10, pady=10)
    ctk.CTkLabel(table_frame, text="Price (₹)", font=("Futura", 15, "bold"), width=100).grid(row=0, column=1, padx=10, pady=10)
    for i, (iname, price) in enumerate(rows, start=1):
        ctk.CTkLabel(table_frame, text=iname, font=("Futura", 14), width=200).grid(row=i, column=0, padx=10, pady=6)
        ctk.CTkLabel(table_frame, text=f"{price:.2f}", font=("Futura", 14), width=100).grid(row=i, column=1, padx=10, pady=6)

# ------------- Sidebar Buttons / Navigation -------------
ctk.CTkLabel(sidebar, text="Menu", font=("Futura", 21, "bold")).pack(pady=(30,32))
ctk.CTkButton(sidebar, text="Checkout", command=show_checkout, font=("Futura", 15), fg_color="#eaeaea",
              text_color="#343434", corner_radius=12).pack(pady=10, fill="x", padx=10)
ctk.CTkButton(sidebar, text="Show Items & Prices", command=show_items, font=("Futura", 15), fg_color="#eaeaea",
              text_color="#343434", corner_radius=12).pack(pady=10, fill="x", padx=10)
ctk.CTkButton(sidebar, text="Employee Records", command=show_employee, font=("Futura", 15), fg_color="#eaeaea",
              text_color="#343434", corner_radius=12).pack(pady=10, fill="x", padx=10)
ctk.CTkButton(sidebar, text="Inventory", command=show_inventory, font=("Futura", 15), fg_color="#eaeaea",
              text_color="#343434", corner_radius=12).pack(pady=10, fill="x", padx=10)

show_checkout()
app.mainloop()
