from typing import Type, Optional, Union

from pydantic import BaseModel


class Endpoint:
    def __init__(
            self,
            path: str,
            body_validator: Optional[Type[BaseModel]] = None,
            query_validator: Optional[Type[BaseModel]] = None,
            response_validator: Optional[Type[BaseModel]] = None,
            method: str = 'POST'
    ):
        self.path = path
        self.body_validator = body_validator
        self.query_validator = query_validator
        self.response_validator = response_validator
        self.method = method

    def _validate_input_body(self, data: dict) -> Optional[dict]:
        if not self.body_validator:
            return
        return self.body_validator(**data).model_dump()

    def _validate_query_params(self, data: dict) -> Optional[dict]:
        if not self.query_validator:
            return
        return self.query_validator(**data).model_dump()

    def validate_input_data(self, body: dict, query_params: dict) -> dict:
        validated_body = self._validate_input_body(body)
        validated_query_params = self._validate_query_params(query_params)
        return {
            "data": validated_body,
            "params": validated_query_params
        }

    def validate_output_data(self, data: Union[dict, list]) -> Optional[Union[BaseModel, list]]:
        if self.response_validator is None:
            return

        if isinstance(data, dict):
            return self.response_validator(**data)
        elif isinstance(data, list):
            return [self.response_validator(**obj) for obj in data]
