import statsd
import logging


class MetricsCollectorCreator:
    @staticmethod
    def forTest():
        return NoMetricsCollector

    @staticmethod
    def forProd():
        return StatsdMetricsCollector


class NoMetricsCollector:
    @staticmethod
    def create_collector(config):
        return NoMetricsCollector()
        
    def __init__(self):
        pass

    def collect_event(self, event):
        pass


class StatsdMetricsCollector:
    @staticmethod
    def create_collector(config):
        return StatsdMetricsCollector(config.METRICS_HOST, config.METRICS_PORT)
        
    def __init__(self, metrics_host, metrics_port):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.metrics_host = metrics_host
        self.metrics_port = metrics_port
        self._collector = None

    @property
    def collector(self):
        if self._collector is None:
            try:
                self._collector = statsd.StatsClient(self.metrics_host, self.metrics_port)
            except Exception as e:
                self.logger.warning('Error connecting to metrics host \'{}\': {}'.format(self.metrics_host, str(e)))
        return self._collector

    def collect_event(self, event):
        self.collector and self.collector.incr(event)
