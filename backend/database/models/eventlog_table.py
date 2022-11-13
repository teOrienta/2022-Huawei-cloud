from sqlalchemy import Column, Integer, DateTime, String, Boolean
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
    csvFlag         = Column(Boolean, nullable=False, default=True)

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
            csvFlag = {self.csvFlag}
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
        yield self.csvFlag

EventlogModel = namedtuple("Eventlog", [
    "id", "caseId", "activity", "resource",
    "startTimestamp", "endTimestamp", "csvFlag"
])