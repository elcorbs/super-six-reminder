import sqlite3 
import os
import psycopg2

class UserModel:
    def __init__(self):
        DATABASE_URL = os.environ['DATABASE_URL']
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cursor = self.conn.cursor()    
    def entered_this_round(self, userId):
        get_user_query = """
        SELECT * FROM users WHERE UserID = %s;
        """
    
        self.cursor.execute(get_user_query, (userId,))
        row_count = self.cursor.rowcount
        self.cursor.close
        if (row_count == 0):
          query = """
          INSERT INTO users (UserId, EnteredThisRound) VALUES (%s, TRUE);
          """
        else:
          query = """
          UPDATE users SET EnteredThisRound = TRUE WHERE UserId = %s;
          """  
        self.cursor.execute(query, (userId,))
        self.conn.commit()
        self.cursor.close
        self.conn.close

    def users_still_outstanding(self):
        outstanding = self.get_row_count("""
        SELECT * FROM users WHERE EnteredThisRound = FALSE;
        """)
        total = self.get_row_count("""
        SELECT * FROM users;
        """)
        return total < 2 | outstanding > 0 

    def start_new_round(self):
        query = """
        UPDATE users SET EnteredThisRound = FALSE;
        """
        self.cursor.execute(query)
        self.conn.commit()
        self.cursor.close
        self.conn.close
    
    def get_row_count(self, query):
        self.cursor.execute(query)
        total = self.cursor.rowcount
        self.cursor.close()
        return total