from database.models import Eventlog, EventlogModel
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from datetime import datetime

class EventlogRepository():
    """ Class to manage Eventlog Repository """
    
    @staticmethod
    def create(engine: Engine) -> Eventlog:
        """ Creates Eventlog table if not exists. """
        insp = inspect(engine)
        if not insp.has_table(Eventlog.table_name, schema=None):
            Eventlog.__table__.create(engine)
        return Eventlog
    
    @staticmethod
    def insert(session: Session, case_id: str, activity: str, resource: str,
            start_timestamp: datetime, end_timestamp: datetime, analysis: str) -> EventlogModel:
        """ Inserts a row (New Event) in Eventlog table. """
        new_event = Eventlog(
            caseId = case_id,
            activity = activity,
            resource = resource,
            startTimestamp = start_timestamp,
            endTimestamp = end_timestamp,
            analysis = analysis
        )
        session.add(new_event)
        session.commit()

        return EventlogModel._make(new_event)

    @staticmethod
    def insert_many(session: Session, events_list: list[dict]) -> list[Eventlog]:
        """ Inserts many rows (New Events) into Eventlog table. """

        events_list = list(map(lambda dic: Eventlog(**dic), events_list))

        for event in events_list:
            session.merge(event)
        session.commit()

        return events_list
    
    @staticmethod
    def count(session: Session):
        """ Return the count of the Eventlog table. """
        return session.query(Eventlog.id).count()

    @staticmethod
    def select(session: Session, start_date, end_date,
                case_id: str = None, activity: str = None,
                resource: str = None, analysis: str = None) -> list[EventlogModel]:
        """ 
        Selects Eventlog table by:
            - caseId
            - activity
            - resource
            - startTimestamp
            - endTimestamp
            - analysis
        """

        filters = {}
        if case_id is not None:
            filters["caseId"] = case_id
        if activity is not None:
            filters["activity"] = activity
        if resource is not None:
            filters["resource"] = resource
        if analysis is not None:
            filters["analysis"] = analysis

        logs = (
            session.query(Eventlog)
            .filter_by(**filters)
            .filter(
                Eventlog.startTimestamp >= start_date,
                Eventlog.endTimestamp <= end_date
            )
            .all()
        )
        
        return list(map(EventlogModel._make, logs))
    
    @staticmethod
    def select_analysis(session: Session) -> list[str]:
        """ Selects the eventlog analysis names. """
        analysis = session.query(Eventlog.analysis).distinct().all()
        return [x[0] for x in list(analysis)]

    @staticmethod
    def select_all(session: Session) -> list[EventlogModel]:
        """ Returns all the rows in Eventlog table. """
        logs = session.query(Eventlog).all()
        return list(map(EventlogModel._make, logs))

    @staticmethod
    def drop(engine: Engine):
        """ Drop Eventlog table if exists """
        insp = inspect(engine)
        if insp.has_table(Eventlog.table_name, schema=None):
            Eventlog.__table__.drop(engine)
        return Eventlog