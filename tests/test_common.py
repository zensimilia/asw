import pytest

from asw import AISUP

DEFAULT_HOST = "http://localhost"
DEFAULT_TOKEN = "t0ken"
DEFAULT_TIMEOUT = 10


@pytest.fixture
def aisup() -> AISUP:
    return AISUP(DEFAULT_HOST, DEFAULT_TOKEN, DEFAULT_TIMEOUT)


def test_class_init_value_error():
    with pytest.raises(ValueError, match="empty"):
        _test = AISUP("", DEFAULT_TOKEN)
    with pytest.raises(ValueError, match="empty"):
        _test = AISUP(DEFAULT_HOST, "")


def test_class_init(aisup: AISUP):
    # verify host
    assert aisup.host == DEFAULT_HOST
    # verify token
    assert aisup.token == DEFAULT_TOKEN
    # verify timeout
    assert aisup.timeout == DEFAULT_TIMEOUT


def test_endpoint_url(aisup: AISUP):
    url = aisup._endpoint_url("endpoint")
    # verify endpount URL
    assert url == f"{DEFAULT_HOST}/endpoint"


def test_auth_headers(aisup: AISUP):
    headers = aisup._auth_headers()
    # verify authorization header
    assert "Authorization" in headers
    # verify include token to header
    assert headers.get("Authorization") == f"Bearer {DEFAULT_TOKEN}"
    # verify content-type header
    assert "Content-Type" in headers
