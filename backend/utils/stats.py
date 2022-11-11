from pm4py.objects.log.obj import EventLog

START_TIMESTAMP_KEY = 'dt_inicio'
END_TIMESTAMP_KEY = 'dt_fim'

def average(l: list):
    avg = 0
    if len(l) > 0:
        avg = round(sum(l) / len(l), 2)
    return avg

def get_log_statistics(eventlog: EventLog):
    """
    Receives and EventLog.
    Returns a set of statistics about it:
    {
        "cases": int (number of cases contained within the EventLog),
        "activities": int (number of activities contained within the Eventlog),
        "averageCaseDuration": int (average duration of each case, in seconds),
        "averageActivityDuration": int (average duration of each activity, in seconds)
    }
    """
    activities_amount = 0
    case_durations = []
    activities_durations = []

    for trace in eventlog:
        trace_duration = 0
        activities_amount += len(trace)

        for activity in trace:
            activity_duration = (activity[END_TIMESTAMP_KEY] - activity[START_TIMESTAMP_KEY]).total_seconds()
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
        "averageCaseDuration": avg_case_duration,
        "averageActivityDuration": avg_activity_duration
    }