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
        SELECT * FROM "users" WHERE UserID = %s;
        """
        print(userId)
        self.cursor.execute(get_user_query, ("{userId}",))
        if (self.cursor.rowcount == 0):
          query = """
          INSERT INTO users (UserId, EnteredThisRound) VALUES (%s, TRUE);
          """
        else:
          query = """
          UPDATE users SET EnteredThisRound = TRUE WHERE UserId = %s;
          """  
        self.cursor.execute(query, (userId,))
        self.conn.commit()

    def users_still_outstanding(self):
        query = """
        SELECT * FROM users WHERE EnteredThisRound = FALSE;
        """
        outstanding = self.cursor.execute(query)
        return outstanding.rowcount > 0 

    def start_new_round(self):
        query = """
        UPDATE users SET EnteredThisRound = FALSE;
        """
        self.cursor.execute(query)
        self.conn.commit()