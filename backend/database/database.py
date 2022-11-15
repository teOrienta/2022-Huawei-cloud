from database.config import db_conn, verify_connection
from database.controllers import EventlogRepository
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
    def select_log_events(self, case_id: str = None, activity: str = None,
                        resource: str = None, start_date: datetime = None,
                        end_date: datetime = None, analysis: str = None):
        
        if start_date is None:
            start_date = datetime(1970, 1, 1)
        if end_date is None:
            end_date = datetime.today()

        function = EventlogRepository.select
        logs = self.call_function_with_session(
            function, start_date, end_date,
            case_id, activity, resource, analysis
        )

        return list(map(lambda x: x._asdict(), logs))
    
    def select_analysis(self):
        function = EventlogRepository.select_analysis
        return self.call_function_with_session(function)

    def insert_many_log_events(self, events_list: list[dict]):
        function = EventlogRepository.insert_many
        return self.call_function_with_session(function, events_list)

    def insert_log_event(self, analysis: str, case_id: str, activity: str, resource: str,
                         start_timestamp: datetime, end_timestamp: datetime):
        function = EventlogRepository.insert
        return self.call_function_with_session(
            function, case_id, activity, resource,
            start_timestamp, end_timestamp, analysis
        )
