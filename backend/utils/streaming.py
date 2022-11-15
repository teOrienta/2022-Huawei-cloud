from pm4py.util.xes_constants import (DEFAULT_NAME_KEY, DEFAULT_START_TIMESTAMP_KEY,
                                      DEFAULT_TIMESTAMP_KEY, DEFAULT_RESOURCE_KEY)
from pm4py.streaming.algo.discovery.dfg.algorithm import apply as StreamingDFG
from pm4py.streaming.stream.live_event_stream import LiveEventStream
from pm4py.streaming.algo.interface import StreamingAlgorithm
from pm4py.objects.log.obj import EventLog, Trace
from dateutil.parser import parser as date_parser
from pm4py.util import exec_utils, constants
import logging, datetime
from enum import Enum


class Parameters(Enum):
    CASE_ID_KEY = constants.PARAMETER_CONSTANT_CASEID_KEY
    RESOURCE_KEY = constants.PARAMETER_CONSTANT_RESOURCE_KEY
    ACTIVITY_KEY = constants.PARAMETER_CONSTANT_ACTIVITY_KEY
    TIMESTAMP_KEY = constants.PARAMETER_CONSTANT_TIMESTAMP_KEY
    START_TIMESTAMP_KEY = constants.PARAMETER_CONSTANT_START_TIMESTAMP_KEY


class StreamingEventlog(StreamingAlgorithm):
    def __init__(self, parameters=None):
        """
        Initialize the StreamingEventlog object

        Parameters
        ---------------
        parameters of the algorithm, including:
         - Parameters.ACTIVITY_KEY: the key of the event to use as activity
         - Parameters.CASE_ID_KEY: the key of the event to use as case identifier
         - Parameters.RESOURCE_KEY: the key of the event to use as resource
         - Parameters.TIMESTAMP_KEY: the key of the event to use as timestamp
         - Parameters.START_TIMESTAMP_KEY: the key of the event to use as start timestamp
        """
        if parameters is None:
            parameters = {}

        self.parameters = parameters
        self.case_id_key = exec_utils.get_param_value(
            Parameters.CASE_ID_KEY, parameters, constants.CASE_CONCEPT_NAME)
        self.activity_key = exec_utils.get_param_value(
            Parameters.ACTIVITY_KEY, parameters, DEFAULT_NAME_KEY)
        self.resource_key = exec_utils.get_param_value(
            Parameters.RESOURCE_KEY, parameters, DEFAULT_RESOURCE_KEY)
        self.timestamp_key = exec_utils.get_param_value(
            Parameters.TIMESTAMP_KEY, parameters, DEFAULT_TIMESTAMP_KEY)
        self.start_timestamp_key = exec_utils.get_param_value(
            Parameters.START_TIMESTAMP_KEY, parameters, DEFAULT_START_TIMESTAMP_KEY)
        
        self.eventlog = EventLog(attributes = {
            Parameters.ACTIVITY_KEY: self.activity_key,
            Parameters.CASE_ID_KEY: self.case_id_key,
            Parameters.RESOURCE_KEY: self.resource_key,
            Parameters.TIMESTAMP_KEY: self.timestamp_key,
            Parameters.START_TIMESTAMP_KEY: self.start_timestamp_key
        })
        self.event_amount = 0
        self.case_amount = 0
        self.first_date = datetime.datetime.now()
        self.last_date = datetime.datetime.now()
        StreamingAlgorithm.__init__(self)

    def __transform_event_date(self, event):
        """
        Converts the timestamp of an event to a datetime object

        Parameters
        ---------------
        event
            Event

        Returns
        ---------------
        event
            Event
        """
        parser = date_parser()
        timestamp = event[self.timestamp_key]
        start_timestamp = event.get(self.start_timestamp_key)
        event[self.timestamp_key] = parser.parse(timestamp)
        if start_timestamp:
            new_start_timestamp = parser.parse(start_timestamp)
            event[self.start_timestamp_key] = new_start_timestamp
        
        if self.first_date > event[self.timestamp_key]:
            self.first_date = event[self.timestamp_key]
        if self.last_date < event[self.timestamp_key]:
            self.last_date = event[self.timestamp_key]

        return event

    def _process(self, event):
        """
        Receives an event from the live event stream,
        and appends it to the current Eventlog object

        Parameters
        ---------------
        event
            Event
        """
        if (self.case_id_key not in event or
            self.activity_key not in event or
            self.timestamp_key not in event):
            return logging.warning(f"{event} does not contain all required keys")

        event = self.__transform_event_date(event)
        self.event_amount += 1
        for trace in self.eventlog:
            if trace.attributes[self.case_id_key] == event[self.case_id_key]:
                return trace.append(event)
        self.eventlog.append(Trace([event], attributes = {
            self.case_id_key: event[self.case_id_key]
        }))
        self.case_amount += 1

    def _current_result(self):
        """
        Gets the current state of the EventlogStream

        Returns
        ----------------
        eventlog
            Eventlog object
        """
        return self.eventlog

event_stream = LiveEventStream()

streaming_eventlog = StreamingEventlog()
streaming_dfg = StreamingDFG()

event_stream.register(streaming_eventlog)
event_stream.register(streaming_dfg)
