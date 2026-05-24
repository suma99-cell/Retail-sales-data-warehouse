import psycopg2
 
 
class DBConnection:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="retail_dw",  
            user="postgres",            
            password="9966379996",
            port="5432"      
        )
 
    # ✅ READ (SELECT)
    def execute_query(self, query, params=None):
        cursor = self.conn.cursor()
 
        try:
            if params:
                cursor.execute(query, params)   # ✅ parameterized query
            else:
                cursor.execute(query)
 
            result = cursor.fetchall()
            return result
 
        except Exception as e:
            print("Query Error:", e)
            return []
 
        finally:
            cursor.close()
 
 
    # ✅ CREATE / UPDATE / DELETE
    def execute_update(self, query, params=None):
        cursor = self.conn.cursor()
 
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
 
            self.conn.commit()
 
        except Exception as e:
            print("Update Error:", e)
            self.conn.rollback()
 
        finally:
            cursor.close()
 
 
    # ✅ CLOSE CONNECTION
    def close(self):
        if self.conn:
            self.conn.close()
 
 