import sys
import traceback
from pathlib import Path
from typing import Any, Optional, Union

from log_analyzer.analyzer import LogAnalyzer
from log_analyzer.config import Config
from log_analyzer.log_file_finder import LogFileFinder
from log_analyzer.logger import Logger
from log_analyzer.report import Report


def main(config_path: Optional[str] = None) -> int:
    """
    Args:
        config_path: Path to configuration file

    Returns:
        Exit code (0 for success, non-zero for error)
    """
    logger: Optional[Any] = None

    try:
        config = Config.load_config(config_path)

        try:
            logger_path = config.log_analyzer_path
            logger = Logger.setup(logger_path)
        except IsADirectoryError as e:
            print(f"Error: Log analyzer path not must be dir - {e}")
            return 0

        logger.info("Log analyzer started", config=config.to_dict())
        log_dir = Path(config.log_dir)

        if not log_dir.exists():
            logger.warning("Log directory does not exist", path=str(log_dir))
            return 0

        log_file = LogFileFinder.find_latest_log(str(log_dir))

        if log_file is None:
            logger.info("No log files found", log_dir=str(log_dir))
            return 0

        report = Report(config, log_file)
        analyzer = LogAnalyzer()

        logger.info(
            "Found log file",
            path=str(log_file.path),
            date=log_file.date.isoformat(),
            is_compressed=log_file.is_compressed,
        )

        report_path: Optional[Union[str, Path]] = None

        if report.exists():
            report_path = report.report_path
        else:
            stats = analyzer.analyze(log_file)
            if stats is not None:
                report_path = report.generate_report_html(stats)
                error_rate = analyzer.error_lines / analyzer.total_lines
                if analyzer.total_lines > 0 and error_rate > config.error_threshold:
                    logger.warning("Report have many broke strings")
            else:
                report_path = None

        if report_path:
            logger.info("Report generated successfully", path=report_path)
            return 0
        else:
            logger.warning("No report generated (no valid log entries)")
            return 0

    except FileNotFoundError as e:
        if logger:
            logger.error("File not found", error=str(e), exc_info=True)
        else:
            print(f"Error: File not found - {e}", file=sys.stderr)
        return 1

    except ValueError as e:
        if logger:
            logger.error("Invalid configuration", error=str(e), exc_info=True)
        else:
            print(f"Error: Invalid configuration - {e}", file=sys.stderr)
        return 1

    except KeyboardInterrupt:
        if logger:
            logger.info("Interrupted by user")
        else:
            print("\nInterrupted by user", file=sys.stderr)
        return 1

    except Exception as e:
        if logger:
            logger.error("Unexpected error", error=str(e), exc_info=True)
        else:
            print(f"Error: Unexpected error - {e}", file=sys.stderr)
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    config_path = sys.argv[2] if len(sys.argv) > 2 and sys.argv[1] in ("-c", "--config") else None

    sys.exit(main(config_path))
