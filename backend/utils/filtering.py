from datetime import datetime
from pm4py.objects.log.obj import EventLog

def filter_log_by_data(log: EventLog, start_date: datetime, end_date: datetime):
    """ Returns the filtered log. Checks if last date of trace occurred within timeframe. """
    filtered_log = EventLog()
    
    for trace in log:
        date_last_event = (trace[-1])["dt_fim"]
        if( start_date < date_last_event < end_date):
            filtered_log.append(trace)

    return filtered_log

def filter_log(log: EventLog, start_date: datetime = None, end_date: datetime = None):
    """
    Filters eventlog in various ways.
    Returns the filtered eventlog and it's details (dfg and statistics).
    """
    if start_date is not None and end_date is not None:
        log = filter_log_by_data(log, start_date, end_date)

    return log