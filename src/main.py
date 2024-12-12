from contextlib import asynccontextmanager
from typing import AsyncIterator

import uvicorn
from fastapi import FastAPI, Request

from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse

from src.api.v1 import router
from src.core.db_helper import db_helper


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    await db_helper.connect_mongo()
    yield
    await db_helper.close_mongo_connect()


app = FastAPI(lifespan=lifespan)

app.include_router(router)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error_type": exc.status_code,
            "error_message": exc.detail,
        },
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
