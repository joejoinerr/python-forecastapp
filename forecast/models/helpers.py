import datetime
from typing import TYPE_CHECKING, List, Optional, Union

from ..const import API_PATH
import forecast.models

if TYPE_CHECKING:
    import forecast


class TasksHelper:
    def __init__(self, _forecast: 'forecast.ForecastClient'):
        self._forecast = _forecast

    def __call__(self,
                 *args,
                 task_id: Optional[int] = None,
                 company_id: Optional[int] = None,
                 updated_after: Union[str, 'datetime.datetime', None] = None,
                 **kwargs) -> Union[List['forecast.models.Task'],
                                    'forecast.models.Task',
                                    None]:
        if isinstance(task_id, int):
            return forecast.models.Task(self._forecast, task_id)
        elif isinstance(company_id, int):
            raw_task = self._forecast.request(API_PATH['task_company_id'].format(id=company_id))
            return forecast.models.Task(self._forecast, raw_task['id'], raw_task)
        else:
            params = None
            if updated_after:
                if isinstance(updated_after, str):
                    updated_after = datetime.datetime.fromisoformat(updated_after)
                params = {
                    'updated_after': updated_after.strftime('%Y%m%dT%H%M%S')
                }
            raw = self._forecast.request(API_PATH['tasks'], params=params)
            if raw:
                return [forecast.models.Task(self._forecast, raw_task['id'], raw_task) for raw_task in raw]
            else:
                return None

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

        return forecast.models.Task(self._forecast, created_task['id'], created_task)


class PeopleHelper:
    def __init__(self, _forecast: 'forecast.ForecastClient'):
        self._forecast = _forecast

    def __call__(self,
                 *args,
                 person_id: Optional[int] = None,
                 **kwargs) -> Union[List['forecast.models.Person'],
                                    'forecast.models.Person',
                                    None]:
        if isinstance(person_id, int):
            return forecast.models.Person(self._forecast, person_id)
        else:
            raw = self._forecast.request(API_PATH['persons'])
            if raw:
                return [forecast.models.Person(self._forecast, raw_person['id'], raw_person)
                        for raw_person in raw]
            else:
                return None


class ProjectsHelper:
    def __init__(self, _forecast: 'forecast.ForecastClient'):
        self._forecast = _forecast

    def __call__(self,
                 *args,
                 project_id: Optional[int] = None,
                 company_id: Optional[int] = None,
                 **kwargs) -> Union[List['forecast.models.Project'],
                                    'forecast.models.Project',
                                    None]:
        if isinstance(project_id, int) and isinstance(company_id, int):
            raise ValueError('Only one of `project_id` or `company_id` should be supplied.')

        if isinstance(project_id, int):
            return forecast.models.Project(self._forecast, project_id)
        elif isinstance(company_id, int):
            raw_project = self._forecast.request(API_PATH['project_company_id'].format(id=company_id))
            return forecast.models.Project(self._forecast, raw_project['id'], raw_project)
        else:
            raw = self._forecast.request(API_PATH['projects'])
            if raw:
                return [forecast.models.Project(self._forecast, raw_project['id'], raw_project)
                        for raw_project in raw]
            else:
                return None


class NPTHelper:
    def __init__(self, _forecast: 'forecast.ForecastClient'):
        self._forecast = _forecast

    def __call__(self,
                 npt_id: Optional[int] = None,
                 *args,
                 **kwargs) -> Union[List['forecast.models.NonProjectTime'],
                                    'forecast.models.NonProjectTime',
                                    None]:
        if isinstance(npt_id, int):
            return forecast.models.NonProjectTime(self._forecast, npt_id)
        else:
            raw = self._forecast.request(API_PATH['non_project_time'])
            if raw:
                return [forecast.models.NonProjectTime(self._forecast, raw_npt['id'], raw_npt)
                        for raw_npt in raw]
            else:
                return None


class RolesHelper:
    def __init__(self, _forecast: 'forecast.ForecastClient'):
        self._forecast = _forecast

    def __call__(self,
                 role_id: Optional[int] = None,
                 *args,
                 **kwargs) -> Union[List['forecast.models.Role'],
                                    'forecast.models.Role',
                                    None]:
        if isinstance(role_id, int):
            return forecast.models.Role(self._forecast, role_id)
        else:
            raw = self._forecast.request(API_PATH['roles'])
            if raw:
                return [forecast.models.Role(self._forecast, raw_role['id'], raw_role)
                        for raw_role in raw]
            else:
                return None

    def create(self,
               name: str,
               *args,
               **kwargs) -> 'forecast.models.Role':
        created_role = self._forecast.request(API_PATH['roles'],
                                              request_type='POST',
                                              data={'name': name})
        return forecast.models.Role(self._forecast, created_role['id'], created_role)


class LabelsHelper:
    def __init__(self, _forecast: 'forecast.ForecastClient'):
        self._forecast = _forecast

    def __call__(self,
                 label_id: Optional[int] = None,
                 *args,
                 **kwargs) -> Union[List['forecast.models.Label'],
                                    'forecast.models.Label',
                                    None]:
        if isinstance(label_id, int):
            return forecast.models.Label(self._forecast, label_id)
        else:
            raw = self._forecast.request(API_PATH['labels'])
            if raw:
                return [forecast.models.Label(self._forecast, raw_label['id'], raw_label)
                        for raw_label in raw]
            else:
                return None

    def create(self,
               name: str,
               color: Optional[str],
               *args,
               **kwargs) -> 'forecast.models.Label':
        label_data = {
            'name': name,
            'color': color,
        }
        created_label = self._forecast.request(API_PATH['labels'],
                                               request_type='POST',
                                               data=label_data)
        return forecast.models.Label(self._forecast, created_label['id'], created_label)


class WorkflowHelper:
    def __init__(self,
                 _forecast: 'forecast.ForecastClient',
                 _project_id: int):
        self._forecast = _forecast
        self._project_id = _project_id

    def __call__(self,
                 column_id: Optional[int] = None,
                 *args,
                 **kwargs) -> Union[List['forecast.models.WorkflowColumn'],
                                    'forecast.models.WorkflowColumn',
                                    None]:
        if isinstance(column_id, int):
            return forecast.models.WorkflowColumn(self._forecast, column_id, self._project_id)
        else:
            raw = self._forecast.request(API_PATH['workflow'].format(project_id=self._project_id))
            if raw:
                return [forecast.models.WorkflowColumn(self._forecast, raw_column['id'], self._project_id, raw_column)
                        for raw_column in raw]
            else:
                return None

    def create(self,
               name: str,
               category: Optional[str] = 'TODO',
               sort_order: Optional[int] = None):
        column_data = {
            'name': name,
            'category': category,
        }
        if isinstance(sort_order, int):
            column_data.update({'sort_order': sort_order})

        api_path = API_PATH['workflow'].format(project_id=self._project_id)
        created_column = self._forecast.request(api_path,
                                                request_type='POST',
                                                data=column_data)
        return forecast.models.WorkflowColumn(self._forecast,
                                              created_column['id'],
                                              self._project_id,
                                              created_column)
