import datetime
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Optional
)

from ..const import API_PATH
import forecast.models
from forecast.models.base import ForecastBase

if TYPE_CHECKING:
    import forecast


class Task(ForecastBase, object):
    def __init__(self,
                 _forecast: 'forecast.ForecastClient',
                 _id: int,
                 raw: Optional[Dict[str, Any]] = None):
        self._forecast = _forecast
        self._id = _id
        self.raw = raw

    def __getattribute__(self, item):
        # Lazy load the JSON response so that we can create a Task without it
        if item == 'raw' and not object.__getattribute__(self, 'raw'):
            path = API_PATH['task_id'].format(id=object.__getattribute__(self, '_id'))
            self.raw = object.__getattribute__(self, '_forecast').request(path)
        return object.__getattribute__(self, item)

    @property
    def company_task_id(self) -> int:
        return int(self.raw['company_task_id'])

    @property
    def title(self) -> Optional[str]:
        return self.raw.get('title')

    @property
    def description(self) -> Optional[str]:
        return self.raw.get('description')

    @property
    def project_id(self) -> int:
        return int(self.raw['project_id'])

    @property
    def estimate(self) -> Optional[float]:
        high_estimate = self.raw.get('high_estimate')
        general_estimate = self.raw.get('forecast')

        if general_estimate:
            return float(general_estimate)
        elif high_estimate:
            return float(high_estimate)
        else:
            return None

    @property
    def remaining(self) -> Optional[float]:
        remaining = self.raw.get('remaining')
        if remaining:
            return float(remaining)
        else:
            return None

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
    def bug(self) -> bool:
        return self.raw['bug']

    @property
    def non_billable(self) -> bool:
        return self.raw['un_billable']

    @property
    def blocked(self) -> bool:
        return self.raw['blocked']

    @property
    def high_priority(self) -> bool:
        return self.raw['high_priority']

    @property
    def workflow_column(self) -> Optional[int]:
        return self.raw.get('workflow_column')

    @property
    def phase(self) -> Optional['forecast.models.Phase']:
        phase = self.raw.get('milestone')
        if phase:
            return forecast.models.Phase(self._forecast, phase, self.project_id)

    @property
    def assigned(self) -> Optional[List['forecast.models.Person']]:
        assigned = self.raw.get('assigned_persons')
        if assigned:
            return [forecast.models.Person(self._forecast, person)
                    for person in assigned]
        else:
            return None

    @property
    def labels(self) -> Optional[List[int]]:
        return self.raw.get('labels')

    @property
    def owner(self) -> Optional['forecast.models.Person']:
        owner = self.raw.get('owner_id')
        if owner:
            return forecast.models.Person(self._forecast, owner)
        else:
            return None

    def __repr__(self):
        if object.__getattribute__(self, 'raw'):
            return f'<forecast.Task(id=\'{self.id}\', title=\'{self.title}\')>'
        else:
            return f'<forecast.Task(id=\'{self.id}\')>'
