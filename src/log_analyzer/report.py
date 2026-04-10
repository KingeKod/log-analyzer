"""Nginx log analyzer core functionality."""

import json
from pathlib import Path

from .config import Config
from .schemas import LogFile, UrlStats


class Report:
    def __init__(self, config: Config, log_file: LogFile):
        Path(config.report_dir).mkdir(parents=True, exist_ok=True)
        self.report_size = config.report_size
        self.report_path = Path(config.report_dir) / self._report_filename(log_file)

    def generate_report_html(self, stats: list[UrlStats]) -> str:
        """
        Generate HTML report from statistics.
        """
        stats_list = stats[: self.report_size]
        stats_json = json.dumps(
            [
                {
                    "url": s.url,
                    "count": s.count,
                    "count_perc": round(s.count_perc, 2),
                    "time_sum": round(s.time_sum, 3),
                    "time_perc": round(s.time_perc, 2),
                    "time_avg": round(s.time_avg, 3),
                    "time_max": round(s.time_max, 3),
                    "time_med": round(s.time_med, 3),
                }
                for s in stats_list
            ],
            ensure_ascii=False,
            indent=2,
        )

        with open("report_template.html", "r", encoding="utf-8") as f:
            template = f.read()

        report = template.replace("$table_json", stats_json)
        self.report_path.write_text(report, encoding="utf-8")

        return str(self.report_path)

    def _report_filename(self, log_file: LogFile) -> str:
        date_str = log_file.date.strftime("%Y.%m.%d")
        return f"report-{date_str}.html"

    def exists(self) -> bool:
        return self.report_path.exists()
