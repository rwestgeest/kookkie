from flask import jsonify, make_response, Response
from dataclasses import dataclass, replace
from typing import Callable, Optional
from .route_builder import add_csrf
from quiltz.domain.results import Result


def build_response(response_builder):
    return response_builder.build()


def from_result_of(result):
    return HTTPResponseBuilder(result)


@dataclass
class HTTPResponseBuilder:
    result: Result
    success_response_fn: Callable[[Result], tuple[dict, int]] = lambda result: (dict(), 204)
    failure_status_code: int = 400
    contains_csrf: bool = False

    def on_success(self, success_response_fn):
        return replace(self, success_response_fn=success_response_fn)

    def on_failure(self, failure_status_code):
        return replace(self, failure_status_code=failure_status_code)

    def with_csrf(self):
        return replace(self, contains_csrf=True)

    def build(self):
        if self.result.is_success():
            body, status_code = self.success_response_fn(self.result)
            response = make_response(jsonify(body), status_code)
            return self.contains_csrf and add_csrf(response) or response
        else:
            return jsonify(dict(message=self.result.message)), self.failure_status_code


def ok() -> tuple[Response, int]:
    return jsonify({}), 200


def created() -> tuple[Response, int]:
    return jsonify({}), 201


def no_content() -> tuple[Response, int]:
    return jsonify({}), 204


def not_found(result: Optional[Result] = None) -> tuple[Response, int]:
    body = result and result.body or {}
    return jsonify(body), 404


def bad_request(result: Result) -> tuple[Response, int]:
    return jsonify(result.body), 400
