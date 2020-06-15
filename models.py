import sqlite3 
import os
import psycopg2

class UserModel:
    def __init__(self):
        DATABASE_URL = os.environ['DATABASE_URL']
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    
    def entered_this_round(self, userId):
        get_user_query = """
        SELECT * FROM Users WHERE UserID = {userId};
        """
        user = self.conn.execute(get_user_query)
        if (user.rowcount == 0):
          query = """
          INSERT INTO Users (UserId, EnteredThisRound) VALUES ({userId}, 1);
          """
        else:
          query = """
          UPDATE Users SET EnteredThisRound = 1 WHERE UserId = {userId};
          """  
        self.conn.execute(query)

    def users_still_outstanding(self):
        query = """
        SELECT COUNT(*) FROM Users WHERE EnteredThisRound = 0;
        """
        outstanding = self.conn.execute(query)
        return outstanding != 2

    def start_new_round(self):
        query = """
        UPDATE Users SET EnteredThisRound = 0;
        """
        self.conn.execute(query)