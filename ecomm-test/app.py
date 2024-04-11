from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_order_with_items(order_id):
    connection = sqlite3.connect('ecommerce.db')
    cursor = connection.cursor()
    
    # Fetch order details
    cursor.execute('''
        SELECT order_id, customer_id, order_date, shipping_address, order_status, total_price
        FROM orders WHERE order_id=?
    ''', (order_id,))
    order = cursor.fetchone()
    
    if order:
        # Fetch items for the order
        cursor.execute('''
            SELECT order_item_id, product_id, quantity, price_per_item
            FROM order_items WHERE order_id=?
        ''', (order_id,))
        items = cursor.fetchall()
        
        order_details = {
            'order_id': order[0],
            'customer_id': order[1],
            'order_date': order[2],
            'shipping_address': order[3],
            'order_status': order[4],
            'total_price': order[5],
            'items': [{
                'order_item_id': item[0],
                'product_id': item[1],
                'quantity': item[2],
                'price_per_item': item[3]
            } for item in items]
        }
    else:
        order_details = None

    connection.close()
    return order_details

@app.route('/get_order', methods=['GET'])
def api_get_order():
    order_id = request.args.get('order_id')
    if order_id:
        try:
            order_id = int(order_id)
        except ValueError:
            return jsonify({'error': 'Invalid order_id format. Please use a numeric value.'}), 400

        order_details = get_order_with_items(order_id)
        if order_details:
            return jsonify(order_details)
        else:
            return jsonify({'error': 'Order not found'}), 404
    else:
        return jsonify({'error': 'Missing order_id argument'}), 400

if __name__ == '__main__':
    app.run(debug=True)
