from flask import Flask, request
import requests
import random

TOKEN = "7970673691:AAEQxRN8EBJsMoF2ANYtEpNR8YHZwhjr6zQ"
URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

app = Flask(__name__)

def send_message(chat_id, text):
    requests.post(URL, json={"chat_id": chat_id, "text": text})

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"]
        if text == "/start":
            send_message(chat_id, "Bem-vindo à Operação Raghnild.")
        elif text == "/introducao":
            send_message(chat_id, "Copenhague, 23h17. Três máfias. Um objetivo.")
        elif text == "/cofre1":
            send_message(chat_id, "Você está diante do Cofre Antigo...")
        elif text == "/cofre2":
            send_message(chat_id, "O segundo cofre está trancado com mais segurança.")
        elif text == "/salavip1":
            send_message(chat_id, "Você entrou na Sala VIP. As câmeras giram.")
        elif text == "/salavip2":
            send_message(chat_id, "Sala VIP 2: silêncio absoluto... algo está errado.")
        elif text == "/fuga":
            send_message(chat_id, "Hora da fuga. A polícia está a caminho!")
        elif text == "/roll_outfit":
            rolagem = random.randint(1, 6)
            send_message(chat_id, f"Outfit rolou um dado: {rolagem}")
        elif text == "/roll_camorra":
            rolagem = random.randint(1, 6)
            send_message(chat_id, f"Camorra rolou um dado: {rolagem}")
        elif text == "/roll_famiglia":
            rolagem = random.randint(1, 6)
            send_message(chat_id, f"Famiglia rolou um dado: {rolagem}")
        else:
            send_message(chat_id, "Comando não reconhecido.")
    return {"ok": True}
    
    # Adicione isso no final do bot.py
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Bot Telegram Operação Raghnild está rodando!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)