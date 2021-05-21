#!/usr/bin/env python

import uvicorn
from fastapi import FastAPI

from app.api.api_v1.main import router
from app.core.config import settings
from app.db.init_db import init_neo4j
from app.sessions.init_db import init_redis

app = FastAPI(
    title="Reddit-Klon",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)
app.include_router(router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    # initialize DBs
    init_neo4j()
    init_redis()

    # run server
    uvicorn.run(app)
