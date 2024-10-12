from abc import ABC, abstractmethod
import requests


class MessageSender(ABC):
    @abstractmethod
    def send_message(self, chat_id: int, message: str):
        pass


class MessageParams:
    def __init__(self, chat_id: int, message: str, parse_mode='HTML'):
        self.chat_id = chat_id
        self.message = message
        self.parse_mode = parse_mode

    def to_dict(self):
        return {
            'chat_id': self.chat_id,
            'text': self.message,
            'parse_mode': self.parse_mode
        }


class MessageUrlBuilder:
    def __init__(self, bot_token: str):
        self.bot_token = bot_token

    def build_url(self, method: str):
        return f'https://api.telegram.org/bot{self.bot_token}/{method}'


class TelegramMessageSender(MessageSender):
    def __init__(self, bot_token: str):
        self.bot_token = bot_token

    def send_message(self, chat_id: int, message: str):
        url = MessageUrlBuilder(bot_token=self.bot_token).build_url(method='sendMessage')
        params = MessageParams(chat_id=chat_id, message=message).to_dict()
        requests.get(url, params=params)
