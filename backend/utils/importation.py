from .streaming import (Parameters, DEFAULT_NAME_KEY, DEFAULT_RESOURCE_KEY, 
                        DEFAULT_START_TIMESTAMP_KEY, DEFAULT_TIMESTAMP_KEY,
                        constants)
import pandas, pm4py, csv
from fastapi import File

def csv_file_to_eventlog(file: File, columns: dict):
    start_timestamp_key = columns.get('start_timestamp_key')
    columns_to_datetime = [x for x in [
        columns.get('timestamp_key'),
        start_timestamp_key
    ] if x is not None]

    dialect = csv.Sniffer().sniff(file.read(1024).decode('utf-8'))
    file.seek(0)

    df = pandas.read_csv(file, encoding = "utf-8", sep=dialect.delimiter,
                         parse_dates=columns_to_datetime)

    if (start_timestamp_key and 
        start_timestamp_key in df and
        df[start_timestamp_key].dtype == 'object'):
        df[start_timestamp_key] = pandas.to_datetime(df[start_timestamp_key],
                                                     errors = 'coerce')
        df = df[df[start_timestamp_key].notna()]

    default_start_timestamp_key = DEFAULT_START_TIMESTAMP_KEY
    rename_columns = {
        columns["case_id_key"]: constants.CASE_CONCEPT_NAME,
        columns["resource_key"]: DEFAULT_RESOURCE_KEY,
        columns["activity_key"]: DEFAULT_NAME_KEY,
        columns["timestamp_key"]: DEFAULT_TIMESTAMP_KEY,
        columns["start_timestamp_key"]: default_start_timestamp_key,
    }
    if columns["resource_key"] is None:
        del rename_columns[columns["resource_key"]]
    if columns["start_timestamp_key"] is None:
        del rename_columns[columns["start_timestamp_key"]]
        default_start_timestamp_key = DEFAULT_TIMESTAMP_KEY

    df = df.rename(columns=rename_columns)
    df = pm4py.format_dataframe(df)
    event_log = pm4py.convert_to_event_log(df)

    event_log.attributes[Parameters.CASE_ID_KEY] = constants.CASE_CONCEPT_NAME
    event_log.attributes[Parameters.ACTIVITY_KEY] = DEFAULT_NAME_KEY
    event_log.attributes[Parameters.RESOURCE_KEY] = DEFAULT_RESOURCE_KEY
    event_log.attributes[Parameters.TIMESTAMP_KEY] = DEFAULT_TIMESTAMP_KEY
    event_log.attributes[Parameters.START_TIMESTAMP_KEY] = default_start_timestamp_key

    return event_log
