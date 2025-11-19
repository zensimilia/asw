import pytest
from pytest_httpserver import HTTPServer
from werkzeug.wrappers import Response

from asw import AISUP

TEST_JSON_RESPONSE = {"lorem": "ipsum"}
TEST_CONTENT = "testdatachunk"
TEST_HEADERS = {
    "content-disposition": "attachment;filename=file.txt",
    "digest": "sha-256=NGOrx8eSPi8LuKlhGv8h55SDbq0VdE0SEWjV32kh9wE=",
    "transfer-encoding": "chunked",
}


@pytest.fixture(scope="session")
def http_server():
    server = HTTPServer()
    server.start()
    server.expect_request("/get", method="GET").respond_with_json(TEST_JSON_RESPONSE)
    server.expect_request("/post", method="POST").respond_with_json(TEST_JSON_RESPONSE)
    server.expect_request("/file").respond_with_handler(custom_chunked_handler)
    yield server
    server.stop()


@pytest.fixture(scope="session")
def aisup(http_server):
    return AISUP(http_server.url_for("/"), "t0ken")


def custom_chunked_handler(_request):
    def dynamic_generator():
        yield b"11\r\nchunk chunk chunk\r\n"
        yield b"0\r\n\r\n"

    return Response(
        dynamic_generator(),
        content_type="application/octet-stream",
        headers=TEST_HEADERS,
        status=200,
    )


def test_get(aisup):
    assert aisup.get("get") == TEST_JSON_RESPONSE


def test_post(aisup):
    assert aisup.post("post") == TEST_JSON_RESPONSE


def test_download(aisup):
    assert aisup.download("guid", name="test", endpoint="file")[-8:] == "test.txt"
