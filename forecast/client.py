from typing import Optional

import requests

from . import models
from .exceptions import ForecastAPIError


class ForecastClient:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self._session = requests.Session()

        # Interface for interacting with people, including creating new people.
        # To get an individual person, use `ForecastClient.person()`
        self.people = models.PeopleHelper(self)

        # Interface frore interacting with tasks
        self.tasks = models.TasksHelper(self)

    def request(self,
                path: str,
                request_type: Optional[str] = 'GET',
                params: Optional[dict] = None,
                headers: Optional[dict] = None,
                data: Optional[dict] = None) -> dict:
        if not isinstance(request_type, str):
            raise TypeError('`request_type` should be string.')
        request_type = request_type.upper()
        valid_types = {'GET', 'POST', 'PUT', 'DELETE'}
        if request_type not in valid_types:
            raise ValueError(f'`request_type` should be one of: {", ".join(valid_types)}.')

        final_headers = {
            'x-forecast-api-key': self.api_key,
        }
        if isinstance(headers, dict):
            final_headers.update(headers)

        req = requests.Request(request_type, f'https://api.forecast.it/api{path}',
                               params=params,
                               headers=final_headers,
                               data=data)
        prepped = self._session.prepare_request(req)

        res = self._session.send(prepped)
        json = res.json()
        try:
            res.raise_for_status()
        except requests.exceptions.HTTPError as e:
            message = json.get('message')
            raise ForecastAPIError(f'Forecast API responded with status {res.status_code}: {message}') from e

        return json
