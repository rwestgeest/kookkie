from app.adapters.metrics import StatsdMetricsCollector
from support.log_collector import log_collector
from support.probe import probe_that
from hamcrest import assert_that, equal_to
import socket
from threading import Thread, Condition
import pytest


class xTestStatsdMetricsCollector:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.statsd_server = StatsDRecorder(8126)
        self.statsd_server.start()
        yield
        self.statsd_server.stop()

    # if this test is still flaky,
    #   it is due to the nature of udp.
    #   and the test should send a few events and see if any one arrives
    def test_sends_metrics_to_statsd(self):
        collector = StatsdMetricsCollector('localhost', 8126)

        def send_and_check():
            collector.collect_event('test')
            assert_that(self.statsd_server.received_data, equal_to(b'test:1|c'))
        probe_that(send_and_check, timeout=1500)

    def xtest_can_handle_invalid_hostnames(self, log_collector):
        collector = StatsdMetricsCollector('invalidhostname', 8126)
        collector.collect_event('test')
        log_collector.assert_warning('Error connecting to metrics host \'invalidhostname\'')

    def test_does_not_fail_when_metrics_host_not_available(self):
        collector = StatsdMetricsCollector('localhost', 8126)
        collector.collect_event('test')


class StatsDRecorder:
    def __init__(self, port):
        self.port = port
        self._running = Condition()

    def start(self):
        self.go_on = True
        self.received_data = ''
        self.thread = Thread(target=self.receive_packages)
        self.thread.start()
        with self._running:
            self._running.wait()

    def receive_packages(self):
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket.bind(('localhost', self.port))
        self.socket.settimeout(.1)
        with self._running:
            self._running.notify_all()
        while self.go_on:
            try:
                self.received_data, _ = self.socket.recvfrom(1024)
            except:
                pass
        self.socket.close()

    def stop(self):
        self.go_on = False
        self.thread.join()
