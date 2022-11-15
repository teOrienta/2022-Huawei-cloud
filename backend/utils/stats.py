from pm4py.objects.log.obj import EventLog
from .streaming import Parameters

def average(l: list):
    avg = 0
    if len(l) > 0:
        avg = round(sum(l) / len(l), 2)
    return avg

def format_timedelta(seconds: float) -> str:
    intervals = (
        ('years', 31536000),
        ('months', 2592000),
        ('weeks', 604800),  
        ('days', 86400),    
        ('hours', 3600),    
        ('minutes', 60),
        ('seconds', 1),
    )
    result = []
    if seconds is None:
        return "instant"

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(int(value), name))

    if len(result) == 0: result = ["instant"]
    return ', '.join(result[:2])

def get_log_statistics(eventlog: EventLog):
    """
    Receives and EventLog.
    Returns a set of statistics about it:
    {
        "cases": int (number of cases contained within the EventLog),
        "activities": int (number of activities contained within the Eventlog),
        "averageCaseDuration": str (average duration of each case, in seconds),
        "averageActivityDuration": str (average duration of each activity, in seconds)
    }
    """
    timestamp_key = eventlog.attributes[Parameters.TIMESTAMP_KEY]
    start_timestamp_key = eventlog.attributes[Parameters.START_TIMESTAMP_KEY]

    activities_amount = 0
    case_durations = []
    activities_durations = []

    for trace in eventlog:
        trace_duration = 0
        activities_amount += len(trace)

        for activity in trace:
            activity_duration = (activity[timestamp_key] - activity[start_timestamp_key]).total_seconds()
            activities_durations.append(activity_duration)
            trace_duration += activity_duration

        case_durations.append(trace_duration)

    cases_amount = len(eventlog)
    activities_amount = len(activities_durations)

    avg_case_duration = average(case_durations)
    avg_activity_duration = average(activities_durations)

    return {
        "cases": cases_amount,
        "activities": activities_amount,
        "averageCaseDuration": format_timedelta(avg_case_duration),
        "averageActivityDuration": format_timedelta(avg_activity_duration)
    }