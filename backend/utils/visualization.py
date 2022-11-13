from pm4py.algo.filtering.dfg.dfg_filtering import filter_dfg_on_paths_percentage
from pm4py.statistics.attributes.log import get as attr_get
from pm4py.objects.log.obj import EventLog
from .streaming import Parameters
import pm4py, tempfile

def save_dfg(eventlog: EventLog, activities_count: dict, dfg_detail_percentage: float, mode: str = "frequency"):
    """
    Receives an eventlog, a dict of it's activities counts and a detail percentage.
    Generates and saves an svg image of the log visualization.
    Mode can be "frequency" or "performance".
    Returns a string that represents the generated svg.
    """
    file_path = tempfile.NamedTemporaryFile(suffix='.svg')
    discover_function = pm4py.discover_dfg
    save_function = pm4py.save_vis_dfg
    file_path.close()

    if mode != "frequency":
        discover_function = pm4py.discover_performance_dfg
        save_function = pm4py.save_vis_performance_dfg
    
    dfg, start_activities, end_activities = discover_function(eventlog)
    if mode != "frequency":
        dfg = {key: value["median"] for key, value in dfg.items()}

    dfg, _, _, _ = filter_dfg_on_paths_percentage(dfg, start_activities,
                end_activities, activities_count, dfg_detail_percentage)
    save_function(dfg, start_activities, end_activities, file_path.name)

    return file_path.name

def generate_svg(eventlog: EventLog, dfg_detail_percentage: float = 0.6):
    """
    Receives an eventlog and detail percentage (for log simplification).
    Returns strings that represent the generated svgs for frequency and performance visualizations.
    """
    
    activity_key = eventlog.attributes[Parameters.ACTIVITY_KEY]
    activities_count = attr_get.get_attribute_values(eventlog, activity_key)
    freq_svg_str = save_dfg(eventlog, activities_count, dfg_detail_percentage, "frequency")
    perf_svg_str = save_dfg(eventlog, activities_count, dfg_detail_percentage, "performance")

    return freq_svg_str, perf_svg_str