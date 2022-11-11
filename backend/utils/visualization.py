import pm4py
from pm4py.objects.log.obj import EventLog
from pm4py.algo.filtering.dfg.dfg_filtering import (
    filter_dfg_on_paths_percentage,
    filter_dfg_on_activities_percentage
)

FREQ_DFG_FILE_PATH = './freq_dfg.svg'
PERF_DFG_FILE_PATH = './perf_dfg.svg'

def save_dfg(eventlog: EventLog, activities_count: dict, dfg_detail_percentage: float, mode: str = "frequency"):
    """
    Receives an eventlog, a dict of it's activities counts and a detail percentage.
    Generates and saves an svg image of the log visualization.
    Mode can be "frequency" or "performance".
    Returns a string that represents the generated svg.
    """
    file_path = FREQ_DFG_FILE_PATH
    discover_function = pm4py.discover_dfg
    save_function = pm4py.save_vis_dfg

    if mode != "frequency":
        file_path = PERF_DFG_FILE_PATH
        discover_function = pm4py.discover_performance_dfg
        save_function = pm4py.save_vis_performance_dfg
    
    dfg, start_activities, end_activities = discover_function(eventlog)

    filter_dfg_on_paths_percentage(
        dfg, start_activities, end_activities, activities_count, dfg_detail_percentage
    )

    save_function(dfg, start_activities, end_activities, file_path)

    with open(file_path, encoding='utf-8') as file:
        svg_str = "".join(file.read().splitlines())

    return svg_str

def generate_svg(eventlog: EventLog, dfg_detail_percentage: float = 0.6):
    """
    Receives an eventlog and detail percentage (for log simplification).
    Returns strings that represent the generated svgs for frequency and performance visualizations.
    """
    
    activities_count = {}
    for demanda in eventlog:
        for atividade in demanda:
            name = atividade["tarefa"]
            try:
                activities_count[name] += 1
            except:
                activities_count[name] = 1

    freq_svg_str = save_dfg(eventlog, activities_count, dfg_detail_percentage, "frequency")
    perf_svg_str = save_dfg(eventlog, activities_count, dfg_detail_percentage, "performance")

    return freq_svg_str, perf_svg_str