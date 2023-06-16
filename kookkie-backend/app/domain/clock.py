from datetime import datetime, timezone, date
from typing import Optional


class Clock:
    @staticmethod
    def fixed() -> 'Clock':
        return FixedClock()

    def now(self) -> datetime:
        return datetime.now(timezone.utc) 

    def today(self) -> date:
        return self.now().date()

    def parse_date(self, date_string) -> Optional[datetime]:
        try:
            return datetime.fromisoformat(date_string).replace(tzinfo=timezone.utc)
        except ValueError as e:
            return None
        except TypeError as e:
            return None


class FixedClock(Clock):
    def __init__(self, the_time=datetime.now(timezone.utc)):
        self._the_time = the_time

    def now(self) -> datetime:
        return self._the_time
