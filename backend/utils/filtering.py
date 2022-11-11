from datetime import datetime
from .stats import get_log_statistics
from .visualization import generate_svg
from pm4py.objects.log.obj import EventLog

def filter_log_by_data(log: EventLog, start_date: datetime, end_date: datetime):
    """ Returns the filtered log. Checks if last date of trace occurred within timeframe. """
    filtered_log = EventLog()
    
    for trace in log:
        date_last_event = (trace[-1])["dt_fim"]
        if( start_date < date_last_event < end_date):
            filtered_log.append(trace)

    return filtered_log

def filter_log(log: EventLog, start_date: datetime = None, end_date: datetime = None, dfg_detail_level: int = 2):
    """
    Filters eventlog in various ways.
    Returns the filtered eventlog and it's details (dfg and statistics).
    """
    if start_date is not None and end_date is not None:
        log = filter_log_by_data(log, start_date, end_date)
    
    dfg_detail_percentage = (1 + dfg_detail_level) * 20 / 100
    freq_dfg_file_path, perf_dfg_file_path = generate_svg(log, dfg_detail_percentage)

    with open(freq_dfg_file_path, encoding='utf-8') as file:
        freq_dfg_str = "".join(file.read().splitlines())

    with open(perf_dfg_file_path, encoding='utf-8') as file:
        perf_dfg_str = "".join(file.read().splitlines())

    stats = get_log_statistics(log)
    
    output = {
        "filters": {
            "exhibition": "frequency",
            "detail_level": dfg_detail_level,
            "startDate": start_date,
            "endDate": end_date
        },

        "statistics": stats,

        "freq_svg": freq_dfg_str,
        "perf_svg": perf_dfg_str
    }

    return log, output