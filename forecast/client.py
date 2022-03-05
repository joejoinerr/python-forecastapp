from typing import Any, Dict, Literal, Optional

import requests

import forecast.models
from .exceptions import ForecastAPIError


class ForecastClient:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self._session = requests.Session()

        # Interface for interacting with people, including creating new people.
        # To get an individual person, use `ForecastClient.person()`
        self.people = forecast.models.PeopleHelper(self)

        # Interface frore interacting with tasks
        self.tasks = forecast.models.TasksHelper(self)

        # Interface frore interacting with projects
        self.projects = forecast.models.ProjectsHelper(self)

        # Interface for interacting with roles
        self.roles = forecast.models.RolesHelper(self)

        # Interface for interacting with labels
        self.labels = forecast.models.LabelsHelper(self)

        # Interface for interacting with NPT
        self.non_project_time = forecast.models.NPTHelper(self)

    def request(self,
                path: str,
                request_type: Literal['GET', 'POST', 'PUT', 'DELETE'] = 'GET',
                params: Optional[Dict[str, Any]] = None,
                headers: Optional[Dict[str, str]] = None,
                data: Optional[Dict[str, Any]] = None) -> dict:
        request_type = request_type.upper()

        final_headers = {
            'x-forecast-api-key': self.api_key,
        }
        if isinstance(headers, dict):
            final_headers.update(headers)

        req = requests.Request(request_type,
                               f'https://api.forecast.it/api{path}',
                               params=params,
                               headers=final_headers,
                               json=data)
        prepped = self._session.prepare_request(req)

        res = self._session.send(prepped)
        json = res.json()
        try:
            res.raise_for_status()
        except requests.exceptions.HTTPError as e:
            message = json.get('message')
            raise ForecastAPIError(f'Forecast API responded with status '
                                   f'{res.status_code}: {message}') from e

        return json
