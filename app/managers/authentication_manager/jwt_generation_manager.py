from datetime import timedelta
from typing import TypedDict

import flask_jwt_extended
from flask import Response, jsonify
from flask_jwt_extended import set_access_cookies, set_refresh_cookies
from utils.request_default_responses import DefaultResponse


class AccessAndRefreshJWT(TypedDict):
    access_token: str
    refresh_token: str


class JWTGenerationManager:
    def __init__(self, access_expire_hour=2, refresh_expire_hour=48):
        """
        :param access_expire_hour: Access token expiration time in hours.
        :param refresh_expire_hour: Refresh token expiration time in hours.
        """
        self.access_expire_hour = access_expire_hour
        self.refresh_expire_hour = refresh_expire_hour

    def generate_token(self, id_user: str, is_refresh=False) -> str:
        """
        Generate an access/refresh token with custom_data.

        :param id_user: The database id of the user for whom the token is generated.
        :param custom_data: Custom data to include in the token.
        :param is_refresh: Wheter to generate a refresh token or an access token
        :return: The generated access token.
        """

        if is_refresh:
            expires = timedelta(hours=self.refresh_expire_hour)
            create_token = flask_jwt_extended.create_refresh_token
        else:
            expires = timedelta(hours=self.access_expire_hour)
            create_token = flask_jwt_extended.create_access_token

        return create_token(identity=id_user, expires_delta=expires)

    def generate_access_and_refresh_tokens(self, id_user: str) -> AccessAndRefreshJWT:
        return {
            'access_token': self.generate_token(id_user, is_refresh=False),
            'refresh_token': self.generate_token(id_user, is_refresh=True),
        }

    def login_with_cookies(self, id_user, resp: dict) -> Response:
        resp = jsonify(resp)
        access_token = self.generate_token(id_user, is_refresh=False)
        refresh_token = self.generate_token(id_user, is_refresh=True)
        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)
        return resp

    @staticmethod
    def logout_with_cookies() -> Response:
        resp = DefaultResponse.success('User successfully logged out')
        set_access_cookies(resp, '')
        set_refresh_cookies(resp, '')
        return resp
