from typing import Any
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware


@database_sync_to_async
def get_user(token_key) -> Any | AnonymousUser:
    try:
        return Token.objects.get(key=token_key).user
    except Token.DoesNotExist:
        return AnonymousUser()


class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        # get the query string (e.g., b'token=abc123')
        query_string = scope.get("query_string", b"").decode()

        # parse the token
        token_key = None
        if "token=" in query_string:
            # simple parsing logic
            params = query_string.split("&")
            for param in params:
                if param.startswith("token="):
                    token_key = param.split("=")[1]
                    break

        # authenticate the user
        if token_key:
            scope["user"] = await get_user(token_key)
        else:
            scope["user"] = AnonymousUser()

        # pass control to the next layer (Consumer)
        return await super().__call__(scope, receive, send)
