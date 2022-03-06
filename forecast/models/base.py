import datetime
from typing import TYPE_CHECKING, Any, Dict, Optional

if TYPE_CHECKING:
    import forecast


class ForecastBase:
    def __init__(self,
                 _forecast: 'forecast.ForecastClient',
                 _id: int,
                 raw: Optional[Dict[str, Any]] = None):
        self._forecast = _forecast
        self._id = _id
        self.raw = raw
        self.path = None  # Must be set by children

    def __getattribute__(self, item):
        """ Lazy loads the API response"""
        if item == 'raw' and not object.__getattribute__(self, 'raw'):
            self.raw = object.__getattribute__(self, '_forecast')\
                .request(self.path)
        return object.__getattribute__(self, item)

    @property
    def id(self) -> int:
        return self._id

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
