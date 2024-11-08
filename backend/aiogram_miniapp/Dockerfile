# Base image using Python 3.11.5-slim
FROM python:3.11.5-slim

# Set environment variables
ENV \
  # Python settings:
  PYTHONFAULTHANDLER=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  # Pip settings:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # Poetry settings:
  POETRY_VERSION=1.3.2 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  # Locale settings:
  LANG=ru_RU.UTF-8 \
  LANGUAGE=ru_RU:ru \
  LC_ALL=ru_RU.UTF-8 \
  # Path for Poetry:
  PATH="/root/.local/bin:$PATH"

# Install system dependencies and Poetry
RUN apt-get update && \
  apt-get install --no-install-recommends -y \
  locales \
  locales-all \
  build-essential \
  gettext \
  libpq-dev \
  ffmpeg \
  wget \
  curl \
  && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/* \
  && echo "ru_RU.UTF-8 UTF-8" > /etc/locale.gen \
  && locale-gen ru_RU.UTF-8 \
  && update-locale LANG=ru_RU.UTF-8 \
  && pip install "poetry-core==1.4.0" "poetry==$POETRY_VERSION" && poetry --version

# Set the working directory
WORKDIR /app

# Copy the project files
COPY ./poetry.lock ./pyproject.toml /app/

# Install Python dependencies
RUN poetry install --no-dev --no-interaction --no-ansi

# Copy the remaining project files
COPY . .

# Set environment variables for the bot
ENV BOT_API_KEY=${BOT_API_KEY}
ENV WEB_SERVER_HOST=${WEB_SERVER_HOST}
# Pass to nginx
# ENV WEB_SERVER_PORT=${WEB_SERVER_PORT}
ENV WEBHOOK_PATH=${WEBHOOK_PATH}
ENV WEBHOOK_SECRET=${WEBHOOK_SECRET}
ENV BASE_WEBHOOK_URL=${BASE_WEBHOOK_URL}
ENV BOT_MODE=${BOT_MODE}

# Expose the port for the webhook
EXPOSE ${WEB_SERVER_PORT}

# Copy and make the entrypoint script executable
COPY ./entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

# Run the entrypoint script
ENTRYPOINT ["sh", "entrypoint.sh"]
