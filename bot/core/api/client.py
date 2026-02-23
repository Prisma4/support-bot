from typing import Dict, Type, Optional, Any, Literal

import httpx
from pydantic import BaseModel

from core.api.endpoint import Endpoint


class ApiClient:
    def __init__(
            self,
            base_url: str,
            headers: Dict[str, str]
    ):
        self.base_url = base_url

        self.client = httpx.AsyncClient(
            headers=headers,
            timeout=30.0,
            follow_redirects=True,
        )
        self.endpoints: Dict[str, Endpoint] = {}

    def register_endpoint(
            self,
            name: str,
            path: str,
            body_validator: Optional[Type[BaseModel]] = None,
            query_validator: Optional[Type[BaseModel]] = None,
            response_validator: Optional[Type[BaseModel]] = None,
            method: Literal["GET", "POST", "DELETE", "PATCH"] = 'POST'
    ):
        self.endpoints[name] = Endpoint(path, body_validator, query_validator, response_validator, method)

    def request(self, endpoint: Endpoint):
        async def _request(
                body: Optional[dict] = None,
                query_params: Optional[dict] = None,
                headers: Optional[dict] = None,
                **kwargs: Any,
        ) -> Any:
            validated_data = endpoint.validate_input_data(body, query_params)
            query_params = validated_data.get('query_params')

            path = endpoint.path

            if query_params:
                pk = query_params.get('pk')
                if isinstance(pk, int):
                    if "{id}" in path:
                        path = path.replace("{id}", str(pk))

            url = f"{self.base_url}/{path}"

            final_headers = {**self.client.headers, **(headers or {})}

            response = await self.client.request(
                method=endpoint.method,
                url=url,
                data=validated_data.get("data"),
                params=query_params,
                headers=final_headers,
                **kwargs,
            )

            response.raise_for_status()
            validated_response = endpoint.validate_output_data(response.json())

            return validated_response

        return _request

    def __getattr__(self, name: str):
        if name in self.endpoints:
            endpoint = self.endpoints[name]
            return self.request(endpoint)
        return getattr(self.obj, name)
