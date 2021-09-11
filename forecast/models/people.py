from typing import TYPE_CHECKING, Any, Optional, Dict

from ..const import API_PATH

if TYPE_CHECKING:
    import forecast


class Person:
    def __init__(self,
                 _forecast: 'forecast.ForecastClient',
                 _id: int,
                 raw: Optional[Dict[str, Any]] = None):
        self._forecast = _forecast
        self._id = _id
        self.raw = raw

    def __getattribute__(self, item):
        # Lazy load the JSON response so that we can create a Person without it
        if item == 'raw' and not object.__getattribute__(self, 'raw'):
            path = API_PATH['person_id'].format(id=object.__getattribute__(self, '_id'))
            self.raw = object.__getattribute__(self, '_forecast').request(path)
        return object.__getattribute__(self, item)

    @property
    def id(self) -> int:
        return self._id

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

    @property
    def created_at(self) -> str:
        return self.raw['created_at']

    @property
    def updated_at(self) -> str:
        return self.raw['updated_at']

    def __repr__(self):
        if object.__getattribute__(self, 'raw'):
            return f'<forecast.Person(id=\'{self.id}\', name=\'{self.name}\')>'
        else:
            return f'<forecast.Person(id=\'{self.id}\')>'
