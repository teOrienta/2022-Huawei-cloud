from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from sqlalchemy import create_engine

class DBConnectionHandler:
    """SQLAlchemy database connection"""

    def __init__(self, connection: str, connection_pool_size: int):        
        self.__connection_string = connection
        self.engine = create_engine(self.__connection_string,
                                    poolclass=QueuePool,
                                    max_overflow=0,
                                    pool_size=connection_pool_size,
                                    pool_pre_ping=True,
                                    pool_use_lifo=True)
        self.session_maker = sessionmaker(self.engine)
        self.session_maker_without_flush = sessionmaker(self.engine, autoflush=False)
        
    def get_conn(self):
        """ Returns a connection instance """
        return self.engine.connect()

    def get_engine(self):
        """Return connection Engine
            :return - engine connection to database
        """
        return self.engine
    
    def get_session(self):
        return self.session_maker()
    
    def get_session_without_flush(self):
        return self.session_maker_without_flush()

    def get_raw_connection(self):
        """Return connection Cursor
            :return - cursor of the database
        """
        return self.engine.raw_connection()