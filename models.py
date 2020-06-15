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
    
    def register_user(self, userId):
        query = """
        INSERT INTO Users (UserId, ReceiveAlerts VALUE ({userId}, 1);
        """
        self.conn.execute(query)
    def entered_this_round(self, userId):
        query = """
        UPDATE Users SET EnteredThisRound = 1 WHERE UserId = {userId};
        """  
        self.conn.execute(query)
    def start_new_round(self):
        query = """
        UPDATE Users SET EnteredThisRound = 0;
        """
        self.conn.execute(query)