import datetime
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Optional
)

from ..const import API_PATH

if TYPE_CHECKING:
    import forecast


class Task(object):
    def __init__(self,
                 _forecast: 'forecast.ForecastClient',
                 _id: int,
                 raw: Optional[Dict[str, Any]] = None):
        self._forecast = _forecast
        self._id = _id
        self.raw = raw

    def __getattribute__(self, item):
        """Lazy load the JSON response"""
        if item == 'raw' and not object.__getattribute__(self, 'raw'):
            path = API_PATH['task'].format(id=object.__getattribute__(self, '_id'))
            self.raw = object.__getattribute__(self, '_forecast').request(path)
        return object.__getattribute__(self, item)

    @property
    def id(self):
        return self._id

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
    def phase(self) -> Optional[int]:
        return self.raw.get('milestone')

    @property
    def assigned(self) -> Optional[List[int]]:
        return self.raw.get('assigned_persons')

    @property
    def labels(self) -> Optional[List[int]]:
        return self.raw.get('labels')

    @property
    def owner_id(self) -> int:
        return self.raw['owner_id']

    @property
    def created_by(self) -> int:
        return self.raw['created_by']

    @property
    def updated_by(self) -> int:
        return self.raw['updated_by']

    @property
    def created_at(self) -> 'datetime.datetime':
        return datetime.datetime.fromisoformat(self.raw['created_at'])

    @property
    def updated_at(self) -> 'datetime.datetime':
        return datetime.datetime.fromisoformat(self.raw['updated_at'])
