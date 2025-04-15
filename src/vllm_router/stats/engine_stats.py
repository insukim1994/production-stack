import threading
import time
from dataclasses import dataclass
from typing import Dict, Optional

import requests
from prometheus_client.parser import text_string_to_metric_families

from vllm_router.log import init_logger
from vllm_router.service_discovery import get_service_discovery
from vllm_router.utils import SingletonMeta

logger = init_logger(__name__)


from dataclasses import dataclass
from typing import Optional

from prometheus_client.parser import text_string_to_metric_families


@dataclass
class EngineStats:
    # vLLM Specific Metrics
    cache_config_info: Optional[float] = None
    num_requests_running: Optional[float] = None
    num_requests_waiting: Optional[float] = None
    num_requests_swapped: Optional[float] = None
    gpu_cache_usage_perc: Optional[float] = None
    cpu_cache_usage_perc: Optional[float] = None
    num_preemptions_total: Optional[float] = None
    prompt_tokens_total: Optional[float] = None
    generation_tokens_total: Optional[float] = None
    request_success_total: Optional[float] = None
    avg_prompt_throughput_toks_per_s: Optional[float] = None
    avg_generation_throughput_toks_per_s: Optional[float] = None

    # Metrics mighth not exist
    gpu_prefix_cache_hit_rate = 0.0

    @staticmethod
    def from_vllm_scrape(vllm_scrape: str) -> "EngineStats":
        # Map Prometheus metric names to dataclass attribute names
        metric_map = {
            "vllm:cache_config_info": "cache_config_info",
            "vllm:num_requests_running": "num_requests_running",
            "vllm:num_requests_waiting": "num_requests_waiting",
            "vllm:num_requests_swapped": "num_requests_swapped",
            "vllm:gpu_cache_usage_perc": "gpu_cache_usage_perc",
            "vllm:cpu_cache_usage_perc": "cpu_cache_usage_perc",
            "vllm:num_preemptions_total": "num_preemptions_total",
            "vllm:prompt_tokens_total": "prompt_tokens_total",
            "vllm:generation_tokens_total": "generation_tokens_total",
            "vllm:request_success_total": "request_success_total",
            "vllm:avg_prompt_throughput_toks_per_s": "avg_prompt_throughput_toks_per_s",
            "vllm:avg_generation_throughput_toks_per_s": "avg_generation_throughput_toks_per_s",
        }

        stats = EngineStats()
        for family in text_string_to_metric_families(vllm_scrape):
            if family.type not in ("counter", "gauge"):
                continue  # Ignore histograms and others
            for sample in family.samples:
                name, value = sample.name, sample.value
                if name in metric_map:
                    setattr(stats, metric_map[name], value)
        return stats


class EngineStatsScraper(metaclass=SingletonMeta):
    def __init__(self, scrape_interval: float):
        """
        Initialize the scraper to periodically fetch metrics from all serving engines.

        Args:
            scrape_interval (float): The interval in seconds
                to scrape the metrics.

        Raises:
            ValueError: if the service discover module is have
            not been initialized.

        """
        # Allow multiple calls but require the first call provide scrape_interval.
        if hasattr(self, "_initialized"):
            return
        if scrape_interval is None:
            raise ValueError(
                "EngineStatsScraper must be initialized with scrape_interval"
            )
        self.engine_stats: Dict[str, EngineStats] = {}
        self.engine_stats_lock = threading.Lock()
        self.scrape_interval = scrape_interval

        # scrape thread
        self.running = True
        self.scrape_thread = threading.Thread(target=self._scrape_worker, daemon=True)
        self.scrape_thread.start()
        self._initialized = True

    def _scrape_one_endpoint(self, url: str):
        """
        Scrape metrics from a single serving engine.

        Args:
            url (str): The URL of the serving engine (does not contain endpoint)
        """
        try:
            response = requests.get(url + "/metrics", timeout=self.scrape_interval)
            response.raise_for_status()
            engine_stats = EngineStats.from_vllm_scrape(response.text)
        except Exception as e:
            logger.error(f"Failed to scrape metrics from {url}: {e}")
            return None
        return engine_stats

    def _scrape_metrics(self):
        """
        Scrape metrics from all serving engines.

        Scrape metrics from all serving engines by calling
        _scrape_one_endpoint on each of them. The metrics are
        stored in self.engine_stats.

        """
        collected_engine_stats = {}
        endpoints = get_service_discovery().get_endpoint_info()
        logger.info(f"Scraping metrics from {len(endpoints)} serving engine(s)")
        for info in endpoints:
            url = info.url
            engine_stats = self._scrape_one_endpoint(url)
            if engine_stats:
                collected_engine_stats[url] = engine_stats

        with self.engine_stats_lock:
            old_urls = list(self.engine_stats.keys())
            for old_url in old_urls:
                if old_url not in collected_engine_stats:
                    del self.engine_stats[old_url]
            for url, stats in collected_engine_stats.items():
                self.engine_stats[url] = stats

    def _sleep_or_break(self, check_interval: float = 1):
        """
        Sleep for self.scrape_interval seconds if self.running is True.
        Otherwise, break the loop.
        """
        for _ in range(int(self.scrape_interval / check_interval)):
            if not self.running:
                break
            time.sleep(check_interval)

    def _scrape_worker(self):
        """
        Periodically scrape metrics from all serving engines in the background.

        This function will loop forever and sleep for self.scrape_interval
        seconds between each scrape. It will call _scrape_metrics to scrape
        metrics from all serving engines and store them in self.engine_stats.

        """
        while self.running:
            self._scrape_metrics()
            self._sleep_or_break()

    def get_engine_stats(self) -> Dict[str, EngineStats]:
        """
        Retrieve a copy of the current engine statistics.

        Returns:
            A dictionary mapping engine URLs to their respective EngineStats objects.
        """
        with self.engine_stats_lock:
            return self.engine_stats.copy()

    def get_health(self) -> bool:
        """
        Check if the EngineStatsScraper is healthy

        Returns:
            bool: True if the EngineStatsScraper is healthy,
                False otherwise
        """
        return self.scrape_thread.is_alive()

    def close(self):
        """
        Stop the background thread and cleanup resources.
        """
        self.running = False
        self.scrape_thread.join()


def initialize_engine_stats_scraper(scrape_interval: float) -> EngineStatsScraper:
    return EngineStatsScraper(scrape_interval)


def get_engine_stats_scraper() -> EngineStatsScraper:
    # This call returns the already-initialized instance (or raises an error if not yet initialized)
    return EngineStatsScraper()
