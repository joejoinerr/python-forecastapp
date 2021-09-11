import datetime
from typing import TYPE_CHECKING, Iterable, Union

from ..const import API_PATH
from . import Person, Task

if TYPE_CHECKING:
    import forecast


class TasksHelper:
    def __init__(self, _forecast: 'forecast.ForecastClient'):
        self._forecast = _forecast

    def __call__(self,
                 *args,
                 updated_after: Union[str, 'datetime.datetime', None] = None,
                 **kwargs) -> Iterable['forecast.models.Task']:
        params = None
        if updated_after:
            if isinstance(updated_after, str):
                updated_after = datetime.datetime.fromisoformat(updated_after)
            params = {
                'updated_after': updated_after.strftime('%Y%m%dT%H%M%S')
            }
        raw = self._forecast.request(API_PATH['tasks'], params=params)
        for raw_task in raw:
            yield Task(self._forecast, raw_task['id'], raw_task)

    def from_id(self, id_: int) -> 'forecast.models.Task':
        return Task(self._forecast, id_)

    def from_company_id(self, company_id: int) -> 'forecast.models.Task':
        raw_task = self._forecast.request(API_PATH['task_company_id'].format(id=company_id))
        return Task(self._forecast, raw_task['id'], raw_task)


class PeopleHelper:
    def __init__(self, _forecast: 'forecast.ForecastClient'):
        self._forecast = _forecast

    def __call__(self, *args, **kwargs) -> Iterable['forecast.models.Person']:
        raw = self._forecast.request(API_PATH['persons'])
        for raw_person in raw:
            yield Person(self._forecast, raw_person['id'], raw_person)
            
    def from_id(self, id_: int) -> 'forecast.models.Person':
        return Person(self._forecast, id_)
