from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError


@database_sync_to_async
def get_user(token):
    try:
        token = AccessToken(token)
        user_id = token.payload["user_id"]
        user = get_user_model().objects.get(pk=user_id)
        return user
    except (ValidationError, TokenError):
        return AnonymousUser()


class QueryParamsAuthMiddleware(BaseMiddleware):

    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        params = parse_qs(scope["query_string"].decode())
        if "access_token" in params:
            access_token = params["access_token"][0]
            user = await get_user(access_token)
            scope["user"] = user
        else:
            scope["user"] = AnonymousUser()
        return await super().__call__(scope, receive, send)
