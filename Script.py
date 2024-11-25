import sqlite3
from tkinter import *
from tkinter import messagebox, ttk
from tkinter.ttk import Combobox
import xml.etree.ElementTree as ET
import os

XML_FILE = "data.xml"
DB_FILE = "data.db"
selected_value = "xml"
root = Tk()


def save_client_info():
    name = name_entry.get().strip()
    email = email_entry.get().strip()
    phone = phone_entry.get().strip()
    address = address_entry.get().strip()

    if name and email and phone and address:
        global selected_value
        if selected_value == "xml":
            if os.path.exists(XML_FILE):
                tree = ET.parse(XML_FILE)
                r = tree.getroot()
                clients = r.find("Clients")
                existing_ids = [
                    int(client.get("client_id", 0)) for client in clients.findall("Client")
                ]
                new_id = max(existing_ids, default=0) + 1
            else:
                clients = ET.Element("Clients")
                tree = ET.ElementTree(clients)
                new_id = 1

            client_element = ET.SubElement(clients, "Client",client_id=str(new_id))
            name_element = ET.SubElement(client_element, "Full_Name")
            name_element.text = name
            email_element = ET.SubElement(client_element, "Email")
            email_element.text = email
            phone_element = ET.SubElement(client_element, "Phone")
            phone_element.text = phone
            address_element = ET.SubElement(client_element, "Address")
            address_element.text = address
            messagebox.showinfo("Success", "Client information saved to the xml!")
            tree.write(XML_FILE, encoding="utf-8", xml_declaration=True)
        elif selected_value == "db":
            connection = sqlite3.connect(DB_FILE)
            cursor = connection.cursor()
            cursor.execute("INSERT INTO clients (Full_Name, Email, Phone, Address) VALUES (?, ?, ?, ?)",
                           (name, email, phone, address))
            connection.commit()
            connection.close()

            messagebox.showinfo("Success", "Client information saved to the database!")

        clear_fields()
    else:
        messagebox.showwarning("Error", "All fields are required!")


def save_supplier_info(name,email,phone,address):

    if name and email and phone and address:
        global selected_value
        if selected_value == "xml":
            if os.path.exists(XML_FILE):
                tree = ET.parse(XML_FILE)
                r = tree.getroot()
                suppliers = r.find("Suppliers")
                existing_ids = [
                    int(supplier.get("supplier_id", 0)) for supplier in suppliers.findall("Supplier")
                ]
                new_id = max(existing_ids, default=0) + 1
            else:
                suppliers = ET.Element("Suppliers")
                tree = ET.ElementTree(suppliers)
                new_id = 1

            client_element = ET.SubElement(suppliers, "Supplier",supplier_id=str(new_id))
            name_element = ET.SubElement(client_element, "Full_Name")
            name_element.text = name
            email_element = ET.SubElement(client_element, "Email")
            email_element.text = email
            phone_element = ET.SubElement(client_element, "Phone")
            phone_element.text = phone
            address_element = ET.SubElement(client_element, "Address")
            address_element.text = address
            messagebox.showinfo("Success", "Supplier information saved to the xml!")
            tree.write(XML_FILE, encoding="utf-8", xml_declaration=True)
        elif selected_value == "db":
            connection = sqlite3.connect(DB_FILE)
            cursor = connection.cursor()
            cursor.execute("INSERT INTO suppliers (Full_Name, Email, Phone, Address) VALUES (?, ?, ?, ?)",
                           (name, email, phone, address))
            connection.commit()
            connection.close()

            messagebox.showinfo("Success", "Supplier information saved to the database!")

        clear_fields()
    else:
        messagebox.showwarning("Error", "All fields are required!")


def save_product_info(name, price, category, quantity, supplier_name, src):
    if name and price and category and quantity and supplier_name:
        supplier_id = None
        if src == "xml":
            if os.path.exists(XML_FILE):
                tree = ET.parse(XML_FILE)
                r = tree.getroot()
                products = r.find("Products")
                if products is None:
                    products = ET.SubElement(r, "Products")

                existing_ids = [
                    int(product.get("product_id", 0)) for product in products.findall("Product")
                ]
                product_id = max(existing_ids, default=0) + 1

                suppliers = r.find("Suppliers")
                if suppliers is not None:
                    for supplier in suppliers.findall("Supplier"):
                        if supplier.find("Full_Name").text == supplier_name:
                            supplier_id = supplier.get("supplier_id")
                            break

                product_element = ET.SubElement(products, "Product", product_id=str(product_id))
                ET.SubElement(product_element, "Name").text = name
                ET.SubElement(product_element, "Price").text = price
                ET.SubElement(product_element, "Category").text = category
                ET.SubElement(product_element, "Quantity").text = quantity
                ET.SubElement(product_element, "supplier_id").text = supplier_id

                tree.write(XML_FILE, encoding="utf-8", xml_declaration=True)
                messagebox.showinfo("Success", f"Product has been saved")

        elif src == "db":

            connection = sqlite3.connect(DB_FILE)
            cursor = connection.cursor()

            cursor.execute("SELECT supplier_id FROM suppliers WHERE Full_Name = ?", (supplier_name,))
            result = cursor.fetchone()
            if result:
                supplier_id = result[0]
            else:
                messagebox.showerror("Error", "Supplier not found in database!")
                connection.close()
                return

            cursor.execute(
                "INSERT INTO products (Name, Price, Category, Quantity, supplier_id) "
                "VALUES (?, ?, ?, ?, ?)",
                (name, float(price), category, int(quantity), supplier_id)
            )
            connection.commit()
            connection.close()
            messagebox.showinfo("Success", f"Product has been saved")
    else:
        messagebox.showwarning("Error", "All fields are required!")


def save_order_info(quantity, product_name,client_name, src):

    if quantity and product_name and client_name:
        product_id = None
        client_id = None
        price = 0
        if src == "xml":
            if os.path.exists(XML_FILE):
                tree = ET.parse(XML_FILE)
                r = tree.getroot()
                orders = r.find("Orders")
                if orders is None:
                    orders = ET.SubElement(r, "Orders")

                existing_ids = [
                    int(order.get("order_id", 0)) for order in orders.findall("Order")
                ]
                order_id = max(existing_ids, default=0) + 1

                products = r.find("Products")
                if products is not None:
                    for product in products.findall("Product"):
                        if product.find("Name").text == product_name:
                            product_id = product.get("product_id")
                            price = product.find("Price").text
                            break

                clients = r.find("Clients")
                if clients is not None:
                    for client in clients.findall("Client"):
                        if client.find("Full_Name").text == client_name:
                            client_id = client.get("client_id")
                            break

                order_element = ET.SubElement(orders, "Order", order_id=str(order_id))
                ET.SubElement(order_element, "product_id").text = product_id
                ET.SubElement(order_element, "client_id").text = client_id
                ET.SubElement(order_element, "Quantity").text = quantity
                ET.SubElement(order_element, "Total_Amount").text = str(int(quantity) * float(price))

                tree.write(XML_FILE, encoding="utf-8", xml_declaration=True)
                messagebox.showinfo("Success", f"Order has been saved")

        elif src == "db":

            connection = sqlite3.connect(DB_FILE)
            cursor = connection.cursor()

            cursor.execute("SELECT client_id FROM clients WHERE Full_Name = ?", (client_name,))
            result = cursor.fetchone()
            if result:
                client_id = result[0]
            else:
                messagebox.showerror("Error", "Client not found in database!")
                connection.close()
                return

            cursor.execute("SELECT product_id, Price FROM products WHERE Name = ?", (product_name,))
            result = cursor.fetchone()
            if result:
                product_id = result[0]
                price = result[1]
            else:
                messagebox.showerror("Error", "Product not found in database!")
                connection.close()
                return

            cursor.execute(
                "INSERT INTO orders (Quantity, product_id,client_id,Total_Amount) "
                "VALUES (?, ?, ?, ?)",
                (quantity, product_id,client_id,int(quantity)*float(price))
            )
            connection.commit()
            connection.close()
            messagebox.showinfo("Success", f"Order has been saved")
    else:
        messagebox.showwarning("Error", "All fields are required!")


def show_selection(event):
    global selected_value
    selected_value = event.widget.get()







def switch_to_info_frame():
    show_frame(info_frame)

def new_client():
    switch_to_info_frame()
    combobox.grid(row=5, column=1, pady=10)
    add_label.grid(row=0, columnspan=2, pady=10)
    clear_fields()

def switch_to_clients_list_frame(src):
    clients_list_frame = Frame(root, padx=20, pady=20)
    clients_list_frame.config(bg="#fffcd1")
    clients_list_frame.pack(fill="both", expand=True)

    Label(clients_list_frame, text="Client Information", font=("Arial", 16),bg="#fffcd1").pack(pady=10)


    columns = ("Id","Name", "Email", "Phone", "Address" )
    table = ttk.Treeview(clients_list_frame, columns=columns, show="headings", height=10)
    table.pack(fill="both", expand=True)

    table.heading("Name", text="Name")
    table.heading("Email", text="Email")
    table.heading("Phone", text="Phone")
    table.heading("Address", text="Address")
    table.heading("Id", text="Id")


    table.column("Name", width=150, anchor="center")
    table.column("Email", width=150, anchor="center")
    table.column("Phone", width=100, anchor="center")
    table.column("Address", width=150, anchor="center")
    table.column("Id", width=150, anchor="center")

    delete_button = Button(clients_list_frame, text="Delete Selected", width=15, bg="red", fg="white",command=lambda: delete_selected(table,src))
    delete_button.pack(pady=5)

    update_button = Button(clients_list_frame, text="Update Selected", width=15, bg="blue", fg="white",command=lambda: load_selected_for_update(table,src,"client"))
    update_button.pack(pady=5)

    show_frame(clients_list_frame)
    show_clients(table,src)




def switch_to_suppliers_list_frame(src):
    suppliers_list_frame = Frame(root, padx=20, pady=20)
    suppliers_list_frame.config(bg="#fffcd1")
    suppliers_list_frame.pack(fill="both", expand=True)

    Label(suppliers_list_frame, text="Supplier Information", font=("Arial", 16),bg="#fffcd1").pack(pady=10)


    columns = ("Id","Name", "Email", "Phone", "Address" )
    table = ttk.Treeview(suppliers_list_frame, columns=columns, show="headings", height=10)
    table.pack(fill="both", expand=True)

    table.heading("Name", text="Name")
    table.heading("Email", text="Email")
    table.heading("Phone", text="Phone")
    table.heading("Address", text="Address")
    table.heading("Id", text="Id")


    table.column("Name", width=150, anchor="center")
    table.column("Email", width=150, anchor="center")
    table.column("Phone", width=100, anchor="center")
    table.column("Address", width=150, anchor="center")
    table.column("Id", width=150, anchor="center")

    delete_button = Button(suppliers_list_frame, text="Delete Selected", width=15, bg="red", fg="white",command=lambda: delete_selected_supplier(table,src))
    delete_button.pack(pady=5)

    update_button = Button(suppliers_list_frame, text="Update Selected", width=15, bg="blue", fg="white",command=lambda: load_selected_for_update(table,src,"supplier"))
    update_button.pack(pady=5)

    show_frame(suppliers_list_frame)
    show_suppliers(table,src)

def switch_to_products_list_frame(src):
    products_list_frame = Frame(root, padx=20, pady=20)
    products_list_frame.config(bg="#fffcd1")
    products_list_frame.pack(fill="both", expand=True)
    Label(products_list_frame, text="Product Information", font=("Arial", 16), bg="#fffcd1").pack(pady=10)
    columns = ("Id", "Name", "Price", "Category", "Quantity", "Supplier")
    table = ttk.Treeview(products_list_frame, columns=columns, show="headings", height=10)
    table.pack(fill="both", expand=True)

    table.heading("Id", text="Id")
    table.heading("Name", text="Name")
    table.heading("Price", text="Price")
    table.heading("Category", text="Category")
    table.heading("Quantity", text="Quantity")
    table.heading("Supplier", text="Supplier")

    table.column("Id", width=80, anchor="center")
    table.column("Name", width=150, anchor="center")
    table.column("Price", width=100, anchor="center")
    table.column("Category", width=120, anchor="center")
    table.column("Quantity", width=100, anchor="center")
    table.column("Supplier", width=150, anchor="center")

    delete_button = Button(products_list_frame, text="Delete Selected", width=15, bg="red", fg="white",
                           command=lambda: delete_selected_product(table, src))
    delete_button.pack(pady=5)

    update_button = Button(products_list_frame, text="Update Selected", width=15, bg="blue", fg="white")
    update_button.pack(pady=5)

    show_frame(products_list_frame)
    show_products(table, src)



def switch_to_new_product_frame():
    def set_suppliers(e):
        selected_format = combobox2.get()
        supplier_combobox["values"] = get_suppliers(selected_format)
        if supplier_combobox["values"]:
            supplier_combobox.set(supplier_combobox["values"][0])
        else:
            supplier_combobox.set("No suppliers found")

    def get_suppliers(data_format):
        suppliers = []
        if data_format == "xml":
            if os.path.exists(XML_FILE):
                tree = ET.parse(XML_FILE)
                r = tree.getroot()
                suppliers_element = r.find("Suppliers")
                if suppliers_element is not None:
                    suppliers = [
                        supplier.find("Full_Name").text for supplier in suppliers_element.findall("Supplier")
                    ]
        elif data_format == "db":

            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("SELECT Full_Name FROM suppliers")
            suppliers = [row[0] for row in cursor.fetchall()]
            conn.close()

        return suppliers



    # New Product frame
    product_frame = Frame(root, padx=20, pady=20, bg="#fffcd1")
    product_frame.pack(fill="both", expand=True)

    Label(product_frame, text="Add New Product", font=("Arial", 16), bg="#fffcd1").grid(row=0, columnspan=2, pady=10)
    Label(product_frame, text="Name:", bg="#fffcd1").grid(row=1, column=0, sticky="w", pady=5, padx=5)
    name_product_entry = Entry(product_frame, width=30)
    name_product_entry.grid(row=1, column=1, pady=5)
    Label(product_frame, text="Price:", bg="#fffcd1").grid(row=2, column=0, sticky="w", pady=5, padx=5)
    price_entry = Entry(product_frame, width=30)
    price_entry.grid(row=2, column=1, pady=5)
    Label(product_frame, text="Category:", bg="#fffcd1").grid(row=3, column=0, sticky="w", pady=5, padx=5)
    category_entry = Entry(product_frame, width=30)
    category_entry.grid(row=3, column=1, pady=5)
    Label(product_frame, text="Quantity:", bg="#fffcd1").grid(row=4, column=0, sticky="w", pady=5, padx=5)
    quantity_entry = Entry(product_frame, width=30)
    quantity_entry.grid(row=4, column=1, pady=5)

    Label(product_frame, text="Data Format:", bg="#fffcd1").grid(row=5, column=0, sticky="w", pady=5, padx=5)
    combobox2 = Combobox(product_frame, values=["xml", "db"], state="readonly", width=10)
    combobox2.grid(row=5, column=1, pady=10)
    combobox2.set("xml")
    combobox2.bind("<<ComboboxSelected>>", set_suppliers)

    Label(product_frame, text="Supplier:", bg="#fffcd1").grid(row=6, column=0, sticky="w", pady=5, padx=5)
    supplier_combobox = Combobox(product_frame, state="readonly", width=30)
    supplier_combobox.grid(row=6, column=1, pady=10)
    supplier_combobox.set("Select Supplier")


    save_product_button = Button(product_frame, text="Save", width=10, bg="green", fg="white",
                                 command=lambda : save_product_info(name_product_entry.get().strip(),price_entry.get().strip(),category_entry.get().strip(),quantity_entry.get().strip(),supplier_combobox.get(),combobox2.get()))
    save_product_button.grid(row=7, columnspan=2, pady=20)

    set_suppliers(None)
    show_frame(product_frame)




def switch_to_new_supplier_frame():
    # New Supplier frame
    supplier_frame = Frame(root, padx=20, pady=20, bg="#fffcd1")
    supplier_frame.pack(fill="both", expand=True)

    Label(supplier_frame, text="Add New Supplier", font=("Arial", 16), bg="#fffcd1").grid(row=0, columnspan=2, pady=10)
    Label(supplier_frame, text="Full Name:", bg="#fffcd1").grid(row=1, column=0, sticky="w", pady=5, padx=5)
    name_supplier_entry = Entry(supplier_frame, width=30)
    name_supplier_entry.grid(row=1, column=1, pady=5)
    Label(supplier_frame, text="Email:", bg="#fffcd1").grid(row=2, column=0, sticky="w", pady=5, padx=5)
    email_supplier_entry = Entry(supplier_frame, width=30)
    email_supplier_entry.grid(row=2, column=1, pady=5)
    Label(supplier_frame, text="Phone:", bg="#fffcd1").grid(row=3, column=0, sticky="w", pady=5, padx=5)
    phone_supplier_entry = Entry(supplier_frame, width=30)
    phone_supplier_entry.grid(row=3, column=1, pady=5)
    Label(supplier_frame, text="Address", bg="#fffcd1").grid(row=4, column=0, sticky="w", pady=5, padx=5)
    address_supplier_entry = Entry(supplier_frame, width=30)
    address_supplier_entry.grid(row=4, column=1, pady=5)
    combobox3 = Combobox(supplier_frame, values=["xml", "db"], state="readonly", width=10)
    combobox3.grid(row=5, column=1, pady=10)
    combobox3.set("xml")
    combobox3.bind("<<ComboboxSelected>>", lambda e: show_selection(e))

    save_supplier_button = Button(supplier_frame, text="Save", width=10, bg="green", fg="white",
                                  command=lambda : save_supplier_info(name_supplier_entry.get().strip(),email_supplier_entry.get().strip(),phone_supplier_entry.get().strip(),address_supplier_entry.get().strip()))
    save_supplier_button.grid(row=6, columnspan=2, pady=20)

    show_frame(supplier_frame)


def switch_to_new_order_frame():
    def set_clients(e):
        selected_format = combobox3.get()
        client_combobox["values"] = get_clients(selected_format)
        if client_combobox["values"]:
            client_combobox.set(client_combobox["values"][0])
            set_products(None)
        else:
            client_combobox.set("No suppliers found")

    def set_products(e):
        selected_format = combobox3.get()
        product_combobox["values"] = get_products(selected_format)
        if product_combobox["values"]:
            product_combobox.set(product_combobox["values"][0])
        else:
            product_combobox.set("No suppliers found")

    def get_clients(data_format):
        clients = []
        if data_format == "xml":
            if os.path.exists(XML_FILE):
                tree = ET.parse(XML_FILE)
                r = tree.getroot()
                clients_element = r.find("Clients")
                if clients_element is not None:
                    clients = [
                        client.find("Full_Name").text for client in clients_element.findall("Client")
                    ]
        elif data_format == "db":

            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("SELECT Full_Name FROM clients")
            clients = [row[0] for row in cursor.fetchall()]
            conn.close()

        return clients

    def get_products(data_format):
        products = []
        if data_format == "xml":
            if os.path.exists(XML_FILE):
                tree = ET.parse(XML_FILE)
                r = tree.getroot()
                products_element = r.find("Products")
                if products_element is not None:
                    products = [
                        product.find("Name").text for product in products_element.findall("Product")
                    ]
        elif data_format == "db":

            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("SELECT Name FROM products")
            products = [row[0] for row in cursor.fetchall()]
            conn.close()

        return products



    # New Order frame
    order_frame = Frame(root, padx=20, pady=20, bg="#fffcd1")
    order_frame.pack(fill="both", expand=True)

    Label(order_frame, text="Add New Order", font=("Arial", 16), bg="#fffcd1").grid(row=0, columnspan=2, pady=10)
    Label(order_frame, text="Quantity:", bg="#fffcd1").grid(row=1, column=0, sticky="w", pady=5, padx=5)
    quantity_entry = Entry(order_frame, width=30)
    quantity_entry.grid(row=1, column=1, pady=5)

    Label(order_frame, text="Data Format:", bg="#fffcd1").grid(row=2, column=0, sticky="w", pady=5, padx=5)
    combobox3 = Combobox(order_frame, values=["xml", "db"], state="readonly", width=10)
    combobox3.grid(row=2, column=1, pady=10)
    combobox3.set("xml")
    combobox3.bind("<<ComboboxSelected>>", set_clients)

    Label(order_frame, text="Client:", bg="#fffcd1").grid(row=3, column=0, sticky="w", pady=5, padx=5)
    client_combobox = Combobox(order_frame, state="readonly", width=30)
    client_combobox.grid(row=3, column=1, pady=10)
    client_combobox.set("Select Client")

    Label(order_frame, text="Product:", bg="#fffcd1").grid(row=4, column=0, sticky="w", pady=5, padx=5)
    product_combobox = Combobox(order_frame, state="readonly", width=30)
    product_combobox.grid(row=4, column=1, pady=10)
    product_combobox.set("Select Product")

    save_order_button = Button(order_frame, text="Save", width=10, bg="green", fg="white",
                                 command=lambda: save_order_info(   quantity_entry.get().strip(),
                                                                   product_combobox.get(), client_combobox.get(),combobox3.get()))
    save_order_button.grid(row=5, columnspan=2, pady=20)

    set_clients(None)
    set_products(None)
    show_frame(order_frame)











menu_bar = Menu(root)
client_menu = Menu(menu_bar, tearoff=0)
supplier_menu = Menu(menu_bar, tearoff=0)
product_menu = Menu(menu_bar, tearoff=0)
order_menu = Menu(menu_bar, tearoff=0)

client_menu.add_command(label="New", command=new_client)
supplier_menu.add_command(label="New", command=switch_to_new_supplier_frame)
product_menu.add_command(label="New", command=switch_to_new_product_frame)
order_menu.add_command(label="New", command=switch_to_new_order_frame)


show_client_menu = Menu(client_menu, tearoff=0)
show_client_menu.add_command(label="Show XML", command=lambda: switch_to_clients_list_frame("xml"))
show_client_menu.add_command(label="Show DB", command=lambda: switch_to_clients_list_frame("db"))

show_supplier_menu = Menu(client_menu, tearoff=0)
show_supplier_menu.add_command(label="Show XML", command=lambda: switch_to_suppliers_list_frame("xml"))
show_supplier_menu.add_command(label="Show DB", command=lambda: switch_to_suppliers_list_frame("db"))

show_product_menu = Menu(product_menu, tearoff=0)
show_product_menu.add_command(label="Show XML", command=lambda: switch_to_products_list_frame("xml"))
show_product_menu.add_command(label="Show DB", command=lambda: switch_to_products_list_frame("db"))

client_menu.add_cascade(label="Show", menu=show_client_menu)
product_menu.add_cascade(label="Show", menu=show_product_menu)
supplier_menu.add_cascade(label="Show", menu=show_supplier_menu)

menu_bar.add_cascade(label="Client", menu=client_menu)
menu_bar.add_cascade(label="Supplier", menu=supplier_menu)
menu_bar.add_cascade(label="Product", menu=product_menu)
menu_bar.add_cascade(label="Order", menu=order_menu)
root.config(menu=menu_bar)

# New client frame
info_frame = Frame(root, padx=20, pady=20, bg="#fffcd1")
info_frame.pack(pady=20)

add_label = (Label(info_frame, text="Add New Client", font=("Arial", 16), bg="#fffcd1"))
add_label.grid(row=0, columnspan=2, pady=10)
Label(info_frame, text="Full Name:", bg="#fffcd1").grid(row=1, column=0, sticky="w", pady=5, padx=5)
name_entry = Entry(info_frame, width=30)
name_entry.grid(row=1, column=1, pady=5)
Label(info_frame, text="Email:", bg="#fffcd1").grid(row=2, column=0, sticky="w", pady=5, padx=5)
email_entry = Entry(info_frame, width=30)
email_entry.grid(row=2, column=1, pady=5)
Label(info_frame, text="Phone:", bg="#fffcd1").grid(row=3, column=0, sticky="w", pady=5, padx=5)
phone_entry = Entry(info_frame, width=30)
phone_entry.grid(row=3, column=1, pady=5)
Label(info_frame, text="Address:", bg="#fffcd1").grid(row=4, column=0, sticky="w", pady=5, padx=5)
address_entry = Entry(info_frame, width=30)
address_entry.grid(row=4, column=1, pady=5)


combobox = Combobox(info_frame, values=["xml", "db"], state="readonly", width=10)
combobox.grid(row=5, column=1, pady=10)
combobox.set("xml")
combobox.bind("<<ComboboxSelected>>", lambda e: show_selection(e))

save_button = Button(info_frame, text="Save", command=save_client_info, width=10, bg="green", fg="white")
save_button.grid(row=6, columnspan=2, pady=20)



def show_frame(frame):
    for widget in root.winfo_children():
        widget.pack_forget()
    frame.pack(fill="both", expand=True)




def show_products(table, src):

    for row in table.get_children():
        table.delete(row)

    if src == "xml":
        if os.path.exists(XML_FILE):
            tree = ET.parse(XML_FILE)
            r = tree.getroot()
            products = r.find("Products")
            if products is not None:
                for product in products.findall("Product"):
                    table.insert("", "end", values=(
                        product.get("product_id"),
                        product.find("Name").text,
                        product.find("Price").text,
                        product.find("Category").text,
                        product.find("Quantity").text,
                        product.find("supplier_id").text,
                    ))
    elif src == "db":
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("SELECT product_id, name, price, category, quantity, supplier_id FROM products")
        for row in cursor.fetchall():
            table.insert("", "end", values=row)
        connection.close()


def show_clients(table,src):
    for row in table.get_children():
        table.delete(row)

    if src == "xml":
        try:
            tree = ET.parse(XML_FILE)
            r = tree.getroot()
            clients = r.find("Clients")
            for client in clients.findall("Client"):
                client_id = client.get("client_id", "N/A")
                name = client.find("Full_Name").text if client.find("Full_Name") is not None else "N/A"
                email = client.find("Email").text if client.find("Email") is not None else "N/A"
                phone = client.find("Phone").text if client.find("Phone") is not None else "N/A"
                address = client.find("Address").text if client.find("Address") is not None else "N/A"
                table.insert("", "end", values=(client_id, name, email, phone, address))
        except FileNotFoundError:
            messagebox.showwarning("Error", "No saved clients file found.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load client data: {e}")

    elif src == "db":
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM clients")
        rows = cursor.fetchall()
        connection.close()

        for row in rows:
            table.insert("", "end", values=row)


def show_suppliers(table,src):
    for row in table.get_children():
        table.delete(row)

    if src == "xml":
        try:
            tree = ET.parse(XML_FILE)
            r = tree.getroot()
            suppliers=r.find("Suppliers")
            for supplier in suppliers.findall("Supplier"):
                supplier_id = supplier.get("supplier_id", "N/A")
                name = supplier.find("Full_Name").text if supplier.find("Full_Name") is not None else "N/A"
                email = supplier.find("Email").text if supplier.find("Email") is not None else "N/A"
                phone = supplier.find("Phone").text if supplier.find("Phone") is not None else "N/A"
                address = supplier.find("Address").text if supplier.find("Address") is not None else "N/A"
                table.insert("", "end", values=(supplier_id, name, email, phone, address))
        except FileNotFoundError:
            messagebox.showwarning("Error", "No saved Suppliers file found.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load Supplier data: {e}")

    elif src == "db":
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM suppliers")
        rows = cursor.fetchall()
        connection.close()

        for row in rows:
            table.insert("", "end", values=row)

def delete_selected(table,src):
    selected_item = table.selection()
    if selected_item:
        confirm = messagebox.askyesno("Delete", "Are you sure you want to delete the selected client?")
        if confirm:
            item_values = table.item(selected_item, "values")
            client_id = item_values[0]
            if src == "xml":
                try:
                    tree = ET.parse(XML_FILE)
                    r = tree.getroot()
                    clients = r.find("Clients")
                    for client in clients.findall("Client"):
                        if client.get("client_id") == str(client_id):
                            clients.remove(client)
                            break

                    tree.write(XML_FILE, encoding="utf-8", xml_declaration=True)
                    table.delete(selected_item)
                    messagebox.showinfo("Success", "Client deleted successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete client: {e}")
            elif src == "db":
                connection = sqlite3.connect(DB_FILE)
                cursor = connection.cursor()
                cursor.execute("delete FROM clients where client_id=?", client_id)
                table.delete(selected_item)
                connection.commit()
                connection.close()
                messagebox.showinfo("Success", "Client deleted successfully!")

    else:
        messagebox.showwarning("No Selection", "Please select a client to delete.")



def delete_selected_product(table,src):
    selected_item = table.selection()
    if selected_item:
        confirm = messagebox.askyesno("Delete", "Are you sure you want to delete the selected Product?")
        if confirm:
            item_values = table.item(selected_item, "values")
            product_id = item_values[0]
            if src == "xml":
                try:
                    tree = ET.parse(XML_FILE)
                    r = tree.getroot()
                    products = r.find("Products")
                    for product in products.findall("Product"):
                        if product.get("product_id") == str(product_id):
                            products.remove(product)
                            break

                    tree.write(XML_FILE, encoding="utf-8", xml_declaration=True)
                    table.delete(selected_item)
                    messagebox.showinfo("Success", "Product deleted successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete Product: {e}")
            elif src == "db":
                connection = sqlite3.connect(DB_FILE)
                cursor = connection.cursor()
                cursor.execute("delete FROM products where product_id=?", product_id)
                table.delete(selected_item)
                connection.commit()
                connection.close()
                messagebox.showinfo("Success", "Product deleted successfully!")

    else:
        messagebox.showwarning("No Selection", "Please select a product to delete.")





def delete_selected_supplier(table,src):
    selected_item = table.selection()
    if selected_item:
        confirm = messagebox.askyesno("Delete", "Are you sure you want to delete the selected Supplier?")
        if confirm:
            item_values = table.item(selected_item, "values")
            supplier_id = item_values[0]
            if src == "xml":
                try:
                    tree = ET.parse(XML_FILE)
                    r = tree.getroot()
                    suppliers = r.find("Suppliers")
                    for supplier in suppliers.findall("Supplier"):
                        if supplier.get("supplier_id") == str(supplier_id):
                            suppliers.remove(supplier)
                            break

                    tree.write(XML_FILE, encoding="utf-8", xml_declaration=True)
                    table.delete(selected_item)
                    messagebox.showinfo("Success", "Supplier deleted successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete Supplier: {e}")
            elif src == "db":
                connection = sqlite3.connect(DB_FILE)
                cursor = connection.cursor()
                cursor.execute("delete FROM suppliers where supplier_id=?", supplier_id)
                table.delete(selected_item)
                connection.commit()
                connection.close()
                messagebox.showinfo("Success", "Supplier deleted successfully!")

    else:
        messagebox.showwarning("No Selection", "Please select a supplier to delete.")


def load_selected_for_update(table,src,c):
    selected_item = table.selection()
    if selected_item:
        item_values = table.item(selected_item, "values")
        clear_fields()
        name_entry.insert(0, item_values[1])
        email_entry.insert(0, item_values[2])
        phone_entry.insert(0, item_values[3])
        address_entry.insert(0, item_values[4])
        global combobox
        global add_label
        combobox.grid_forget()
        add_label.grid_forget()
        switch_to_info_frame()
        if c == "client" :
            save_button.config(command=lambda: update_client_info(table, selected_item,src))
        elif c == "supplier" :
            save_button.config(command=lambda: update_supplier_info(table, selected_item, src))

    else:
        messagebox.showwarning("No Selection", "Please select a client to update.")


def update_client_info(table, selected_item,src):
    updated_name = name_entry.get().strip()
    updated_email = email_entry.get().strip()
    updated_phone = phone_entry.get().strip()
    updated_address = address_entry.get().strip()
    client_id = table.item(selected_item, "values")[0]

    if updated_name and updated_email and updated_phone and updated_address:
        if src == "xml":
            try:
                tree = ET.parse(XML_FILE)
                r = tree.getroot()
                clients = r.find("Clients")

                for client in clients.findall("Client"):
                    if client.get("client_id") == str(client_id):
                        client.find("Full_Name").text = updated_name
                        client.find("Email").text = updated_email
                        client.find("Phone").text = updated_phone
                        client.find("Address").text = updated_address
                        break

                tree.write(XML_FILE, encoding="utf-8", xml_declaration=True)
                messagebox.showinfo("Success", "Client updated successfully!")


            except Exception as e:
                messagebox.showerror("Error", f"Failed to update client: {e}")
        elif src == "db":
            connection = sqlite3.connect(DB_FILE)
            cursor = connection.cursor()
            cursor.execute("""
                           UPDATE clients
                           SET Full_Name = ?, Email = ?, Phone = ?, Address = ?
                           WHERE client_id = ?
                       """, (updated_name, updated_email, updated_phone, updated_address, client_id))
            connection.commit()
            connection.close()

            messagebox.showinfo("Success", "Client information updated successfully!")
            clear_fields()
        show_clients(table, src)
        switch_to_clients_list_frame(src)
    else:
        messagebox.showwarning("Error", "All fields are required!")




def update_supplier_info(table, selected_item,src):
    updated_name = name_entry.get().strip()
    updated_email = email_entry.get().strip()
    updated_phone = phone_entry.get().strip()
    updated_address = address_entry.get().strip()
    supplier_id = table.item(selected_item, "values")[0]

    if updated_name and updated_email and updated_phone and updated_address:
        if src == "xml":
            try:
                tree = ET.parse(XML_FILE)
                r = tree.getroot()
                suppliers = r.find("Suppliers")

                for supplier in suppliers.findall("Supplier"):
                    if supplier.get("supplier_id") == str(supplier_id):
                        supplier.find("Full_Name").text = updated_name
                        supplier.find("Email").text = updated_email
                        supplier.find("Phone").text = updated_phone
                        supplier.find("Address").text = updated_address
                        break

                tree.write(XML_FILE, encoding="utf-8", xml_declaration=True)
                messagebox.showinfo("Success", "Supplier updated successfully!")


            except Exception as e:
                messagebox.showerror("Error", f"Failed to update Supplier: {e}")
        elif src == "db":
            connection = sqlite3.connect(DB_FILE)
            cursor = connection.cursor()
            cursor.execute("""
                           UPDATE suppliers
                           SET Full_Name = ?, Email = ?, Phone = ?, Address = ?
                           WHERE supplier_id = ?
                       """, (updated_name, updated_email, updated_phone, updated_address, supplier_id))
            connection.commit()
            connection.close()

            messagebox.showinfo("Success", "Supplier information updated successfully!")
            clear_fields()
        show_suppliers(table, src)
        switch_to_suppliers_list_frame(src)
    else:
        messagebox.showwarning("Error", "All fields are required!")


def clear_fields():
    name_entry.delete(0, END)
    email_entry.delete(0, END)
    phone_entry.delete(0, END)
    address_entry.delete(0, END)


root.title("Gestion Stock")
root.config(bg="#fffcd1")
root.geometry("800x500")
root.mainloop()
