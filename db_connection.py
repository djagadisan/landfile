from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
import sqlalchemy

class DBConnection():
    
    def _createConn(self):
        
        DB_URI = "mysql+mysqlconnector://{user}:{password}@{host}:{port}/{db}"
        self.db = create_engine(DB_URI.format(
                    user = 'root',
                    password = '1aa5.m',
                    host = '127.0.0.1',
                    port = '3306',
                    db = 'perf_test_nectar')
                    )
        return self.db

