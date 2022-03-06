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
        super(Role, self).__init__(_forecast, _id, raw)
        self.path = API_PATH['role_id'].format(
            id=object.__getattribute__(self, '_id'))

    @property
    def name(self) -> str:
        return self.raw['name']

    def __repr__(self):
        if object.__getattribute__(self, 'raw'):
            return (f'<forecast.{type(self).__name__}(id=\'{self.id}\', '
                    f'name=\'{self.name}\')>')
        else:
            return f'<forecast.{type(self).__name__}(id=\'{self.id}\')>'
