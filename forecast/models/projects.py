import datetime
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Iterable,
    List,
    Optional,
    Union
)

from ..const import API_PATH
from .base import ForecastBase

if TYPE_CHECKING:
    import forecast


class Project(ForecastBase, object):
    def __init__(self,
                 _forecast: 'forecast.ForecastClient',
                 _id: int,
                 raw: Optional[Dict[str, Any]] = None):
        self._forecast = _forecast
        self._id = _id
        self.raw = raw

    def __getattribute__(self, item):
        # Lazy load the JSON response so that we can create a Project without it
        if item == 'raw' and not object.__getattribute__(self, 'raw'):
            path = API_PATH['project_id'].format(id=object.__getattribute__(self, '_id'))
            self.raw = object.__getattribute__(self, '_forecast').request(path)
        return object.__getattribute__(self, item)

    @property
    def company_project_id(self) -> int:
        return int(self.raw['company_project_id'])

    @property
    def name(self) -> str:
        return self.raw['name']

    @property
    def connected_project(self) -> Optional['forecast.models.Project']:
        connected_project = self.raw.get('connected_project')
        if connected_project:
            return Project(self._forecast, connected_project)
        else:
            return None

    @property
    def stage(self) -> str:
        return self.raw['stage']

    @property
    def status(self) -> Optional[str]:
        return self.raw.get('status')

    @property
    def status_description(self) -> Optional[str]:
        return self.raw.get('status_description')

    @property
    def description(self) -> Optional[str]:
        return self.raw.get('description')

    @property
    def color(self) -> Optional[str]:
        return self.raw.get('color')

    @property
    def estimation_units(self) -> Optional[str]:
        return self.raw.get('estimation_units')

    @property
    def minutes_per_estimation_point(self) -> Optional[int]:
        return self.raw.get('minutes_per_estimation_point')

    @property
    def budget(self) -> Optional[float]:
        return self.raw.get('budget')

    @property
    def budget_type(self) -> Optional[str]:
        return self.raw.get('budget_type')

    @property
    def use_sprints(self) -> bool:
        return self.raw['use_sprints']

    @property
    def sprint_length(self) -> Optional[int]:
        return self.raw.get('sprint_length')

    @property
    def start_date(self) -> Optional['datetime.date']:
        start_date = self.raw.get('start_date')
        if start_date:
            return datetime.date.fromisoformat(start_date)
        else:
            return None

    @property
    def end_date(self) -> Optional['datetime.date']:
        end_date = self.raw.get('end_date')
        if end_date:
            return datetime.date.fromisoformat(end_date)
        else:
            return None

    @property
    def task_levels(self) -> int:
        return self.raw['task_levels']

    @property
    def client(self) -> int:
        return self.raw['client']

    @property
    def rate_card(self) -> int:
        return self.raw['rate_card']

    @property
    def remaining_auto_calculated(self) -> bool:
        return self.raw['remaining_auto_calculated']

    @property
    def use_project_allocations(self) -> bool:
        return self.raw['use_project_allocations']

    @property
    def use_baseline(self) -> bool:
        return self.raw['use_baseline']

    @property
    def baseline_win_chance(self) -> float:
        return self.raw['baseline_win_chance']

    @property
    def baseline_target(self) -> float:
        return self.raw['baseline_target']

    @property
    def labels(self) -> Optional[List[int]]:
        return self.raw.get('labels')

    @property
    def external_refs(self) -> Optional[List]:
        return self.raw.get('external_refs')

    def phases(self, phase_id: Optional[int] = None) -> Union['forecast.models.Phase',
                                                              List['forecast.models.Phase'],
                                                              None]:
        if isinstance(phase_id, int):
            return Phase(self._forecast, phase_id, self.id)
        else:
            all_phases = self._forecast.request(API_PATH['milestones']
                                                .format(project_id=self.id))
            if all_phases:
                return [Phase(self._forecast, raw_phase['id'], self.id, raw=raw_phase)
                        for raw_phase in all_phases]
            else:
                return None

    def __repr__(self):
        if object.__getattribute__(self, 'raw'):
            return f'<forecast.Project(id=\'{self.id}\', name=\'{self.name}\')>'
        else:
            return f'<forecast.Project(id=\'{self.id}\')>'


class Phase(ForecastBase, object):
    def __init__(self,
                 _forecast: 'forecast.ForecastClient',
                 _id: int,
                 _project_id: int,
                 raw: Optional[Dict[str, Any]] = None):
        self._forecast = _forecast
        self._id = _id
        self._project_id = _project_id
        self.raw = raw

    def __getattribute__(self, item):
        # Lazy load the JSON response so that we can create a Phase without it
        if item == 'raw' and not object.__getattribute__(self, 'raw'):
            path = API_PATH['milestone_id'].format(project_id=object.__getattribute__(self, '_project_id'),
                                                   milestone_id=object.__getattribute__(self, '_id'))
            self.raw = object.__getattribute__(self, '_forecast').request(path)
        return object.__getattribute__(self, item)

    @property
    def project_id(self) -> int:
        return self._project_id

    @property
    def name(self) -> str:
        return self.raw['name']

    @property
    def start_date(self) -> Optional['datetime.date']:
        start_date = self.raw.get('start_date')
        if start_date:
            return datetime.date.fromisoformat(start_date)
        else:
            return None

    @property
    def end_date(self) -> Optional['datetime.date']:
        end_date = self.raw.get('end_date')
        if end_date:
            return datetime.date.fromisoformat(end_date)
        else:
            return None

    def __repr__(self):
        if object.__getattribute__(self, 'raw'):
            return f'<forecast.Phase(id=\'{self.id}\', ' \
                   f'project_id=\'{self.project_id}\', ' \
                   f'name=\'{self.name}\')>'
        else:
            return f'<forecast.Phase(id=\'{self.id}\', project_id=\'{self.project_id}\')>'
