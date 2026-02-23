class BotApi:
    def __init__(self, client):
        self.client = client

    def _form_auth_header_for_user(self, user_id: int):
        return {"HTTP_X_TELEGRAM_USER_ID": str(user_id)}

    def _get_default_headers(self, **kwargs):
        headers = {}

        user_id = kwargs.get("user_id")
        if isinstance(user_id, int):
            headers.update(self._form_auth_header_for_user(user_id))

        return headers

    def _get_client_method(self, method: str) -> callable:
        method = getattr(self.client, method)
        assert callable(method), "Client has not implemented method {}".format(method)
        return method

    async def get_ticket_messages(self, user_id: int, ticket_id: int, page: int = 1):
        headers = self._get_default_headers(user_id=user_id)
        query_params = {
            "page": page,
            "pk": ticket_id
        }

        method = self._get_client_method("get_ticket_messages")
        return await method(headers=headers, query_params=query_params)

    async def create_ticket_message(self, user_id: int, text: str, ticket_id: int):
        headers = self._get_default_headers(user_id=user_id)
        body = {
            "text": text,
            "ticket": ticket_id
        }

        method = self._get_client_method("create_ticket_message")
        return await method(headers=headers, body=body)

    async def get_tickets(self, user_id: int, page: int = 1):
        headers = self._get_default_headers(user_id=user_id)
        query_params = {"page": page}

        method = self._get_client_method("get_tickets")
        return await method(headers=headers, query_params=query_params)

    async def create_ticket(self, user_id: int, name: str):
        headers = self._get_default_headers(user_id=user_id)
        body = {"name": name}

        method = self._get_client_method("create_ticket")
        return await method(headers=headers, body=body)

    async def close_ticket(self, user_id: int, ticket_id: int):
        headers = self._get_default_headers(user_id=user_id)
        query_params = {"pk": ticket_id}

        method = self._get_client_method("close_ticket")
        return await method(headers=headers, query_params=query_params)
