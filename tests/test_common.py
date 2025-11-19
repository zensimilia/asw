import pytest

from asw import AISUP

TEST_HOST = "http://localhost"
TEST_TOKEN = "t0ken"
TEST_TIMEOUT = 10
TEST_HASH = "sha-256=qjD/hwhgBOmehCQYcocI6bWjxUdQo5aQ7Zwq9zENjWw="


@pytest.fixture
def aisup() -> AISUP:
    return AISUP(TEST_HOST, TEST_TOKEN, TEST_TIMEOUT)


def test_class_init_value_error():
    with pytest.raises(ValueError, match="empty"):
        _test = AISUP("", TEST_TOKEN)
    with pytest.raises(ValueError, match="empty"):
        _test = AISUP(TEST_HOST, "")


def test_class_init(aisup: AISUP):
    # verify host
    assert aisup.host == TEST_HOST
    # verify token
    assert aisup.token == TEST_TOKEN
    # verify timeout
    assert aisup.timeout == TEST_TIMEOUT


def test_endpoint_url(aisup: AISUP):
    url = aisup._endpoint_url("endpoint")
    # verify endpount URL
    assert url == f"{TEST_HOST}/endpoint"


def test_auth_headers(aisup: AISUP):
    headers = aisup._auth_headers()
    # verify authorization header
    assert "Authorization" in headers
    # verify include token to header
    assert headers.get("Authorization") == f"Bearer {TEST_TOKEN}"
    # verify content-type header
    assert "Content-Type" in headers


def test_get_digest(aisup):
    test_str = f"digest: {TEST_HASH}"
    # verify with string
    assert aisup._get_digest(test_str) == TEST_HASH
    # verify with empty
    assert aisup._get_digest(None) == ""
