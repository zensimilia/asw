import pytest
from pytest_httpserver import HTTPServer

from asw import AISUP

JSON_RESPONSE = {"lorem": "ipsum"}


@pytest.fixture(scope="session")
def http_server():
    server = HTTPServer()
    server.start()
    server.expect_request("/get", method="GET").respond_with_json(JSON_RESPONSE)
    server.expect_request("/post", method="POST").respond_with_json(JSON_RESPONSE)
    yield server
    server.stop()


@pytest.fixture(scope="session")
def aisup(http_server):
    return AISUP(http_server.url_for("/"), "t0ken")


def test_get(aisup: AISUP):
    assert aisup.get("get") == JSON_RESPONSE


def test_post(aisup: AISUP):
    assert aisup.post("post") == JSON_RESPONSE
