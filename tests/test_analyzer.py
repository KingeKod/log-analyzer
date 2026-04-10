from src.log_analyzer.analyzer import LogAnalyzer
from src.log_analyzer.log_file_finder import LogFileFinder
from src.log_analyzer.schemas import UrlStats


def last_log(tmp_path) -> LogAnalyzer:
    log_file = tmp_path / "nginx-access-ui.log-20170630"
    log_file.write_text(
        '1.196.116.32 -  - [29/Jun/2017:03:50:22 +0300] "GET /api/users/2 HTTP/1.1" 200 927 "-" "Lynx/2.8.8dev.9 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/2.10.5" "-" "1498697422-2190034393-4708-9752759" "dc7161be3" 0.390\n'  # noqa: E501
        '1.196.116.32 -  - [29/Jun/2017:03:50:22 +0300] "GET /api/users HTTP/1.1" 200 927 "-" "Lynx/2.8.8dev.9 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/2.10.5" "-" "1498697422-2190034393-4708-9752759" "dc7161be3" 0.550\n'  # noqa: E501
        '1.196.116.32 -  - [29/Jun/2017:03:50:22 +0300] "GET /api/users/2 HTTP/1.1" 200 927 "-" "Lynx/2.8.8dev.9 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/2.10.5" "-" "1498697422-2190034393-4708-9752759" "dc7161be3" 0.440\n'  # noqa: E501
        '1.196.116.32 -  - [29/Jun/2017:03:50:22 +0300] "GET /api/users HTTP/1.1" 200 927 "-" "Lynx/2.8.8dev.9 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/2.10.5" "-" "1498697422-2190034393-4708-9752759" "dc7161be3" 0.440\n'  # noqa: E501
    )
    return LogFileFinder.find_latest_log(tmp_path)


def empty_last_log(tmp_path) -> LogAnalyzer:
    log_file = tmp_path / "nginx-access-ui.log-20170630"
    log_file.write_text("   ")
    return LogFileFinder.find_latest_log(tmp_path)


def invalid_last_log(tmp_path) -> LogAnalyzer:
    log_file = tmp_path / "nginx-access-ui.log-20170630"
    log_file.write_text(
        '1.196.116.32 -  - [29/Jun/2017:03:50:22 +0300] "GET /api/users/2 HTTP/1.1" 200 927 "-" "Lynx/2.8.8dev.9 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/2.10.5" "-" "1498697422-2190034393-4708-9752759" "dc7161be3" 0.390\n'  # noqa: E501
        '1.196.116.32 -  - [29/Jun/2017:03:50:22 +0300] "GET /api/users HTTP/1.1" 200 927 "-" "Lynx/2.8.8dev.9 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/2.10.5" "-" 0.550\n'  # noqa: E501
        '1.196.116.32 -  - [29/Jun/2017:03:50:22 +0300] "GET /api/users/2 HTTP/1.1" 200 927 "-" "Lynx/2.8.8dev.9 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/2.10.5" "-" "1498697422-2190034393-4708-9752759" "dc7161be3" 0.440\n'  # noqa: E501
        '1.196.116.32 -  - [29/Jun/2017:03:50:22 +0300] "GET /api/users HTTP/1.1" 200 927 "-" 0.440\n'  # noqa: E501
    )
    return LogFileFinder.find_latest_log(tmp_path)


def test_parse_valid_file(tmp_path):
    result = LogAnalyzer().analyze(last_log(tmp_path))
    assert result is not None
    assert isinstance(result, list)
    assert isinstance(result[0], UrlStats)
    assert result[0].url == "/api/users"
    assert result[0].count == 2
    assert result[0].count_perc == 50.0
    assert result[0].time_sum == 0.99
    assert result[0].time_perc == 54.395604395604394
    assert result[0].time_avg == 0.495
    assert result[0].time_max == 0.55
    assert result[0].time_med == 0.495


def test_parse_empty_file(tmp_path):
    result = LogAnalyzer().analyze(empty_last_log(tmp_path))
    assert result is None


def test_parse_file_with_broke_lines(tmp_path):
    analyzer = LogAnalyzer()
    analyzer.analyze(invalid_last_log(tmp_path))
    assert analyzer.total_lines == 4
    assert analyzer.error_lines == 2
    assert analyzer.error_lines == 2
