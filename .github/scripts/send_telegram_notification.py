import requests
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

def create_github_release(tag_name, body):
    github_token = os.getenv('GITHUB_TOKEN')
    repo_owner = os.getenv('GITHUB_REPOSITORY_OWNER')
    repo_name = os.getenv('GITHUB_REPOSITORY_NAME')

    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/releases'
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    payload = {
        'tag_name': tag_name,
        'body': body
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

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

    # Tạo GitHub release
    tag_name = f'v{stock}'
    body = f"Gittechvn - Kho hàng: {stock}"
    create_github_release(tag_name, body)

if __name__ == "__main__":
    main()
