# Aisup Service Wrapper

A tool class for work with its API.

- dev: `uv sync`
- build: `uv build`
- tests: `uv pytest -v`

## Basic usage

Install package by you favourite package manager.

- UV

    ```bash
    uv add git+https://github.com/zensimilia/asw.git
    ```

- PIP

    ```bash
    pip install git+https://github.com/zensimilia/asw.git
    ```

Create class member with `host` and authorization`token` params. You can send GET or POST request
to the service endpoints and download files:

```python
from asw import AISUP

aisup = AISUP("https://example.host", "t0p_5ecret_t0ken")

get_response = aisup.get("api/endpoint/get")
print("JSON: ", get_response)

post_data = {"lorem": "ipsum"}
post_response = aisup.post("api/endpoint/post", post_data)
print("JSON: ", post_response)

file = aisup.download("GUID-OF-FILE", path="./downloads")
print("FULL PATH: ", file)
```

## Reference

### _class_ **AISUP** (host, token, timeout = 5)

Initialize class member.

- :param str host: A full hostname with its scheme
- :param str token: The auth token
- :param int, optional timeout: Request timeout in sec. Default to 5

### _method_ **get** (endpoint, **kwargs)

Send GET request to the service and return response as parsed json.

- :param str endpoint: Endpoint path
- :param **kwargs: Extra keyword arguments to passed to _requests_ method
- :return dict: Decoded json response.
- :raise JSONDecodeError: If the response is not in json format

### _method_ **post** (endpoint, data = None, **kwargs)

Send POST request to the service and return response as parsed json.

- :param str endpoint: Endpoint path
- :param dict, optional data: Data in dictionary
- :param **kwargs: Extra keyword arguments to passed to _requests_ method
- :return dict: Decoded json response.
- :raise JSONDecodeError: If the response is not in json format

### _method_ **download** (guid, path = None, name = None, endpoint = None, data = None)

Download file by guid and returns its full path.

- :param str guid: ID of the requested file
- :param str, optional path: Desired path for download to. Temp directory if `None`
- :param str, optional name: Desired filename (without extension) or guid if `None`
- :param str, optional endpoint: To override default download endpiont
- :param dict, optional data: Extra data to override request json
- :return str: Full path to downloaded file
- :raise RequestException, NetworkError, FileError, HashError: If request or IO error occurs
