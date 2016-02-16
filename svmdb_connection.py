from sqlalchemy import engine, create_engine


class DBConnection():

    def _createConn(self):
        engine = create_engine('sqlite:///vm_data.db', echo=True)
        return engine

