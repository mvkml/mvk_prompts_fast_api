#WILL IMPLEMENT BASE REPOSITORY CODE
from sqlalchemy import null
from sqlalchemy.orm import Session
from dal.connections import sql_connection

class SQLBaseRepository:
    def __init__(self):
        self.db = self.get_sql_session()

    def get_sql_session(self):
        if self.db == null:
            self.db =  sql_connection.get_db()
        return self.db