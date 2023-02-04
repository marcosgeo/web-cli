# auth.py

import re
from bumbo.middleware import Middleware


STATIC_TOKEN = "IxJCjdaxSqbe8xD"


class TokenMiddleware(Middleware):
    _regex = re.compile(r"^Token: (\w+)$")

    def process_request(self, req):
        header = req.headers.get("Authorization", "")
        match = self._regex.match(header)
        token = match.group(1) if match else None
        req.token = token


class InvalidTokenException(Exception):
    pass


def login_required(handler):
    def wrapped_view(request, response, *args, **kwargs):
        print(f"  *** login_required ***   handler: {handler}")
        token = getattr(request, "token", None)
        if token is None or not token == STATIC_TOKEN:
            raise InvalidTokenException("Invalid Token")
        return handler(request, response, *args, **kwargs)
    return wrapped_view


def on_exception(req, resp, exception):
    if isinstance(exception, InvalidTokenException):
        resp.text = "Token is invalid"
        resp.status_code = 401

