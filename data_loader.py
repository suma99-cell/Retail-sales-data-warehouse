from models import Customer, Product, Date, Sales
from db_connection import DBConnection



def load_customers(db):
    rows = db.execute_query("SELECT * FROM dim_customer")
    customers = {}
    for r in rows:
        customers[r[0]] = Customer(*r)
    return customers



def load_products(db):
    rows = db.execute_query("SELECT * FROM dim_product")
    products = {}
    for r in rows:
        products[r[0]] = Product(*r)
    return products



def load_dates(db):
    rows = db.execute_query("SELECT * FROM dim_date")
    dates = {}
    for r in rows:
        dates[r[0]] = Date(*r)
    return dates



def load_sales(db, customers, products, dates):
    rows = db.execute_query("SELECT * FROM fact_sales")
    sales_list = []

    for r in rows:
        sale = Sales(
            r[0],              # sale_id
            customers[r[1]],  # customer object
            products[r[2]],   # product object
            dates[r[3]],      # date object
            r[4],             # quantity
            r[5],             # sales amount
            r[6]              # discount
        )
        sales_list.append(sale)

    return sales_list



def load_data():
    db = DBConnection()

    # Load all dimension data
    customers = load_customers(db)
    products = load_products(db)
    dates = load_dates(db)

    # Load fact data
    sales = load_sales(db, customers, products, dates)

    db.close()

    return {
        "customers": customers,
        "products": products,
        "dates": dates,
        "sales": sales
    }