# queries.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create_database import VM
 
engine = create_engine('sqlite:///vm_backup.db', echo=False)
 
# create a Session
Session = sessionmaker(bind=engine)
session = Session()

# how to do a SELECT * (i.e. all)
res = session.query(VM).all()
for vm in res:
    print vm.id, vm.uuid_vm, vm.host, vm.vm_state, vm.update_state 