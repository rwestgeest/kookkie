from app.domain import Clock
from hamcrest import assert_that, equal_to, is_not
import time
from datetime import timezone, datetime

class TestClock_now:
    def test_now_is_not_the_same(self):
        now_now = Clock().now()
        time.sleep(0.01)
        then_now = Clock().now()
        assert_that(now_now, is_not(equal_to(then_now)))

    def test_now_is_in_utc(self):
        now = Clock().now()
        assert_that(now.tzinfo, equal_to(timezone.utc))
        
    def test_now_can_be_an_utc(self):
        now = Clock().now()
        now_without_timezone = now.replace(tzinfo = None)
        now_repaired = now_without_timezone.replace(tzinfo=timezone.utc)
        assert_that(now_repaired, equal_to(now))

class TestClock_parse_date:
    def test_returns_midnight_of_that_date(self):
        timestamp = Clock().parse_date('2020-12-10')
        assert_that(timestamp, equal_to(datetime(2020,12,10,0,0,0,0,tzinfo=timezone.utc)))

    def test_returns_none_when_date_string_is_none(self):
        assert_that(Clock().parse_date(None), equal_to(None))

    def test_returns_none_when_date_string_is_invalid(self):
        assert_that(Clock().parse_date('2020-13-42'), equal_to(None))

class TestFixedClock:
    def test_now_is_always_the_same(self):
        now_now = Clock.fixed().now()
        time.sleep(0.01)
        then_now = Clock.fixed().now()
        assert_that(now_now, equal_to(then_now))