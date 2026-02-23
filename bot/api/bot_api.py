class BotApi:
    def __init__(self, client):
        self.client = client

    def _form_auth_header_for_user(self, user_id: int):
        return {"HTTP_X_TELEGRAM_USER_ID": user_id}

    def _get_default_headers(self, **kwargs):
        headers = {}

        user_id = kwargs.get("user_id")
        if isinstance(user_id, int):
            headers.update(self._form_auth_header_for_user(user_id))

        return headers

    async def _get_client_method(self, method: str) -> callable:
        method = getattr(self.client, method)
        assert callable(method), "Client has not implemented method {}".format(method)
        return method

    async def get_ticket_messages(self, user_id: int, ticket_id: int, page: int = 1):
        headers = self._get_default_headers(user_id=user_id)
        query_params = {
            "page": page,
            "pk": ticket_id
        }

        return await self.client.get_ticket_messages(headers=headers, query_params=query_params)

    async def create_ticket_message(self, user_id: int, text: str, ticket_id: int):
        headers = self._get_default_headers(user_id=user_id)
        body = {
            "text": text,
            "ticket": ticket_id
        }

        return await self._get_client_method("create_ticket_message")(headers=headers, body=body)

    async def get_tickets(self, user_id: int, page: int = 1):
        headers = self._get_default_headers(user_id=user_id)
        query_params = {"page": page}

        return await self._get_client_method("get_tickets")(headers=headers, query_params=query_params)

    async def create_ticket(self, user_id: int, name: str):
        headers = self._get_default_headers(user_id=user_id)
        body = {"name": name}

        return await self._get_client_method("create_ticket")(headers=headers, body=body)

    async def close_ticket(self, user_id: int, ticket_id: int):
        headers = self._get_default_headers(user_id=user_id)
        query_params = {"pk": ticket_id}

        return await self._get_client_method("close_ticket")(headers=headers, query_params=query_params)
