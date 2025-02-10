import time
import json
import requests
import os

# === Пути к файлам ===
CONFIG_FILE = "config.json"  # Конфигурационный файл с API и ID
LOG_FILE = "log.json"  # Файл с JSON-логами

# Функция загрузки конфигурации
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            try:
                config = json.load(f)
                return config.get("BOT_TOKEN"), config.get("CHAT_ID")
            except json.JSONDecodeError:
                print("Ошибка чтения config.json!")
    return None, None

# Функция отправки сообщения в Telegram
def send_message(bot_token, chat_id, text):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=payload)
    return response.status_code == 200

# Функция обработки JSON-лога
def watch_log(bot_token, chat_id):
    while True:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    if isinstance(data, list) and data:
                        for entry in data:
                            message_text = (f"*Token Address:* {entry['tokenAddress']}\n"
                                            f"*Description:* {entry['description']}\n"
                                            f"*Telegram:* {entry['telegram']}")
                            print(f"Отправка:\n{message_text}")
                            send_message(bot_token, chat_id, message_text)

                        # Очищаем лог после отправки
                        with open(LOG_FILE, "w", encoding="utf-8") as f:
                            json.dump([], f)
                except json.JSONDecodeError:
                    print("Ошибка чтения log.json!")
        time.sleep(3)

if __name__ == "__main__":
    print("Загрузка конфигурации...")
    bot_token, chat_id = load_config()

    if not bot_token or not chat_id:
        print("Ошибка: Не удалось загрузить BOT_TOKEN и CHAT_ID из config.json")
    else:
        print("Бот запущен и отслеживает JSON-лог...")
        watch_log(bot_token, chat_id)
