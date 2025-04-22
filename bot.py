from flask import Flask, request
import telebot
import random
import os
from telebot import types

API_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# Armazenamento de pontuação por chat_id
pontuacoes = {}
mafia_selecionada = {}

def init_player(chat_id):
    if chat_id not in pontuacoes:
        pontuacoes[chat_id] = {"Outfit": 0, "Camorra": 0, "Famiglia": 0}
        mafia_selecionada[chat_id] = None

def pontuar(chat_id, mafia, pontos):
    if chat_id in pontuacoes:
        pontuacoes[chat_id][mafia] += pontos

def rolar_dado():
    return random.randint(1, 6)

# Textos
introducao = """
Copenhague, Dinamarca.

Você acaba de pousar. A névoa cobre o teto do Palácio Marienborg.

As três máfias mais perigosas do submundo americano desembarcaram na Europa com o mesmo objetivo:

• Roubar a Lança de Salomão.
• Sequestrar o Embaixador Rashid al-Hariri.

Quem controlar um, domina o mercado negro.
Quem controlar os dois, comanda o submundo.

Quem é você nessa guerra?
"""

cofre1 = """
[PONTO DE ACESSO: COFRE PRINCIPAL — PARTE 1]

Você chegou à ala restrita. O sistema de segurança usa rastreamento térmico.

Use seu comando de dado e responda com: /cofre2
"""

cofre2 = """
[PONTO DE ACESSO: COFRE PRINCIPAL — PARTE 2]

Você insere o código do informante. O visor pisca em verde.

Use seu comando de dado e vá para /salavip1
"""

salavip1 = """
[SALA VIP — PARTE 1]

Você atravessa o salão principal. Rashid al-Hariri negocia com oligarcas russos.

Use seu comando de dado e vá para /salavip2
"""

salavip2 = """
[SALA VIP — PARTE 2]

A escuta transmite em tempo real. A troca será feita no porto de Nyhavn.

Vá para: /fuga
"""

fuga = """
[ROTA DE FUGA — FASE FINAL]

Explosões à distância. Sirenes. Gritos em dinamarquês.

• Se tirou pontos altos em todas as ações, sua máfia escapa com a lança e o embaixador.
• Se falhou em alguma parte, você é interceptado por mercenários rivais.

Fim da missão.
"""

# Comandos

@bot.message_handler(commands=['start'])
def send_start(message):
    init_player(message.chat.id)
    bot.send_message(message.chat.id, "Bem-vindo à Operação Raghnild.\nDigite /introducao para começar.")

@bot.message_handler(commands=['introducao'])
def send_intro(message):
    init_player(message.chat.id)
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 3
    markup.add(
        types.InlineKeyboardButton("Outfit", callback_data="mafia_Outfit"),
        types.InlineKeyboardButton("Camorra", callback_data="mafia_Camorra"),
        types.InlineKeyboardButton("Famiglia", callback_data="mafia_Famiglia")
    )
    bot.send_message(message.chat.id, introducao, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('mafia_'))
def escolher_mafia(call):
    chat_id = call.message.chat.id
    mafia = call.data.split("_")[1]
    mafia_selecionada[chat_id] = mafia
    bot.send_message(chat_id, f"Máfia selecionada: *{mafia}*", parse_mode='Markdown')

@bot.message_handler(commands=['cofre1'])
def send_cofre1(message):
    bot.send_message(message.chat.id, cofre1)

@bot.message_handler(commands=['cofre2'])
def send_cofre2(message):
    bot.send_message(message.chat.id, cofre2)

@bot.message_handler(commands=['salavip1'])
def send_salavip1(message):
    bot.send_message(message.chat.id, salavip1)

@bot.message_handler(commands=['salavip2'])
def send_salavip2(message):
    bot.send_message(message.chat.id, salavip2)

@bot.message_handler(commands=['fuga'])
def send_fuga(message):
    chat_id = message.chat.id
    total = sum(pontuacoes[chat_id].values())
    if total >= 5:
        final = "\nVocê escapa com tudo. Missão concluída com sucesso."
    else:
        final = "\nVocê foi interceptado. A missão falhou."
    bot.send_message(chat_id, fuga + final)

# Comando de pontuação final
@bot.message_handler(commands=['pontuacaofinal'])
def pontuacao_final(message):
    chat_id = message.chat.id
    if chat_id not in pontuacoes:
        bot.send_message(chat_id, "Nenhuma pontuação registrada.")
        return

    ranking = sorted(pontuacoes[chat_id].items(), key=lambda x: x[1], reverse=True)
    resultado = "*Resultado Final da Operação Raghnild:*\n\n"
    medalhas = ["1º lugar", "2º lugar", "3º lugar"]
    for i, (mafia, pontos) in enumerate(ranking):
        resultado += f"{medalhas[i]}: *{mafia}* — {pontos} pontos\n"
    resultado += f"\n*Domínio garantido por:* *{ranking[0][0]}*"
    bot.send_message(chat_id, resultado, parse_mode='Markdown')

# Dado separado por máfia

@bot.message_handler(commands=['dado_outfit'])
def dado_outfit(message):
    chat_id = message.chat.id
    resultado = rolar_dado()
    texto = f"Outfit rolou: {resultado}\n"
    if resultado >= 5:
        texto += "Missão com precisão! +3 pontos."
        pontuar(chat_id, "Outfit", 3)
    elif resultado >= 3:
        texto += "Executou com tensão. +1 ponto."
        pontuar(chat_id, "Outfit", 1)
    else:
        texto += "Falha crítica! Sem pontos."
    bot.send_message(chat_id, texto)

@bot.message_handler(commands=['dado_camorra'])
def dado_camorra(message):
    chat_id = message.chat.id
    resultado = rolar_dado()
    texto = f"Camorra rolou: {resultado}\n"
    if resultado >= 5:
        texto += "Movimento brutal! +3 pontos."
        pontuar(chat_id, "Camorra", 3)
    elif resultado >= 3:
        texto += "Quase perfeito. +1 ponto."
        pontuar(chat_id, "Camorra", 1)
    else:
        texto += "Pegos de surpresa. Sem pontos."
    bot.send_message(chat_id, texto)

@bot.message_handler(commands=['dado_famiglia'])
def dado_famiglia(message):
    chat_id = message.chat.id
    resultado = rolar_dado()
    texto = f"Famiglia rolou: {resultado}\n"
    if resultado >= 5:
        texto += "Jogada magistral! +3 pontos."
        pontuar(chat_id, "Famiglia", 3)
    elif resultado >= 3:
        texto += "Ação arriscada. +1 ponto."
        pontuar(chat_id, "Famiglia", 1)
    else:
        texto += "Plano fracassou. Sem pontos."
    bot.send_message(chat_id, texto)

# Flask
@app.route("/", methods=["POST"])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "OK", 200

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=os.getenv("RENDER_EXTERNAL_URL"))
    app.run(host="0.0.0.0", port=10000)