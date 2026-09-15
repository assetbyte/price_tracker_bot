from dataclasses import dataclass
import hmac
import hashlib
import json
import os
from urllib.parse import parse_qsl

from dotenv import load_dotenv
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

load_dotenv()


@dataclass
class TelegramUser:
    telegram_id: int
    first_name: str
    last_name: str
    username: str
    is_authenticated: bool = True


class TelegramAuthentication(BaseAuthentication):
    async def authenticate(self, request):
        init_data = request.headers.get('X-Telegram-Init-Data')
        
        if not init_data:
            return None

        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not bot_token:
            raise AuthenticationFailed('TELEGRAM_BOT_TOKEN not set in environment.')

        parsed_data = dict(parse_qsl(init_data))
        received_hash = parsed_data.pop('hash', None)

        if not received_hash:
            raise AuthenticationFailed('No hash provided in initData.')

        data_check_string = '\n'.join(
            f"{k}={v}" for k, v in sorted(parsed_data.items())
        )
        
        secret_key = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()
        calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

        if calculated_hash != received_hash:
            raise AuthenticationFailed('Недействительная подпись Telegram initData.')

        user_raw = parsed_data.get('user')
        if not user_raw:
            raise AuthenticationFailed('Данные пользователя отсутствуют в initData.')

        user_data = json.loads(user_raw)

        user = TelegramUser(
            telegram_id=user_data['id'],
            first_name=user_data.get('first_name', ''),
            last_name=user_data.get('last_name', ''),
            username=user_data.get('username', ''),
            is_authenticated=True
        )

        return (user, None)