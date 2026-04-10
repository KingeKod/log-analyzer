# Log Analyzer

Анализатор логов nginx с генерацией HTML-отчета.

## Возможности

- Парсинг логов nginx (как сжатых `.gz`, так и обычных файлов)
- Подсчет статистики по URL: количество запросов, время обработки
- Генерация HTML-отчета
- Структурированное логирование

## Установка

```bash
# Установка зависимостей через uv
uv sync
uv sync --dev
```

### Дефолтный запуск

```bash
# Использует конфиг по умолчанию (config.json)
uv run python -m src.log_analyzer.main
```

### Запуск с кастомным конфигом

```bash
uv run python -m src.log_analyzer.main --config /path/to/config.json
```

### Через Makefile

```bash
# Установка зависимостей
make install

# Запуск
make run
```

## Конфигурация

Файл `config.json`:

```json
{
    "log_dir": "./logs",
    "report_dir": "./reports",
    "report_size": 100,
    "log_analyzer_path": "./logs_out/out.log",
    "error_threshold": 0.1
}
```

| Параметр | Описание | Значение по умолчанию |
|----------|----------|----------------------|
| `log_dir` | Директория с лог-файлами | `./logs` |
| `report_dir` | Директория для отчетов | `./reports` |
| `report_size` | Количество URL в отчете | `100` |
| `log_analyzer_path` | Путь до лога программы | `100` |
| `error_threshold` | Порог ошибок парсинга (0.0-1.0) | `0.1` |

## Команды Makefile

| Команда | Описание |
|---------|----------|
| `make install` | Установить зависимости |
| `make lint` | Запустить линтеры |
| `make test` | Запустить тесты |
| `make format` | Отформатировать код |
| `make mypy` | Запустить проверку типов |
| `make clean` | Очистить сгенерированные файлы |
| `make run` | Запустить анализатор |

## Тестирование

```bash
# Запуск всех тестов
make test
```

## Формат логов nginx

```
IP ID USER [DD/Mon/YYYY:HH:MM:SS +ZZZZ] "METHOD /path HTTP/1.1" STATUS BYTES "REFER" "USER_AGENT" "ADDITIONAL_ID" "REQUEST_ID" "TRANSACTION_ID" REQUEST_TIME
```

Пример:
```
1.196.116.32 -  - [29/Jun/2017:03:50:22 +0300] "GET /api/users/2 HTTP/1.1" 200 927 "-" "Lynx/2.8.8dev.9 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/2.10.5" "-" "1498697422-2190034393-4708-9752759" "dc7161be3" 0.390
