import pm4py
import pandas as pd
from database.models import LicitacoesModel

CASE_ID_COLUMN = 'numeroLicitacao'
ACTIVITY_COLUMN = 'situacaoLicitacao'
START_TIMESTAMP_COLUMN = 'dataAbertura'
TIMESTAMP_COLUMN = 'dataResultado'

def generate_eventlog(licitacoes: list[LicitacoesModel]):
    """
    Receives a list of LicitacoesModel to transform into an eventlog.
    Returns an eventlog.
    """

    df = pd.DataFrame(licitacoes, columns=licitacoes[0]._fields)
    
    rename_columns = {
        CASE_ID_COLUMN: 'case:concept:name',
        ACTIVITY_COLUMN: 'concept:name',
        START_TIMESTAMP_COLUMN: 'time:start_timestamp',
        TIMESTAMP_COLUMN: 'time:timestamp'
    }
    df = df.rename(columns=rename_columns)

    df = pm4py.format_dataframe(
        df,
        case_id='case:concept:name',
        activity_key='concept:name',
        start_timestamp_key='time:start_timestamp',
        timestamp_key='time:timestamp'
    )

    eventlog = pm4py.convert_to_event_log(df)

    return eventlog