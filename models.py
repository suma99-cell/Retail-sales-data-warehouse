# ✅ Base Dimension Class
class Dimension:
    def __init__(self, key):
        self.key = int(key)   # ✅ FIX → always integer


# ✅ CUSTOMER DIMENSION
class Customer(Dimension):
    def __init__(self, key, name, gender, city, state, country, customer_type):
        super().__init__(key)
        self.name = name
        self.gender = gender
        self.city = city
        self.state = state
        self.country = country
        self.customer_type = customer_type


# ✅ PRODUCT DIMENSION
class Product(Dimension):
    def __init__(self, key, name, category, brand, price):
        super().__init__(key)
        self.name = name
        self.category = category
        self.brand = brand
        self.price = float(price)   # ✅ FIX


# ✅ DATE DIMENSION
class Date(Dimension):
    def __init__(self, key, full_date, day, month, quarter, year):
        super().__init__(key)
        self.full_date = full_date
        self.day = int(day)
        self.month = int(month)
        self.quarter = int(quarter)
        self.year = int(year)


# ✅ FACT TABLE (SALES)
class Sales:
    def __init__(self, sale_id, customer, product, date, quantity, sales_amount, discount):
        self.sale_id = int(sale_id)   # ✅ FIX

        # ✅ Relationships
        self.customer = customer
        self.product = product
        self.date = date

        # ✅ Measures
        self.quantity = int(quantity)
        self.sales_amount = float(sales_amount)
        self.discount = float(discount)

    # ✅ Derived Measure
    def net_amount(self):
        return self.sales_amount - self.discount
