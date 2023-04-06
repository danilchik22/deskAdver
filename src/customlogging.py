import logging
import os

import requests


def send_message_telegramm(text):
    """
    Отправка сообщений в Telegram.
    token - это ваш токен бота Telegram. Получается с помощью бота @BotFather. Нужно найти его
    в поиске и нажать кнопку /start. chat_id получается с помощью @MyTelegramID_bot.
    Необходимо начать с ним диалог и вы получите chat_id.
    """
    token = os.getenv("TOKEN_BOT")
    chat_id = os.getenv("CHAT_ID")
    url_req = (
        "https://api.telegram.org/bot"
        + token
        + "/sendMessage"
        + "?chat_id="
        + chat_id
        + "&text="
        + text
    )
    try:
        requests.get(url_req)
    except Exception:
        print("API Telegram недоступен. Либо недействующий Chat id или TokenBot.")


class TelegramHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        send_message_telegramm(log_entry)


logging_config: dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {
            "format": "[%(asctime)s] %(levelname)s %(name)s (%(lineno)d) %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "console",
        },
        "telegramm": {
            "level": "ERROR",
            "class": "src.customlogging.TelegramHandler",
            "formatter": "console",
        },
    },
    "root": {
        "handlers": ["console", "telegramm"],
        "level": "INFO",
        "propagate": False,
    },
}
