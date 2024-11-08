#!/bin/sh

# This script handles starting the bot based on the BOT_MODE environment variable.

cd ./aiogram_miniapp

# Check if the necessary environment variables are set
if [ -z "$BOT_API_KEY" ]; then
  echo "Error: BOT_API_KEY is not set."
  exit 1
fi

if [ "$BOT_MODE" = "webhook" ]; then
  # Check if all required webhook environment variables are set
  if [ -z "$BASE_WEBHOOK_URL" ] || [ -z "$WEB_SERVER_HOST" ] || [ -z "$WEB_SERVER_PORT" ] || [ -z "$WEBHOOK_SECRET" ]; then
    echo "Error: One or more required environment variables for webhook mode are not set."
    echo "Required: BASE_WEBHOOK_URL, WEB_SERVER_HOST, WEB_SERVER_PORT, WEBHOOK_SECRET"
    exit 1
  fi

  # If running in webhook mode
  echo "Starting bot in webhook mode..."
  poetry run python main.py --webhook-url="${BASE_WEBHOOK_URL}${WEBHOOK_PATH}" \
                            --webhook-host="$WEB_SERVER_HOST" \
                            --webhook-port="$WEB_SERVER_PORT" \
                            --webhook-secret="$WEBHOOK_SECRET"
else
  # Default to long-polling mode
  echo "Starting bot in long-polling mode..."
  poetry run python main.py
fi
