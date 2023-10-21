from fastapi import FastAPI
from conf import tags_metadata

app = FastAPI(
    title='miac_map_api',
    openapi_tags=tags_metadata,
)
