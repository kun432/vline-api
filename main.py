import traceback

from fastapi import FastAPI
from fastapi import Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import PlainTextResponse

app = FastAPI()


class CustomException(Exception):
    default_status_code = status.HTTP_200_OK

    def __init__(
        self,
        msg: str,
        status_code: int = default_status_code,
    ) -> None:
        self.status_code = status_code
        self.detail = ""


class HttpRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        try:
            response: Response = await call_next(request)
        except Exception as e:
            ce = CustomException(e)
            response = PlainTextResponse(content=ce.detail, status_code=ce.status_code)

        return response


@app.get("/")
async def check_vline(place, order, timediff=0.0):
    time_threshold = 2.0
    if place == "" or order == "":
        raise CustomException(msg="引数エラー")
    try:
        place = int(place)
        order = str(order)
        timediff = float(timediff)

        orders = order.split("-")[-3:]
        max_pos = int(orders[0])
        min_pos = int(orders[0])
        prv_pos = int(orders[0])
        max_down = 0
        for i in orders[1:]:
            i = int(i)
            if prv_pos == i:
                continue
            else:
                if max_pos < i:
                    max_pos = i
                if min_pos > i:
                    min_pos = i
                if prv_pos < i:
                    diff = i - prv_pos
                    if max_down < diff:
                        max_down = diff
                    prv_pos = i
        final_diff = max_pos - place

        if final_diff >= 2 and max_down >= 2:
            if time_threshold <= time_threshold:
                return PlainTextResponse(content="1")

        return PlainTextResponse(content="0")

    except:
        raise CustomException(msg="入力エラー")


app.add_middleware(HttpRequestMiddleware)
