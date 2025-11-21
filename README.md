# Aisup Service Wrapper

A simple and clear tool-class for work with Aisup VKB API.

## Development

- Clone: `git clone https://github.com/zensimilia/asw.git`
- Install dependencies: `uv sync`
- Run tests: `uv pytest -v`
- Build package: `uv build`

## Basic usage

Install from this repo with `PIP` or your favorite package manager.

```console
pip install git+https://github.com/zensimilia/asw.git
```

Create class member with `host` and authorization`token` params. Now you can send GET or POST request
to the service endpoints and download files. Example:

```python
from asw import AISUP

aisup = AISUP("https://example.host:8000", "t0p_5ecret_t0ken")

get_response = aisup.get("api/endpoint/get")
print(get_response)
# {result:"ok"}

post_data = {"lorem": "ipsum"}
post_response = aisup.post("api/endpoint/post", post_data)
print(post_response)
# {dolor: "sit amet", ...}

file = aisup.download("GUID-OF-FILE", path="./downloads")
print(file)
# /app/downloads/GUID-OF-FILE.jpg
```

## Reference

### _class_ asw.**AISUP** (host, token, timeout = 5)

Initialize class member.

- :param str host: A full hostname with its scheme
- :param str token: The auth token
- :param int, optional timeout: Request timeout in sec. Default to 5

### _method_ AISUP.**get** (endpoint, **kwargs)

Send GET request to the service and return response as parsed json.

- :param str endpoint: Endpoint path
- :param **kwargs: Extra keyword arguments to passed to _requests_ method
- :return dict: Decoded json response.
- :raise JSONDecodeError: If the response is not in json format

### _method_ AISUP.**post** (endpoint, data = None, **kwargs)

Send POST request to the service with optional data and return response as parsed json.

- :param str endpoint: Endpoint path
- :param dict, optional data: Data in dictionary
- :param **kwargs: Extra keyword arguments to passed to _requests_ method
- :return dict: Decoded json response.
- :raise JSONDecodeError: If the response is not in json format

### _method_ AISUP.**download** (guid, path = None, name = None, endpoint = None, data = None)

Download the file by guid to the temporary directory (if _path_ is not specified)
and returns its filename with full path.

- :param str guid: ID of the requested file
- :param str, optional path: Desired path for download to. Temp directory if `None`
- :param str, optional name: Desired filename (without extension) or guid if `None`
- :param str, optional endpoint: To override default download endpiont
- :param dict, optional data: Extra data to override request json
- :return str: Full path to downloaded file
- :raise RequestException, NetworkError, FileError, HashError: If request or IO error occurs

## License

Aisup Service Wrapper is released under the MIT License. See the [LICENSE](LICENSE) file for more details.
