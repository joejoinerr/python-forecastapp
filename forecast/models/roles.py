import datetime
from typing import TYPE_CHECKING, Any, Dict, Optional

from ..const import API_PATH
from .base import ForecastBase

if TYPE_CHECKING:
    import forecast


class Role(ForecastBase, object):
    def __init__(self,
                 _forecast: 'forecast.ForecastClient',
                 _id: int,
                 raw: Optional[Dict[str, Any]] = None):
        self._forecast = _forecast
        self._id = _id
        self.raw = raw

    def __getattribute__(self, item):
        # Lazy load the JSON response so that we can create a Role without it
        if item == 'raw' and not object.__getattribute__(self, 'raw'):
            path = API_PATH['role_id'].format(id=object.__getattribute__(self, '_id'))
            self.raw = object.__getattribute__(self, '_forecast').request(path)
        return object.__getattribute__(self, item)

    @property
    def name(self) -> str:
        return self.raw['name']

    def __repr__(self):
        if object.__getattribute__(self, 'raw'):
            return f'<forecast.Role(id=\'{self.id}\', name=\'{self.name}\')>'
        else:
            return f'<forecast.Role(id=\'{self.id}\')>'
