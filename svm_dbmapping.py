from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


class DBMapping():

    Base = declarative_base()

    class ErrorCodes(Base):
        __tablename__ = "vm"
        id = Column(Integer, primary_key=True)
        host = Column(String(5), nullable=False)
        vm_id = Column(String(256), nullable=False)
        vm_state = Column(String(256), nullable=False)
