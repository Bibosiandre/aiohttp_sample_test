import uuid
from aiohttp.web_exceptions import HTTPNotFound, HTTPUnauthorized, HTTPForbidden
from aiohttp_apispec import docs, request_schema, response_schema, querystring_schema

from app.crm.models import User
from app.crm.schemes import UserSchema, UserGetSchema, UserGetRequestSchema, GetUserResponseSchema, UserAddSchema

from app.web.app import View
from app.web.schemes import ResponseSchema
from app.web.utils import json_response, basic_auth


class AddUserView(View):
    @docs(tags=['crm'], summary='Add nu', description='Add nu(new user) to DB')
    @request_schema(UserAddSchema)
    @response_schema(ResponseSchema, 200)
    async def post(self):
        data = self.request['data']
        user = User(email=data['email'], id_=uuid.uuid4())
        await self.request.app.crm_accessor.add_user(user)
        return json_response()


class ListUsersView(View):
    @docs(tags=['crm'], summary='lu', description='lu(list user) to DB')
    @request_schema(UserSchema)
    @response_schema(ResponseSchema, 200)
    async def get(self):
        if self.request.headers.get('Authorization'):
            raise HTTPUnauthorized
        if not basic_auth(self.request.headers['Authorization'], username=self.request.app.config.username, password=self.request.app.config.password):
            raise HTTPForbidden
        users = await self.request.app.crm_accessor.list_users()
        raw_users = [{'email': user.email, 'id': str(user.id_)} for user in users]
        return json_response(data={'users': raw_users})


class GetUserView(View):
    @docs(tags=['crm'], summary='Gu', description='Gu(get user) from DB')
    @querystring_schema(UserGetRequestSchema)
    @response_schema(GetUserResponseSchema, 200)
    async def get(self):
        if self.request.headers.get('Authorization'):
            raise HTTPUnauthorized
        if not basic_auth(self.request.headers['Authorization'], username=self.request.app.config.username, password=self.request.app.config.password):
            raise HTTPForbidden
        user_id = self.request.query['id']
        user = await self.request.app.crm_accessor.get_user(uuid.UUID(user_id))
        if user:
            return json_response(data={'user': {'email': user.email, 'id': user.id_}})
        else:
            raise HTTPNotFound
