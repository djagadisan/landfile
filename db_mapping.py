from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base


class DBMapping():

    Base = declarative_base()

    class ErrorCodes(Base):
        __tablename__ = "error_codes"
        id = Column(Integer,primary_key=True)
        code = Column(String(5),nullable = False)
        error_name = Column(String(256),nullable = False)



    class ResultCode(Base):
        __tablename__ = "result_code"
        id = Column(Integer,primary_key=True)
        name = Column(String(2),nullable = False)
        result_name = Column(String(5),nullable = False)
        
     
    class TestResult(Base):
        __tablename__ = "test_result"
        id = Column(Integer,primary_key=True)
        test_id = Column(String(50),nullable = False)
        test_date = Column(DateTime,nullable = False)
        test_cell = Column(String(50),nullable = False )
        vm_boot = Column(Float(Precision=2),nullable = False )
        vm_boot_status = Column(Integer,nullable = False)
        snap = Column(Float(Precision=2),nullable = False )
        snap_status = Column(Integer,nullable = False)
        all_run = Column(Float(Precision=2),nullable = False )
        all_status = Column(Integer,nullable = False)
    
    
                
