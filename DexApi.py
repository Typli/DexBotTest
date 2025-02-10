import requests
import json
import time
import os

url = "https://api.dexscreener.com/token-profiles/latest/v1"

headers = {
    "cookie": "__cf_bm=qhxUqZ4N1htRDQDbKV3nhF4GnlLcyffox31WM8jCk6c-1739113476-1.0.1.1-MT7Wq2dI6SlkLATv7qxEZOWZQo_c3lirXqAP5vAWb3JL.25obUP.bJ1qNEK0e_2RuJVwOfsQ4Gsqm.qyBlkN4MV62nZFsEi.Rpjf84jbWls",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

LOG_FILE = "log.json"

# Загружаем предыдущие данные из файла
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        try:
            previous_data = {entry["tokenAddress"] for entry in json.load(f)}
        except json.JSONDecodeError:
            previous_data = set()
else:
    previous_data = set()

while True:
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        new_entries = []

        for entry in data:
            token_address = entry.get("tokenAddress")
            description = entry.get("description")
            telegram_url = next((link["url"] for link in entry.get("links", []) if link.get("type") == "telegram"), None)

            if telegram_url and token_address not in previous_data:
                new_entry = {
                    "tokenAddress": token_address,
                    "description": description,
                    "telegram": telegram_url
                }
                print(json.dumps(new_entry, indent=4, ensure_ascii=False))
                new_entries.append(new_entry)
                previous_data.add(token_address)

        # Если появились новые записи, дополняем файл
        if new_entries:
            if os.path.exists(LOG_FILE):
                with open(LOG_FILE, "r", encoding="utf-8") as f:
                    try:
                        existing_data = json.load(f)
                        if isinstance(existing_data, list):
                            new_entries = existing_data + new_entries
                    except json.JSONDecodeError:
                        pass

            with open(LOG_FILE, "w", encoding="utf-8") as f:
                json.dump(new_entries, f, indent=4, ensure_ascii=False)
    else:
        print(f"Ошибка запроса: {response.status_code}")

    time.sleep(3)