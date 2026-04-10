import re
from datetime import datetime
from pathlib import Path
from typing import Optional

from .schemas import LogFile


class LogFileFinder:
    """Finder for nginx log files on date in filename."""

    _LOG_FILE_PATTERN = re.compile(r"nginx-access-ui\.log-(\d{8})(?:\.gz)?$")

    @staticmethod
    def find_latest_log(log_dir: str) -> Optional[LogFile]:
        log_path = Path(log_dir)

        if not log_path.exists():
            return None

        latest_file: Optional[Path] = None
        latest_date: Optional[datetime] = None

        for file_path in log_path.iterdir():
            match = LogFileFinder._LOG_FILE_PATTERN.match(file_path.name)

            if match:
                date_str = match.group(1)
                try:
                    file_date = datetime.strptime(date_str, "%Y%m%d")

                    if latest_date is None or file_date > latest_date:
                        latest_date = file_date
                        latest_file = file_path
                except ValueError:
                    continue

        if latest_file is None or latest_date is None:
            return None

        return LogFile(
            path=latest_file,
            date=latest_date,
            is_compressed=latest_file.suffix == ".gz",
        )
