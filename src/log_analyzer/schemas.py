from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class LogFile:
    """Represents a parsed log file."""

    path: Path
    date: datetime
    is_compressed: bool


@dataclass
class LogEntry:
    """Represents a single log entry."""

    url: str
    request_time: float


@dataclass
class UrlStats:
    """Statistics for a single URL."""

    url: str
    count: int
    count_perc: float
    time_sum: float
    time_perc: float
    time_avg: float
    time_max: float
    time_med: float
