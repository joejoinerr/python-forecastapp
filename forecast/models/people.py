from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import forecast


class Person:
    def __init__(self,
                 _forecast: 'forecast.ForecastClient',
                 raw: dict):
        self._forecast = _forecast
        self.raw = raw
