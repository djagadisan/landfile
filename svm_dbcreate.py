from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
import sqlalchemy
from svm_dbmapping import DBMapping
from svmdb_connection import DBConnection


db_data = DBMapping()
engine = DBConnection()._createConn()
engine.echo = True
