"""Aisup Service Wrapper core module."""

import base64
import hashlib
import pathlib
import tempfile
import urllib.parse
from http import HTTPMethod, HTTPStatus

import requests

from . import exceptions


class AISUP:
    """Aisup Service Wrapper class."""

    DOWNLOAD_ENDPOINT = "api/system/getFileStream"
    DOWNLOAD_CHUNK_SIZE = None

    token: str
    host: str
    timeout: int

    def __init__(self, host: str, token: str, timeout: int = 5) -> None:
        """Initialize class member.

        :param str host: A full hostname with its scheme
        :param str token: The auth token
        :param int, optional timeout: Request timeout in sec. Default to 5
        """
        if any(not item.strip() for item in [host, token]):
            msg = "Some of the required arguments are empty"
            raise ValueError(msg)
        self.host = host
        self.token = token
        self.timeout = timeout

    def _endpoint_url(self, endpoint: str) -> str:
        """Return full endpoint URL.

        :param str endpoint: Endpoint path
        :return str: Full URL with scheme, host and path
        """
        return urllib.parse.urljoin(self.host, endpoint)

    def _auth_headers(self) -> dict[str, str]:
        """Return HTTP headers with authorization token.

        :return dict: Dict with prepared authorization headers
        """
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    @staticmethod
    def _get_digest(digest_header: str | None) -> str:
        """Return parsed _digest_ value from header.

        :param str, optional digest_header: A digest header of the response
        :return str: Hash value from digest header
        """
        if digest_header is None:
            return ""
        return digest_header.split(",", maxsplit=1)[0][8:]

    def _send_request(
        self,
        method: HTTPMethod,
        endpoint: str,
        *,
        data: dict | None = None,
        **kwargs,
    ) -> requests.Response:
        """Send data to the service endpoint with authorization.

        :param HTTPMethod method: Request method
        :param str endpoint: Endpoint path
        :param dict, optional data: JSON data passed with the request
        :param **kwargs: Extra keyword arguments to passed to `request` method
        :return Response: Response object
        :raise AisupError, UnauthorizedError, HTTPError, NetworkError: If any error occured
        """
        url = self._endpoint_url(endpoint)

        try:
            response = requests.request(
                method.value,
                url,
                json=data,
                headers=self._auth_headers(),
                timeout=self.timeout,
                **kwargs,
            )
            response.raise_for_status()
        except ValueError as err:
            msg = f"Invalid request: {err}"
            raise exceptions.AisupError(msg) from err
        except requests.exceptions.HTTPError as err:
            if err.response.status_code == HTTPStatus.UNAUTHORIZED:
                raise exceptions.UnauthorizedError from err
            msg = f"AISUP responses with status {err.response.status_code}: {err.strerror}"
            raise exceptions.HTTPError(msg) from err
        except requests.exceptions.RequestException as err:
            msg = f"Network error: {err.strerror}"
            raise exceptions.NetworkError(msg) from err

        return response

    def download(
        self,
        guid: str,
        *,
        path: str | None = None,
        name: str | None = None,
        endpoint: str | None = None,
        data: dict | None = None,
    ) -> str:
        """Download the file by guid to the temporary directory (if _path_ is not specified)
        and returns its filename with full path.

        :param str guid: ID of the requested file
        :param str, optional path: Desired path for download to. Temp directory if `None`
        :param str, optional name: Desired filename (without extension) or guid if `None`
        :param str, optional endpoint: To override default download endpiont
        :param dict, optional data: Extra data to override request json
        :return str: Full path to downloaded file
        :raise RequestException, NetworkError, FileError, HashError: If request or IO error occurs
        """
        json = {"id": guid}
        if data is not None:
            json.update(data)  # override json

        response = self._send_request(HTTPMethod.POST, endpoint or self.DOWNLOAD_ENDPOINT, data=json, stream=True)

        hasher = hashlib.sha256()
        header_hash = self._get_digest(response.headers.get("digest"))
        file_suffix = pathlib.Path(response.headers["content-disposition"]).suffix
        file_name = pathlib.Path(path or tempfile.gettempdir()) / f"{name or guid}{file_suffix}"

        try:
            with pathlib.Path(file_name).open("wb+") as f:
                for chunk in response.iter_content(chunk_size=self.DOWNLOAD_CHUNK_SIZE):
                    f.write(chunk)
                    hasher.update(chunk)
                file_hash = base64.b64encode(hasher.digest()).decode()
        except requests.exceptions.RequestException as err:
            msg = f"Network error: {err}"
            raise exceptions.NetworkError(msg) from err
        except OSError as err:
            msg = f"{err.strerror}: {err.filename}"
            raise exceptions.FileError(msg) from err

        if file_hash != header_hash:
            raise exceptions.HashError(guid)

        return file_name.resolve().as_posix()

    def post(self, endpoint: str, data: dict | None = None, **kwargs) -> dict:
        """Send POST request to the service with optional data and return response as parsed json.

        :param str endpoint: Endpoint path
        :param dict, optional data: Data in dictionary
        :param **kwargs: Extra keyword arguments to passed to _requests_ method
        :return dict: Decoded json response.
        :raise JSONDecodeError: If the response is not in json format
        """
        try:
            return self._send_request(HTTPMethod.POST, endpoint, data=data, **kwargs).json()
        except requests.exceptions.JSONDecodeError as err:
            raise exceptions.JSONDecodeError from err

    def get(self, endpoint: str, **kwargs) -> dict:
        """Send GET request to the service and return response as parsed json.

        :param str endpoint: Endpoint path
        :param **kwargs: Extra keyword arguments to passed to _requests_ method
        :return dict: Decoded json response.
        :raise JSONDecodeError: If the response is not in json format
        """
        try:
            return self._send_request(HTTPMethod.GET, endpoint, **kwargs).json()
        except requests.exceptions.JSONDecodeError as err:
            raise exceptions.JSONDecodeError from err
