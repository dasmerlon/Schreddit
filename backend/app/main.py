#!/usr/bin/env python
import logging
import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api_v1.main import router
from app.core.config import settings
from app.db.init_db import init_mongodb, init_neo4j

app = FastAPI(
    title="Reddit-Klon",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)
app.include_router(router, prefix=settings.API_V1_STR)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.FRONTEND_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    # initialize DBs
    init_mongodb()
    init_neo4j()

    if os.environ.get("NEOMODEL_CYPHER_DEBUG", False):
        uvicorn.config.logger
        logging.basicConfig()
        logging.getLogger("neomodel").setLevel(logging.DEBUG)

    # run server
    uvicorn.run(app, host='0.0.0.0')
