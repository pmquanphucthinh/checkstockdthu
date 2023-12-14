import requests
import json
import os

def send_telegram_message(bot_token, chat_id, message):
    api_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    params = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'
    }
    response = requests.post(api_url, data=params)
    return response.json()

def main():
    api_url = os.getenv('API_URL')
    api_params = os.getenv('API_PARAMS')
    telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')

    # Gửi request đến API
    response = requests.get(f'{api_url}?{api_params}')
    data = response.json()

    # Gửi dữ liệu về Telegram
    message = f"Thông tin từ API:\n{json.dumps(data, indent=2)}"
    send_telegram_message(telegram_bot_token, telegram_chat_id, message)

if __name__ == "__main__":
    main()