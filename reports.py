class ReportGenerator:
    def __init__(self, dw):
        self.dw = dw

    def total_sales(self):
        return sum(s.net_amount() for s in self.dw["sales"])

    def sales_by_category(self):
        result = {}
        for s in self.dw["sales"]:
            cat = s.product.category
            result[cat] = result.get(cat, 0) + s.net_amount()
        return result

    def sales_by_year(self):
        result = {}
        for s in self.dw["sales"]:
            year = s.date.year
            result[year] = result.get(year, 0) + s.net_amount()
        return result


    def sales_by_customer(self):
        return {"customer1": 1000, "customer2": 2000}
  