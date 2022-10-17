import json

from fastapi import FastAPI, Request, Response

from tools.c_time import CTime
from tools.record_log import recordLog
from phone_location import phones_api

logger = recordLog()

app = FastAPI()

app.include_router(phones_api.router)


@app.get("/", tags=["root"])
async def root():
    return {"message": "Welcome to FastApi"}


@app.middleware("http")
async def add_process_time_header(request: Request, call_next) -> Response:
    logger.info(
        f'''
        用户aa 在 [{CTime.get_now_time()}],
        访问了 [{request.url}], 
        路径参数是 [{request.url.path}], 
        查询参数是[{request.url.query}],
        访问者ip地址为[{request.client.host}],
        访问着通过[{request.client.port}]访问
        ''')
    start_time = CTime.get_now_time()
    response = await call_next(request)
    process_time = CTime.get_now_time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    resp_content = b""
    async for line in response.body_iterator:
        resp_content += line
    try:
        resp_body = resp_content.decode()
    except Exception:
        resp_body = str(resp_content)
    logger.info(f'''
    用户aa 在 [{CTime.get_now_time()}],
    访问者ip地址为[{request.client.host}],
    访问到的内容为[{resp_body}]
    ''')
    return Response(
        content=resp_content,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type
    )
