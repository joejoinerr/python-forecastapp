from typing import Optional

import requests

from .exceptions import ForecastAPIError


class ForecastClient:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self._session = requests.Session()

    def _request(self,
                 url: str,
                 type_: Optional[str] = 'GET',
                 headers: Optional[dict] = None,
                 data: Optional[dict] = None) -> 'requests.Response':
        type_ = type_.upper()
        valid_types = {'GET', 'POST', 'PUT', 'DELETE'}
        if type_ not in valid_types:
            raise ValueError(f'`type_` should be one of: {", ".join(valid_types)}')

        final_headers = {
            'x-forecast-api-key': self.api_key,
        }
        if isinstance(headers, dict):
            final_headers.update(headers)

        req = requests.Request(type_, url, headers=final_headers, data=data)
        prepped = self._session.prepare_request(req)

        res = self._session.send(prepped)
        json = res.json()
        try:
            res.raise_for_status()
        except requests.exceptions.HTTPError as e:
            message = json['message']
            raise ForecastAPIError(f'Forecast API responded with status {res.status_code}: {message}') from e

        return res
