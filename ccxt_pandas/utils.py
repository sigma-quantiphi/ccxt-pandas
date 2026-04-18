import os
from typing import Any

import pandas as pd
import requests


def print_markdown(message: Any) -> None:
    if isinstance(message, pd.DataFrame):
        print(message.to_markdown(index=False))
    else:
        print(message)


def time_logger(func):
    def wrapper(*args, **kwargs):
        start_time = pd.Timestamp.now(tz="UTC")
        result = func(*args, **kwargs)
        end_time = pd.Timestamp.now(tz="UTC")
        elapsed_time = end_time - start_time
        print(f"{end_time}: Function {func.__name__} executed in {elapsed_time}.")
        return result

    return wrapper


def send_telegram_message(
    message: str,
    telegram_message_thread_id: int,
    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN"),
    telegram_chat_id: str = os.getenv("TELEGRAM_CHAT_ID"),
) -> dict:
    """Send notifications to Telegram."""
    telegram_api_url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    params = {
        "chat_id": telegram_chat_id,
        "text": message,
        "message_thread_id": telegram_message_thread_id,
    }
    response = requests.get(telegram_api_url, params=params)
    return response.json()
