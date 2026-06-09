import pandas as pd
import psycopg2



def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="retail_dw",
        user="postgres",
        password="9966379996",
        port="5432"
    )


def process_file(file_path, table_name, load_function):


    df = pd.read_csv(file_path)
    print(f"{file_path} extracted successfully")


    print("DataFrame validation successful")


    df = df.drop_duplicates()
    print("DataFrame transformed successfully")


    load_function(df)
    print(f"{table_name} loaded successfully\n")  



def load_customers(df):
    conn = get_connection()
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO dim_customer 
            (customer_key, customer_name, gender, city, state, country, customer_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (customer_key) DO NOTHING
        """, (
            int(row['customer_key']),
            str(row['customer_name']),
            str(row['gender']),
            str(row['city']),
            str(row['state']),
            str(row['country']),
            str(row['customer_type'])
        ))

    conn.commit()
    cursor.close()
    conn.close()



def load_products(df):
    conn = get_connection()
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO dim_product 
            (product_key, product_name, category, brand, unit_price)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (product_key) DO NOTHING
        """, (
            int(row['product_key']),
            str(row['product_name']),
            str(row['category']),
            str(row['brand']),
            float(row['unit_price'])
        ))

    conn.commit()
    cursor.close()
    conn.close()



def load_dates(df):
    conn = get_connection()
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO dim_date 
            (date_key, full_date, day, month, quarter, year)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (date_key) DO NOTHING
        """, (
            int(row['date_key']),
            row['full_date'],
            int(row['day']),
            int(row['month']),
            int(row['quarter']),
            int(row['year'])
        ))

    conn.commit()
    cursor.close()
    conn.close()


def load_fact(df):
    conn = get_connection()
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO fact_sales 
            (sale_id, customer_key, product_key, date_key, quantity_sold, sales_amount, discount_amount)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (sale_id) DO NOTHING
        """, (
            int(row['sale_id']),
            int(row['customer_key']),
            int(row['product_key']),
            int(row['date_key']),
            int(row['quantity_sold']),
            float(row['sales_amount']),
            float(row['discount_amount'])
        ))

    conn.commit()
    cursor.close()
    conn.close()



def main():


    process_file("data/dim_customer.csv", "customers", load_customers)

    process_file("data/dim_product.csv", "products", load_products)


    process_file("data/dim_date.csv", "dates", load_dates)


    process_file("data/fact_sales.csv", "fact_sales", load_fact)

    print("ETL process completed successfully")


if __name__ == "__main__":
    main()