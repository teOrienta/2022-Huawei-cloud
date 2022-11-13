from database.controllers import EventlogRepository
from database.config import db_conn, verify_connection
from datetime import datetime

class PostgreSQL:
    def __init__(self):
        self.connection = db_conn
        self.engine = None
        self.__migration()

    def __migration(self):
        self.is_connected = False
        try:
            self.engine = self.connection.get_engine()

            EventlogRepository.create(self.engine)

            self.is_connected = True
        except Exception as e:
            print("DATABASE NOT CONNECTED:", e)
        return self.is_connected

    @verify_connection
    def call_function_with_session(self, func, *args, **kwargs):
        """ Abstract function to call a function with a session """
        with self.connection.get_session() as session:
            return func(session, *args, **kwargs)

    # Eventlog functions
    def get_event_logs(self, case_id: str = None, activity: str = None, resource: str = None,
                    start_date: datetime = None, end_date: datetime = None, analysis: str = None):
        
        if start_date is None:
            start_date = datetime(1970, 1, 1)
        if end_date is None:
            end_date = datetime.today()

        function = EventlogRepository.select
        logs = self.call_function_with_session(
            function, case_id, activity, resource,
            start_date, end_date, analysis
        )

        return logs

    
