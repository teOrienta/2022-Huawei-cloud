from utils import event_stream, streaming_dfg, streaming_eventlog, database
from pm4py.objects.log.obj import Event 
from pm4py import save_vis_dfg
from routers import routers

import tempfile, json, logging
from threading import Thread

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from client import consume_events_queue

app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routers)
event_stream.start()

def events_callback(channel, method, prop, body):
    logger = logging.getLogger(__name__)
    event = json.loads(body)
    logger.info(f"Received event: {event}")

    event = Event(event)
    database.insert_log_event(
        analysis = "live",
        case_id = event[streaming_eventlog.case_id_key],
        activity = event[streaming_eventlog.activity_key],
        resource = event.get(streaming_eventlog.resource_key),
        end_timestamp = event[streaming_eventlog.timestamp_key],
        start_timestamp = event.get(streaming_eventlog.start_timestamp_key,
                                    event[streaming_eventlog.timestamp_key])
    )
    event_stream.append(event)
    channel.basic_ack(delivery_tag = method.delivery_tag)

@app.get("/api/image/download/")
def download_dfg_image():
    file_path = tempfile.NamedTemporaryFile(suffix='.svg')
    file_path.close()

    dfg, _, sa, ea = streaming_dfg.get()
    save_vis_dfg(dfg, sa, ea, file_path.name)
    return FileResponse(file_path.name)

Thread(target=consume_events_queue, args=(events_callback,)).start()
