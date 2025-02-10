from flask import Flask, request, jsonify, render_template_string
import json
import subprocess
import time
import os


app = Flask(__name__)

# HTML-файл
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Получаем путь к папке с `main.py`
HTML_PAGE = os.path.join(BASE_DIR, "index.html")  # Формируем полный путь

@app.route("/")
def index():
    return render_template_string(open(HTML_PAGE, "r", encoding="utf-8").read())

@app.route("/start", methods=["POST"])
def start_bots():
    data = request.json
    bot_token = data.get("botToken")
    chat_id = data.get("chatId")

    # Сохраняем данные в config.json
    with open("config.json", "w", encoding="utf-8") as f:
        json.dump({"BOT_TOKEN": bot_token, "CHAT_ID": chat_id}, f, indent=4)

    # Запуск DexBot
    subprocess.Popen(["python3", "DexBot.py"])
    time.sleep(3)  # Ожидание 3 секунды
    subprocess.Popen(["python3", "DexApi.py"])

    return "Боты запущены!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
