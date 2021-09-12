import datetime


class ForecastBase:
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
