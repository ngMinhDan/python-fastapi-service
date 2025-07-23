# call_next is a function provided by fastapi, actually from starlette.
# it take current request object and forward it to the next handler in the next middleware stack

# why python can do it ?
# python treats function like values , you can pass them to other function , assign them to variable,
# so what powers things like:
# middleware chains , dependency injections, decorators

# we can use ratelimit like a depend or use middleware to add into fastapi app

from ast import Dict
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from fastapi import FastAPI

MAX_REQUESTS, WINDOW_SEC = 10, 60


class SlidingWindowRateLimit(BaseHTTPMiddleware):
    """
    Sliding window store all key and timestamp in memory
    """

    def __init__(self, app: FastAPI):
        super().__init__(app)
        self.limit = MAX_REQUESTS
        self.window = WINDOW_SEC
        self.store: Dict[str, list[float]] = {}

    async def dispatch(self, request: Request, call_next) -> Response:
        client_ip = request.client.host
        now = time.time()

        request_times = self.store.get(client_ip, [])
        print(f"{client_ip}: {request_times}")

        # remove expired requests
        request_times = [t for t in request_times if now - t < self.window]
        self.store[client_ip] = request_times

        if len(request_times) >= self.limit:
            return Response("Too many requests", status_code=429)

        request_times.append(now)
        self.store[client_ip] = request_times

        response = await call_next(request)
        return response


class FixedWindowRateLimit(BaseHTTPMiddleware):
    """
    Fixed window rate limit middleware, store window data and count of requests in memory
    """

    def __init__(self, app: FastAPI):
        super().__init__(app)
        self.limit = MAX_REQUESTS
        self.window = WINDOW_SEC
        self.store: Dict[str, tuple[int, int]] = {}

    async def dispatch(self, request: Request, call_next) -> Response:
        client_ip = request.client.host
        now = time.time()

        current_window = int(now - (now % self.window))
        window_data = self.store.get(client_ip)

        if window_data is None or window_data[0] != current_window:
            self.store[client_ip] = (current_window, 1)
        else:
            if window_data[1] >= self.limit:
                return Response("Too many requests", status_code=429)
            self.store[client_ip] = (current_window, window_data[1] + 1)

        response = await call_next(request)
        return response
