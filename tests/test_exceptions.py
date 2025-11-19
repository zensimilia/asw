import pytest
from pytest_httpserver import HTTPServer

from asw import AISUP, exceptions


@pytest.fixture(scope="session")
def http_server():
    server = HTTPServer()
    server.start()
    server.expect_request("/404", method="GET").respond_with_data("not found", status=404)
    server.expect_request("/500", method="GET").respond_with_data("server error", status=500)
    server.expect_request("/401", method="POST").respond_with_data("un authorized", status=401)
    server.expect_request("/no-json", method="POST").respond_with_data("corrupted", status=200)
    yield server
    server.stop()


@pytest.fixture(scope="session")
def aisup(http_server):
    return AISUP(http_server.url_for("/"), "t0ken")


def test_get_404(aisup: AISUP):
    with pytest.raises(exceptions.HTTPError):
        aisup.get("/404")


def test_get_500(aisup: AISUP):
    with pytest.raises(exceptions.HTTPError):
        aisup.get("/500")


def test_post_401(aisup: AISUP):
    with pytest.raises(exceptions.UnauthorizedError, match="Not authenticated"):
        aisup.post("/401", {"lorem": "ipsum"})


def test_post_json_decode_error(aisup: AISUP):
    with pytest.raises(exceptions.JSONDecodeError):
        aisup.post("/no-json", {"lorem": "ipsum"})


def test_request_error():
    # Invalid URL: No scheme supplied
    aisup = AISUP("bad_request", "t0ken")
    with pytest.raises(exceptions.AisupError):
        aisup.post("/")


def test_network_error():
    aisup = AISUP("http://no_network", "t0ken")
    with pytest.raises(exceptions.NetworkError):
        aisup.post("/")
