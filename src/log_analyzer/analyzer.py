import gzip
import re
from collections import defaultdict
from pathlib import Path
from statistics import median
from typing import Dict, Generator, Iterable, Optional, Union

from .schemas import LogEntry, LogFile, UrlStats

# Nginx log regex pattern - standard combined format with request_time at the end
# Example: 1.196.116.32 -  - [29/Jun/2017:03:50:22 +0300] "GET /api/users/2 HTTP/1.1" 200 927 "-" "Lynx/2.8.8dev.9 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/2.10.5" "-" "1498697422-2190034393-4708-9752759" "dc7161be3" 0.390 # noqa: E501
NGINX_LOG_PATTERN = re.compile(
    r"^(?P<ip>[\d.]+)\s+"  # IP address
    r"(?P<id>\S+)\s+"  # id
    r"(?P<user>\S+)\s+"  # user
    r"\[(?P<timestamp>[^\]]+)\]\s+"  # timestamp
    r'"(?P<request>[^"]+)"\s+'  # request
    r"(?P<status>\d+)\s+"  # status
    r"(?P<bytes>\S+)\s+"  # bytes sent
    r'(?P<referer>"[^"]*")?\s+'  # referer (optional)
    r'(?P<user_agent>"[^"]*")?\s*'  # user agent (optional)
    r"(?P<additional_id>\S+)\s+"  # additional id (optional)
    r"(?P<request_id>\S+)\s+"  # request id (optional)
    r"(?P<transaction_id>\S+)\s+"  # transaction id (optional)
    r"(?P<request_time>[\d.]+)$"  # request_time
)


class LogAnalyzer:
    """Main class for analyzing nginx logs."""

    def __init__(self) -> None:
        """
        Initialize the log analyzer.
        """
        self.total_lines: int = 0
        self.error_lines: int = 0

    def analyze(self, log_file: Optional[LogFile] = None) -> Optional[list[UrlStats]]:
        """
        Analyze the latest log file and generate report.

        Args:
            log_file: LogFile to analyze (finds latest if None)

        Returns:
            Path to generated report, or None if no analysis performedpythom grnr
        """

        if log_file is None or not Path(log_file.path).exists():
            return None

        entries = list(self._parse_nginx_log(log_file.path, log_file.is_compressed))

        if not entries:
            return None

        return self._calculate_statistics(entries)

    def _parse_nginx_log(
        self, log_file: Union[str, Path], is_compressed: bool = False
    ) -> Generator[LogEntry, None, None]:
        """
        Parse nginx log file and yield LogEntry objects.

        Args:
            log_file: Path to log file
            is_compressed: file is gzipped

        Yields:
            LogEntry objects for each valid log line
        """
        log_path = Path(log_file)

        if is_compressed:
            with gzip.open(log_path, "rt", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    self.total_lines += 1
                    entry = self._parse_line(line)
                    if entry:
                        yield entry
                    else:
                        self.error_lines += 1
        else:
            with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    self.total_lines += 1
                    entry = self._parse_line(line)
                    if entry:
                        yield entry
                    else:
                        self.error_lines += 1

    def _parse_line(self, line: str) -> Optional[LogEntry]:
        """
        Parse a single nginx log line.

        Args:
            line: A single line from the nginx log

        Returns:
            LogEntry with url and request_time, or None if parsing fails
        """
        line = line.strip()
        if not line:
            return None

        match = NGINX_LOG_PATTERN.match(line)
        if not match:
            return None

        request = match.group("request")
        request_parts = request.split()
        if len(request_parts) >= 2:
            url = request_parts[1]
        else:
            url = request

        try:
            request_time = float(match.group("request_time"))
        except (ValueError, TypeError):
            return None

        return LogEntry(url=url, request_time=request_time)

    def _calculate_statistics(
        self, entries: Iterable[LogEntry], report_size: int = 100
    ) -> list[UrlStats]:
        """
        Calculate statistics for all URLs.

        Args:
            entries: list of LogEntry objects
            report_size: Maximum number of URLs to include in report

        Returns:
            List of UrlStats sorted by time_sum descending
        """
        url_data: Dict[str, list[float]] = defaultdict(list)

        for entry in entries:
            url_data[entry.url].append(entry.request_time)

        total_requests = sum(len(times) for times in url_data.values())
        total_time = sum(sum(times) for times in url_data.values())

        stats_list: list[UrlStats] = []
        for url, times in url_data.items():
            count = len(times)
            time_sum = sum(times)
            time_max = max(times)
            time_med = median(times)
            time_avg = time_sum / count if count > 0 else 0.0

            count_perc = (count / total_requests * 100) if total_requests > 0 else 0.0
            time_perc = (time_sum / total_time * 100) if total_time > 0 else 0.0

            stats_list.append(
                UrlStats(
                    url=url,
                    count=count,
                    count_perc=count_perc,
                    time_sum=time_sum,
                    time_perc=time_perc,
                    time_avg=time_avg,
                    time_max=time_max,
                    time_med=time_med,
                )
            )

        stats_list.sort(key=lambda x: x.time_sum, reverse=True)
        return stats_list
