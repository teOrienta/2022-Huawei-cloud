from sqlalchemy import Column, Integer, DateTime, String
from database.config import Base, classproperty
from collections import namedtuple

class Eventlog(Base):
    """ Eventlog Entity """

    __table_args__  = { 'extend_existing': True } 
    __tablename__   = f"Eventlog"
    id              = Column(Integer, primary_key=True)
    caseId          = Column(String, nullable=False)
    activity        = Column(String, nullable=False)
    resource        = Column(String, nullable=True)
    startTimestamp  = Column(DateTime, nullable=True)
    endTimestamp    = Column(DateTime, nullable=False)
    analysis        = Column(String, nullable=False)

    @classproperty
    def table_name(cls):
        return cls.__tablename__

    def __repr__(self):
        return f"""Eventlog(
            id = {self.id}
            caseId = {self.caseId}
            activity = {self.activity}
            resource = {self.resource}
            startTimestamp = {self.startTimestamp}
            endTimestamp = {self.endTimestamp}
            analysis = {self.analysis}
        )"""

    def __eq__(self, other):
        return self.id == other.id

    def __iter__(self):
        yield self.id
        yield self.caseId
        yield self.activity
        yield self.resource
        yield self.startTimestamp
        yield self.endTimestamp
        yield self.analysis

EventlogModel = namedtuple("Eventlog", [
    "id", "caseId", "activity", "resource",
    "startTimestamp", "endTimestamp", "analysis"
])