import pm4py
from pm4py.objects.log.obj import EventLog
from pm4py.algo.filtering.dfg.dfg_filtering import (
    filter_dfg_on_paths_percentage,
    filter_dfg_on_activities_percentage
)

FREQ_DFG_FILE_PATH = '../freq_dfg.svg'
PERF_DFG_FILE_PATH = '../perf_dfg.svg'

def save_dfg(eventlog: EventLog, activities_count: dict, dfg_detail_percentage: float, mode: str = "frequency"):
    """
    Receives an eventlog, a dict of it's activities counts and a detail percentage.
    Generates and saves an svg image of the log visualization.
    Mode can be "frequency" or "performance"
    Returns saved dfg filepath.
    """
    if mode == "frequency":
        file_path = FREQ_DFG_FILE_PATH
        dfg, start_activities, end_activities = pm4py.discover_dfg(eventlog)
        
        filter_dfg_on_paths_percentage(
            dfg, start_activities, end_activities, activities_count, dfg_detail_percentage
        )

        pm4py.save_vis_dfg(dfg, start_activities, end_activities, file_path)

    else:
        file_path = PERF_DFG_FILE_PATH
        dfg, start_activities, end_activities = pm4py.discover_performance_dfg(eventlog)

        filter_dfg_on_paths_percentage(
            dfg, start_activities, end_activities, activities_count, dfg_detail_percentage
        )

        pm4py.save_vis_performance_dfg(dfg, start_activities, end_activities, file_path)

    return file_path

def generate_svg(eventlog: EventLog, dfg_detail_percentage: float = 0.6):
    """
    Receives an eventlog and detail percentage (for log simplification).
    Returns SVG images filepaths for frequency and performance visualizations.
    """
    
    activities_count = {}
    for demanda in eventlog:
        for atividade in demanda:
            name = atividade["tarefa"]
            try:
                activities_count[name] += 1
            except:
                activities_count[name] = 1

    freq_dfg_file_path = save_dfg(eventlog, activities_count, dfg_detail_percentage, "frequency")
    perf_dfg_file_path = save_dfg(eventlog, activities_count, dfg_detail_percentage, "performance")

    return freq_dfg_file_path, perf_dfg_file_path