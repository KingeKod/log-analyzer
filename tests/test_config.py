"""Tests for configuration management."""

import json

import pytest

from src.log_analyzer.config import Config


def test_default_values():
    config = Config()
    assert config.log_dir == "./logs"
    assert config.report_dir == "./reports"
    assert config.report_size == 100
    assert config.log_analyzer_path is None
    assert config.error_threshold == 0.1


def test_custom_values():
    config = Config(
        log_dir="/custom/logs",
        report_dir="/custom/reports",
        report_size=50,
        log_analyzer_path="/var/log/analyzer.log",
        error_threshold=0.2,
    )
    assert config.log_dir == "/custom/logs"
    assert config.report_dir == "/custom/reports"
    assert config.report_size == 50
    assert config.log_analyzer_path == "/var/log/analyzer.log"
    assert config.error_threshold == 0.2


def test_to_dict():
    config = Config(log_dir="/custom/logs", report_size=50, log_analyzer_path="/var/log/test.log")
    config_dict = config.to_dict()

    assert config_dict["log_dir"] == "/custom/logs"
    assert config_dict["report_size"] == 50
    assert config_dict["log_analyzer_path"] == "/var/log/test.log"


def test_from_dict():
    data = {
        "log_dir": "/custom/logs",
        "report_dir": "/custom/reports",
        "report_size": 50,
        "log_analyzer_path": "/var/log/test.log",
        "error_threshold": 0.2,
    }
    config = Config.from_dict(data)

    assert config.log_dir == "/custom/logs"
    assert config.report_dir == "/custom/reports"
    assert config.report_size == 50
    assert config.log_analyzer_path == "/var/log/test.log"
    assert config.error_threshold == 0.2


def test_load_config_empty_file(tmp_path):
    config_file = tmp_path / "config.json"
    config_file.write_text("{}")

    config = Config.load_config(str(config_file))
    assert config.log_dir == "./logs"
    assert config.report_size == 100


def test_load_config_file_not_found():
    with pytest.raises(FileNotFoundError):
        Config.load_config("/nonexistent/config.json")


def test_load_config_invalid_json(tmp_path):
    config_file = tmp_path / "config.json"
    config_file.write_text("invalid json content")

    with pytest.raises(ValueError):
        Config.load_config(str(config_file))


def test_load_config_partial_override(tmp_path):
    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps({"log_dir": "/custom/logs", "error_threshold": 0.05}))

    config = Config.load_config(str(config_file))
    assert config.log_dir == "/custom/logs"
    assert config.error_threshold == 0.05
    assert config.report_size == 100
    assert config.report_dir == "./reports"


def test_load_config_no_file_uses_default():
    config = Config.load_config(None)
    assert config.log_dir == "./logs"
    assert config.error_threshold == 0.4
