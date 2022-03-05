from typing import TYPE_CHECKING, Any, Optional, Dict

from .base import ForecastBase
from ..const import API_PATH

if TYPE_CHECKING:
    import forecast


class Person(ForecastBase, object):
    def __init__(self,
                 _forecast: 'forecast.ForecastClient',
                 _id: int,
                 raw: Optional[Dict[str, Any]] = None):
        super(Person, self).__init__(_forecast, _id, raw)
        self.path = API_PATH['person_id'].format(
            id=object.__getattribute__(self, '_id'))

    @property
    def name(self) -> str:
        name_parts = [self.raw[part] for part in ('first_name', 'last_name')
                      if self.raw.get(part)]
        return ' '.join(name_parts)

    @property
    def email(self) -> Optional[str]:
        return self.raw.get('email')

    @property
    def user_type(self) -> str:
        return self.raw['user_type']

    @property
    def working_hours(self) -> Optional[Dict[str, int]]:
        days = {
            'monday',
            'tuesday',
            'wednesday',
            'thursday',
            'friday',
            'saturday',
            'sunday',
        }
        working_hours = {k: int(v) for k, v in self.raw if k in days}
        return working_hours if working_hours else None

    @property
    def active(self) -> bool:
        return self.raw['active']

    @property
    def default_role(self):
        return self.raw.get('default_role')

    @property
    def cost(self) -> Optional[float]:
        return self.raw.get('cost')

    @property
    def language(self) -> str:
        return self.raw['language']

    @property
    def start_date(self) -> Optional[str]:
        return self.raw.get('start_date')

    @property
    def end_date(self) -> Optional[str]:
        return self.raw.get('end_date')

    def __repr__(self):
        if object.__getattribute__(self, 'raw'):
            return (f'<forecast.{type(self).__name__}(id=\'{self.id}\', '
                    f'name=\'{self.name}\')>')
        else:
            return f'<forecast.{type(self).__name__}(id=\'{self.id}\')>'
