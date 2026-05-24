from db_connection import DBConnection
from data_loader import load_customers, load_products, load_dates, load_sales
from reports import ReportGenerator


def main():
    print("=== Retail Data Warehouse OOP Project ===")

    # ✅ Step 1: Connect Database
    db = DBConnection()

    print("Connected to PostgreSQL ✅")

    # ✅ Step 2: Load Data
    customers = load_customers(db)
    products = load_products(db)
    dates = load_dates(db)
    sales = load_sales(db, customers, products, dates)

    print("Data Loaded ✅")

    # ✅ Step 3: Create Data Warehouse Object
    data_warehouse = {
        "customers": customers,
        "products": products,
        "dates": dates,
        "sales": sales
    }

    # ✅ Step 4: Generate Reports
    report = ReportGenerator(data_warehouse)

    print("\n=== REPORTS ===")
    print("Total Sales:", report.total_sales())
    print("Sales by Category:", report.sales_by_category())
    print("Sales by Year:", report.sales_by_year())



    # ✅ Step 5: Close Connection
    db.close()
    print("\nDatabase connection closed ✅")


# ✅ Run the program
if __name__ == "__main__":
    main()