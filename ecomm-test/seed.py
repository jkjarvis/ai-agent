import sqlite3

connection = sqlite3.connect('ecommerce.db')
cursor = connection.cursor()

# Insert sample order
cursor.execute('''
    INSERT INTO orders (customer_id, order_date, shipping_address, order_status, total_price)
    VALUES (1, '2024-03-09', '123 Main St, Anytown, AN', 'Processing', 59.99)
''')
order_id = cursor.lastrowid

# Insert sample order items for the above order
order_items = [
    (order_id, 101, 2, 19.99),
    (order_id, 102, 1, 20.00)
]
cursor.executemany('''
    INSERT INTO order_items (order_id, product_id, quantity, price_per_item)
    VALUES (?, ?, ?, ?)
''', order_items)

connection.commit()
connection.close()
