import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

DEFAULT_CONFIG: Dict[str, Any] = {
    "log_dir": "./logs",
    "report_dir": "./reports",
    "report_size": 100,
    # "log_analyzer_path": "./logs_out/out.log",
    "log_analyzer_path": None,
    "error_threshold": 0.1,
}


@dataclass
class Config:
    log_dir: str = DEFAULT_CONFIG["log_dir"]
    report_dir: str = DEFAULT_CONFIG["report_dir"]
    report_size: int = DEFAULT_CONFIG["report_size"]
    log_analyzer_path: Optional[str] = DEFAULT_CONFIG["log_analyzer_path"]
    error_threshold: float = DEFAULT_CONFIG["error_threshold"]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "log_dir": self.log_dir,
            "report_dir": self.report_dir,
            "report_size": self.report_size,
            "log_analyzer_path": self.log_analyzer_path,
            "error_threshold": self.error_threshold,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Config":
        """Create config from dictionary."""
        return cls(
            log_dir=data.get("log_dir", cls.log_dir),
            report_dir=data.get("report_dir", cls.report_dir),
            report_size=data.get("report_size", cls.report_size),
            log_analyzer_path=data.get("log_analyzer_path", cls.log_analyzer_path),
            error_threshold=data.get("error_threshold", cls.error_threshold),
        )

    @staticmethod
    def load_config(config_path: Optional[str] = None) -> "Config":
        """
        Load configuration from file or use defaults.

        Args:
            config_path: Path to configuration file (uses default if None or empty)

        Returns:
            Config object with merged configuration

        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If config file is not valid JSON
        """
        config_dict = DEFAULT_CONFIG.copy()

        if config_path is None:
            default_path = Path("./config.json")
            if default_path.exists():
                config_path = str(default_path)
            else:
                return Config.from_dict(config_dict)

        config_path_obj = Path(config_path)

        if not config_path_obj.exists():
            raise FileNotFoundError(f"Config file not found: {config_path_obj}")

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                file_config = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in config file {config_path}: {e}")

        config_dict.update(file_config)

        return Config.from_dict(config_dict)
