from typing import TYPE_CHECKING

from ..const import API_PATH
from .people import Person

if TYPE_CHECKING:
    import forecast


class PeopleHelper:
    def __init__(self, _forecast: 'forecast.ForecastClient'):
        self._forecast = _forecast

    def __call__(self, *args, **kwargs):
        raw = self._forecast.request(API_PATH['persons'])
        for raw_person in raw:
            yield Person(self._forecast, raw_person)
