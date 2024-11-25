import sqlite3

DB_FILE = "data.db"

def setup_database():
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            client_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Full_Name TEXT NOT NULL,
            Email TEXT NOT NULL,
            Phone TEXT NOT NULL,
            Address TEXT NOT NULL
        )
    """)
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS suppliers (
                supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
                Full_Name TEXT NOT NULL,
                Email TEXT NOT NULL,
                Phone TEXT NOT NULL,
                Address TEXT NOT NULL
            )
        """)
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                Price REAL NOT NULL,
                Category TEXT NOT NULL,
                Quantity INTEGER NOT NULL,
                supplier_id INTEGER NOT NULL,
                FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
                    ON DELETE CASCADE
            )
        """)


    cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                Total_Amount REAL NOT NULL,
                Quantity INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                client_id INTEGER NOT NULL,
                FOREIGN KEY (product_id) REFERENCES products(product_id)
                    ON DELETE CASCADE,
                FOREIGN KEY (client_id) REFERENCES clients(client_id)
                    ON DELETE CASCADE
            )
        """)


    connection.commit()
    connection.close()

setup_database()