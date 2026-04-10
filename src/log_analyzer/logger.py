import logging
import sys
from logging import INFO
from typing import Any, Optional

import structlog


class Logger:
    @staticmethod
    def setup(log_analyzer_path: Optional[str] = None) -> Any:
        """
        Set up logging based on configuration log analyzer path
        """
        if log_analyzer_path is not None:
            logging.basicConfig(
                format="%(message)s",
                level=logging.INFO,
                filename=str(log_analyzer_path),
            )
        else:
            logging.basicConfig(
                format="%(message)s",
                level=logging.INFO,
                stream=sys.stdout,
            )

        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                structlog.dev.ConsoleRenderer(),
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.make_filtering_bound_logger(INFO),
            cache_logger_on_first_use=True,
        )

        return structlog.get_logger()
