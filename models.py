import sqlite3 

class Schema:
    def __init__(self):
        print("init schema")
        self.conn = sqlite3.connect('users.db')
        self.create_user_table()

    def create_user_table(self):
        print("creating user table")
        query = """
        CREATE TABLE IF NOT EXISTS "Users" (
          id INTEGER PRIMARY KEY,
          UserId TEXT,
          ReceiveAlerts integer,
          EnteredThisRound integer,
        );
        """

        self.conn.execute(query)

class UserModel:
    def __init__(self):
        self.conn = sqlite3.connect('users.db')
    
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