import sqlite3

connection = sqlite3.connect('ecommerce.db')
cursor = connection.cursor()

# Create orders table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        order_date TEXT NOT NULL,
        shipping_address TEXT NOT NULL,
        order_status TEXT NOT NULL,
        total_price REAL NOT NULL
    )
''')

# Create order_items table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS order_items (
        order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        price_per_item REAL NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders (order_id)
    )
''')

connection.commit()
connection.close()
