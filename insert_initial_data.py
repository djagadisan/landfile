from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_connection import DBConnection
import sqlalchemy
from db_mapping import DBMapping



engine = DBConnection()._createConn()
engine.echo = True
DBMapping().Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

session.add_all([
                 DBMapping().ErrorCodes(code="FPCT",error_name="Fail Pre Check Test"),
                 DBMapping().ErrorCodes(code="FKP",error_name="Fail to create key pair"),
                 DBMapping().ErrorCodes(code="FSG",error_name="Fail to create security group"),
                 DBMapping().ErrorCodes(code="FRI",error_name="Fail to run instances"),
                 DBMapping().ErrorCodes(code="FRB",error_name="Fail to reboot instances"),
                 DBMapping().ErrorCodes(code="FRTS",error_name="Fail to reboot process"),
                 DBMapping().ErrorCodes(code="FFT",error_name="Fail to file test"),
                 DBMapping().ErrorCodes(code="FIPN",error_name="Fail instances port Not ready"),
                 DBMapping().ErrorCodes(code="FISB",error_name="Fail instances stuck in build process"),
                 DBMapping().ErrorCodes(code="FURS",error_name="Fail unable to remove snapshot")
                 ])
session.commit()
