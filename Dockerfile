FROM python:3.13-slim

WORKDIR /app

# Установка curl
RUN apt-get update && apt-get install -y --no-install-recommends curl

# Установка uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# Копирование файлов конфигурации
COPY pyproject.toml uv.lock README.md report_template.html config.json ./

# Установка зависимостей
RUN uv sync --frozen --dev

# Копирование проекта
COPY src/ ./src/

# Создание директорий для логов и отчетов
RUN mkdir -p /logs /reports

# Входные параметры
ARG CONFIG_PATH=

ENV CONFIG_PATH=${CONFIG_PATH}

# Команда запуска
CMD ["sh", "-c", "uv run python -m src.log_analyzer.main --config ${CONFIG_PATH}"]
