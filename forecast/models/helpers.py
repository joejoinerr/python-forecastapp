import datetime
from typing import TYPE_CHECKING, Iterable, Union

from ..const import API_PATH
from . import Person, Task, Project

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

    def create(self,
               project_id: int,
               **kwargs) -> 'forecast.models.Task':
        if not isinstance(project_id, int):
            raise ValueError('`project_id` should be an integer.')

        valid = {
            'title',
            'description',
            'role',
            'estimate',
            'approved',
            'start_date',
            'end_date',
            'bug',
            'non_billable',
            'blocked',
            'sprint',
            'workflow_column',
            'phase',
            'assigned',
            'labels',
            'owner_id',
        }

        new_task = {k: v for k, v in kwargs.items() if k in valid}
        new_task['project_id'] = project_id

        if 'estimate' in new_task.keys():
            for estimate in ['high_estimate', 'low_estimate']:
                new_task[estimate] = new_task['estimate']
            del new_task['estimate']

        if 'non_billable' in new_task.keys():
            new_task['un_billable'] = new_task.pop('non_billable')

        if 'assigned' in new_task.keys():
            new_task['assigned_persons'] = new_task.pop('assigned')

        if 'phase' in new_task.keys():
            new_task['milestone'] = new_task.pop('phase')

        created_task = self._forecast.request(API_PATH['tasks'],
                                              request_type='POST',
                                              data=new_task)

        return Task(self._forecast, created_task['id'], created_task)


class PeopleHelper:
    def __init__(self, _forecast: 'forecast.ForecastClient'):
        self._forecast = _forecast

    def __call__(self, *args, **kwargs) -> Iterable['forecast.models.Person']:
        raw = self._forecast.request(API_PATH['persons'])
        for raw_person in raw:
            yield Person(self._forecast, raw_person['id'], raw_person)

    def from_id(self, id_: int) -> 'forecast.models.Person':
        return Person(self._forecast, id_)


class ProjectsHelper:
    def __init__(self, _forecast: 'forecast.ForecastClient'):
        self._forecast = _forecast

    def __call__(self, *args, **kwargs) -> Iterable['forecast.models.Project']:
        raw = self._forecast.request(API_PATH['projects'])
        for raw_project in raw:
            yield Project(self._forecast, raw_project['id'], raw_project)

    def from_id(self, id_: int) -> 'forecast.models.Project':
        return Project(self._forecast, id_)

    def from_company_id(self, company_id: int) -> 'forecast.models.Project':
        raw_project = self._forecast.request(API_PATH['project_company_id'].format(id=company_id))
        return Project(self._forecast, raw_project['id'], raw_project)
