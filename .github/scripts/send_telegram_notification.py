import requests
import json
import os
import subprocess

def send_telegram_message(bot_token, chat_id, message):
    api_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    params = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'
    }
    response = requests.post(api_url, data=params)
    return response.json()

def update_readme(stock):
    with open('README.md', 'r') as f:
        readme_content = f.read()

    new_content = readme_content.replace('Stock: N/A', f'Stock: {stock}')

    with open('README.md', 'w') as f:
        f.write(new_content)

    # Git commit và push
    subprocess.run(['git', 'add', 'README.md'])
    subprocess.run(['git', 'commit', '-m', 'Update stock in README.md'])
    subprocess.run(['git', 'push'])

def main():
    api_url = os.getenv('API_URL')
    api_params = os.getenv('API_PARAMS')
    telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')

    # Gửi request đến API
    response = requests.get(f'{api_url}?{api_params}')
    data = response.json()

    # Trích xuất giá trị stock
    stock = data.get('stock', 'N/A')

    # Gửi dữ liệu về Telegram
    message = f"Gittechvn - Kho hàng: {stock}"
    send_telegram_message(telegram_bot_token, telegram_chat_id, message)

    # Cập nhật thông tin vào README.md và thực hiện commit
    update_readme(stock)

if __name__ == "__main__":
    main()
