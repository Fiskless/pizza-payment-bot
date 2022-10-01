import logging
import telegram


class CustomLogsHandler(logging.Handler):
    def __init__(self, chat_id, tg_token=None):
        super().__init__()
        self.chat_id = chat_id
        self.bot = None
        self.vk_api = None
        self.bot = telegram.Bot(token=tg_token)

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(
                chat_id=self.chat_id,
                text=log_entry
            )
