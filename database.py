import sqlite3

class Database:
    
    def __init__(self,db):

        self.connect = sqlite3.connect(db)
        self.cur = self.connect.cursor()
        self.create_country_info()
        self.create_total_info()
    
    def create_country_info(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS country_info (name TEXT PRIMARY KEY, total_cases INTEGER, total_deaths INTEGER)")
        self.connect.commit()
    
    def create_total_info(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS total_info (name TEXT PRIMARY KEY, total_value INTEGER)")
        self.connect.commit()
    
    def insert_country_info(self, name, total_cases, total_death):
        self.cur.execute("INSERT INTO country_info VALUES(?,?,?)",(name, total_cases, total_death))
        self.connect.commit()

    def insert_total_info(self, name, total_value):
        self.cur.execute("INSERT INTO total_info VALUES(?,?)", (name, total_value))
        self.connect.commit()
    
    def update_country_info(self, name,total_cases, total_death):
        self.cur.execute("UPDATE country_info SET total_cases = ?, total_deaths = ? WHERE name = ?", (total_cases, total_death, name))
        self.connect.commit()
        
    def update_total_info(self, name, total_value):
        self.cur.execute("UPDATE total_info SET total_value = ? WHERE name = ?", (total_value, name))
        self.connect.commit()

    def fetch_country_info(self):

        self.cur.execute("SELECT * FROM country_info")
        rows = self.cur.fetchall()
        return rows

    def fetch_total_info(self):
        self.cur.execute("SELECT * FROM total_info")
        rows = self.cur.fetchall()
        return rows