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
        SELECT * FROM Users WHERE UserID = {userId};
        """
        user = self.cursor.execute(get_user_query)
        if (user.rowcount == 0):
          query = """
          INSERT INTO Users (UserId, EnteredThisRound) VALUES ({userId}, TRUE);
          """
        else:
          query = """
          UPDATE Users SET EnteredThisRound = TRUE WHERE UserId = {userId};
          """  
        self.cursor.execute(query)

    def users_still_outstanding(self):
        query = """
        SELECT COUNT(*) FROM Users WHERE EnteredThisRound = FALSE;
        """
        outstanding = self.cursor.execute(query)
        return outstanding > 0 

    def start_new_round(self):
        query = """
        UPDATE Users SET EnteredThisRound = FALSE;
        """
        self.cursor.execute(query)