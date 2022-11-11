from pm4py.streaming.algo.discovery.dfg import algorithm as dfg_discovery
from pm4py.streaming.stream.live_event_stream import LiveEventStream
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

event_stream = LiveEventStream()
streaming_dfg = dfg_discovery.apply()

event_stream.register(streaming_dfg)
event_stream.start()

def events_callback(channel, method, prop, body):
    logger = logging.getLogger(__name__)
    event = json.loads(body)
    logger.info(f"Received event: {event}")

    event = Event(event)
    event_stream.append(event)
    channel.basic_ack(delivery_tag = method.delivery_tag)

@app.get("/api/image/")
def get_dfg_image():
    file_path = tempfile.NamedTemporaryFile(suffix='.svg')
    file_path.close()

    dfg, _, sa, ea = streaming_dfg.get()
    save_vis_dfg(dfg, sa, ea, file_path.name)
    with open(file_path.name, encoding='utf-8') as file:
        image = "".join(file.read().splitlines())
    return image

@app.get("/api/image/download/")
def download_dfg_image():
    file_path = tempfile.NamedTemporaryFile(suffix='.svg')
    file_path.close()

    dfg, _, sa, ea = streaming_dfg.get()
    save_vis_dfg(dfg, sa, ea, file_path.name)
    return FileResponse(file_path.name)

Thread(target=consume_events_queue, args=(events_callback,)).start()
