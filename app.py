from flask import Flask, jsonify, render_template, request
from data_loader import load_data
from db_connection import DBConnection

app = Flask(__name__)



@app.route('/')
def home():
    return render_template('index.html')



@app.route('/total_sales')
def total_sales():
    dw = load_data()
    total = sum(s.net_amount() for s in dw["sales"])
    return jsonify({"total_sales": total})


@app.route('/sales_by_customer')
def sales_by_customer():
    dw = load_data()
    result = {}

    for s in dw["sales"]:
        name = s.customer.name
        result[name] = result.get(name, 0) + s.net_amount()

    return jsonify(result)



@app.route('/sales_details')
def sales_details():
    dw = load_data()

    data = []
    for s in dw["sales"]:
        data.append({
            "customer": s.customer.name,
            "product": s.product.name,
            "date": str(s.date.full_date),
            "amount": s.net_amount()
        })

    return jsonify(data)



@app.route('/dim_customer')
def dim_customer():
    dw = load_data()
    return jsonify([{
        "customer_key": c.key,
        "customer_name": c.name,
        "gender": c.gender,
        "city": c.city,
        "state": c.state,
        "country": c.country,
        "customer_type": c.customer_type
    } for c in dw["customers"].values()])


@app.route('/dim_product')
def dim_product():
    dw = load_data()
    return jsonify([{
        "product_key": p.key,
        "product_name": p.name,
        "category": p.category,
        "brand": p.brand,
        "unit_price": p.price
    } for p in dw["products"].values()])


@app.route('/dim_date')
def dim_date():
    dw = load_data()
    return jsonify([{
        "date_key": d.key,
        "full_date": str(d.full_date).split(" ")[0],
        "day": d.day,
        "month": d.month,
        "quarter": d.quarter,
        "year": d.year
    } for d in dw["dates"].values()])


@app.route('/fact_sales')
def fact_sales():
    dw = load_data()
    return jsonify([{
        "sale_id": s.sale_id,
        "customer_key": s.customer.key,
        "product_key": s.product.key,
        "date_key": s.date.key,
        "quantity_sold": s.quantity,
        "sales_amount": s.net_amount(),
        "discount_amount": s.discount
    } for s in dw["sales"]])




@app.route('/add_sale', methods=['POST'])
def add_sale():
    print("🔥 API HIT: ADD SALE")   
    db = DBConnection()
    data = request.get_json(silent=True) or request.form.to_dict()

    print("DATA RECEIVED:", data)

    if not data:
        return jsonify({"error": "No data received"}), 400

    query = """
    INSERT INTO fact_sales 
    (customer_key, product_key, date_key, quantity_sold, sales_amount, discount_amount)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (
        data['customer_key'],
        data['product_key'],
        data['date_key'],
        data['quantity_sold'],
        data['sales_amount'],
        data['discount_amount']
    )

    db.execute_update(query, values)
    db.close()

    return jsonify({"message": "Sale Added"})



@app.route('/get_sale/<int:sale_id>')
def get_sale(sale_id):
    db = DBConnection()

    result = db.execute_query(
        "SELECT * FROM fact_sales WHERE sale_id=%s",
        (sale_id,)
    )

    db.close()

    if not result:
        return jsonify({"error": "Sale not found"}), 404

    row = result[0]
    return jsonify({
        "sale_id": row[0],
        "customer_key": row[1],
        "product_key": row[2],
        "date_key": row[3],
        "quantity_sold": row[4],
        "sales_amount": row[5],
        "discount_amount": row[6]
    })



@app.route('/update_sale/<int:sale_id>', methods=['PUT'])
def update_sale(sale_id):
    db = DBConnection()
    data = request.get_json(silent=True) or request.form.to_dict()

    print("UPDATE DATA:", data)

    if not data:
        return jsonify({"error": "No data received"}), 400

    query = """
    UPDATE fact_sales
    SET customer_key=%s, product_key=%s, date_key=%s,
        quantity_sold=%s, sales_amount=%s, discount_amount=%s
    WHERE sale_id=%s
    """

    values = (
        data['customer_key'],
        data['product_key'],
        data['date_key'],
        data['quantity_sold'],
        data['sales_amount'],
        data['discount_amount'],
        sale_id
    )

    db.execute_update(query, values)
    db.close()

    return jsonify({"message": "Sale Updated"})



@app.route('/update_quantity/<int:sale_id>', methods=['PUT'])
def update_quantity(sale_id):
    db = DBConnection()
    data = request.get_json(silent=True) or request.form.to_dict()

    if not data:
        return jsonify({"error": "No data received"}), 400

    db.execute_update(
        "UPDATE fact_sales SET quantity_sold=%s WHERE sale_id=%s",
        (data['quantity_sold'], sale_id)
    )

    db.close()

    return jsonify({"message": "Quantity Updated"})


@app.route('/delete_sale/<int:sale_id>', methods=['DELETE'])
def delete_sale(sale_id):
    db = DBConnection()

    db.execute_update(
        "DELETE FROM fact_sales WHERE sale_id=%s",
        (sale_id,)
    )

    db.close()

    return jsonify({"message": "Sale Deleted"})



if __name__ == "__main__":
    app.run(debug=True)