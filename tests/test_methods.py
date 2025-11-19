import pytest
from pytest_httpserver import HTTPServer

from asw import AISUP

JSON_RESPONSE = {"lorem": "ipsum"}


@pytest.fixture
def httpserver(httpserver: HTTPServer):
    httpserver.expect_request("/get", method="GET").respond_with_json(JSON_RESPONSE)
    httpserver.expect_request("/post", method="POST").respond_with_json(JSON_RESPONSE)
    yield httpserver
    httpserver.check_assertions()


@pytest.fixture
def aisup(httpserver: HTTPServer) -> AISUP:
    return AISUP(httpserver.url_for("/"), "t0ken")


def test_get(aisup: AISUP):
    assert aisup.get("get") == JSON_RESPONSE


def test_post(aisup: AISUP):
    assert aisup.post("post") == JSON_RESPONSE
