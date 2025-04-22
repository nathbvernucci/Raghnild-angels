from flask import Flask, request
import telebot
import random
import os

API_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# Armazenamento de pontuação por chat_id
pontuacoes = {}

def init_player(chat_id):
    if chat_id not in pontuacoes:
        pontuacoes[chat_id] = {"Outfit": 0, "Camorra": 0, "Famiglia": 0}

def pontuar(chat_id, mafia, pontos):
    if chat_id in pontuacoes:
        pontuacoes[chat_id][mafia] += pontos

def rolar_dado():
    return random.randint(1, 6)

# Mensagens

introducao = """
Copenhague, Dinamarca.

Você acaba de pousar. A névoa cobre o teto do Palácio Marienborg, onde o maior leilão clandestino da Europa está prestes a começar.

As três máfias mais perigosas do submundo americano desembarcaram na Europa com o mesmo objetivo:

• Roubar a Lança de Salomão, relíquia sagrada e símbolo de poder oculto.
• Sequestrar o Embaixador Rashid al-Hariri, peça-chave de uma nova era geopolítica.

Quem controlar um, domina o mercado negro.
Quem controlar os dois, comanda o submundo.

Quem é você nessa guerra?

Escolha sua máfia:
• Outfit
• Camorra
• Famiglia
"""

cofre1 = """
[PONTO DE ACESSO: COFRE PRINCIPAL — PARTE 1]

Você chegou à ala restrita. Luzes vermelhas piscam no teto. O sistema de segurança do palácio usa tecnologia israelense de rastreamento térmico.

Um dos capangas desativa o campo de calor com um bloqueador de espectro. Você se arrasta até o terminal.

É agora. Rola o dado pra tentar quebrar a primeira camada de firewall.

Responda com: /cofre2
"""

cofre2 = """
[PONTO DE ACESSO: COFRE PRINCIPAL — PARTE 2]

Você insere o código extraído do informante da Interpol. O visor pisca em verde.

Rola o dado de novo.

• Se tirar de 1 a 3: um alarme silencioso é acionado. 
• Se tirar de 4 a 6: o sistema abre o cofre como um cofre de banco suíço.

Você ouve o som das engrenagens se movendo.

Digite: /salavip1
"""

salavip1 = """
[SALA VIP — PARTE 1]

Você atravessa o salão principal. Champagne e diamantes. Gente rica demais para morrer de forma barata.

No centro da sala, Rashid al-Hariri negocia com oligarcas russos. O plano exige precisão.

• Se tirar de 1 a 2: o segurança do Rashid te nota.
• De 3 a 4: você chega perto, mas outro mafioso te intercepta.
• De 5 a 6: você planta a escuta sob o casaco do diplomata.

Digite: /salavip2
"""

salavip2 = """
[SALA VIP — PARTE 2]

A escuta transmite em tempo real. O embaixador revela onde será feita a troca da Lança de Salomão.

Você manda a localização para seu QG. A operação agora exige sincronização com a equipe do cofre.

É hora de agir.

Digite: /fuga
"""

fuga = """
[ROTA DE FUGA — FASE FINAL]

Explosões à distância. Sirenes. Gritos em dinamarquês.

• Se tirou pontos altos em todas as ações, sua máfia escapa com a lança e o embaixador.
• Se falhou em alguma parte, você é interceptado por mercenários rivais.

As ruas de Copenhague estão vermelhas.

A guerra começou.

Fim da missão.
"""

# Comandos

@bot.message_handler(commands=['start'])
def send_start(message):
    bot.reply_to(message, "Bem-vindo à Operação Raghnild.\nDigite /introducao para começar.")
    init_player(message.chat.id)

@bot.message_handler(commands=['introducao'])
def send_intro(message):
    init_player(message.chat.id)
    bot.reply_to(message, introducao)

@bot.message_handler(commands=['cofre1'])
def send_cofre1(message):
    bot.reply_to(message, cofre1)

@bot.message_handler(commands=['cofre2'])
def send_cofre2(message):
    chat_id = message.chat.id
    dado = rolar_dado()
    resultado = f"Você rolou: {dado}"

    if dado >= 4:
        resultado += "\nSucesso! A primeira camada foi quebrada."
        pontuar(chat_id, "Outfit", 2)
    else:
        resultado += "\nFalha! Um alarme silencioso foi ativado."
        pontuar(chat_id, "Camorra", 1)

    bot.reply_to(message, resultado + "\n\n" + cofre2)

@bot.message_handler(commands=['salavip1'])
def send_salavip1(message):
    chat_id = message.chat.id
    dado = rolar_dado()
    resultado = f"Você rolou: {dado}"

    if dado >= 5:
        resultado += "\nVocê plantou a escuta com sucesso."
        pontuar(chat_id, "Famiglia", 3)
    elif dado >= 3:
        resultado += "\nVocê chegou perto, mas foi interrompido por um rival."
        pontuar(chat_id, "Camorra", 1)
    else:
        resultado += "\nO segurança do Rashid te notou. Você precisa recuar."
        pontuar(chat_id, "Outfit", 1)

    bot.reply_to(message, resultado + "\n\n" + salavip1)

@bot.message_handler(commands=['salavip2'])
def send_salavip2(message):
    bot.reply_to(message, salavip2)

@bot.message_handler(commands=['fuga'])
def send_fuga(message):
    chat_id = message.chat.id
    total = sum(pontuacoes[chat_id].values())

    if total >= 5:
        final = "\nVocê escapa com tudo. Missão concluída com sucesso."
    else:
        final = "\nVocê foi interceptado. A missão falhou."

    bot.reply_to(message, fuga + final)

@bot.message_handler(commands=['pontuacaofinal'])
def pontuacao_final(message):
    chat_id = message.chat.id
    if chat_id not in pontuacoes:
        bot.send_message(chat_id, "Nenhuma pontuação registrada para este jogo.")
        return

    ranking = sorted(pontuacoes[chat_id].items(), key=lambda x: x[1], reverse=True)
    resultado = "*Resultado Final da Operação Raghnild:*\n\n"
    medalhas = ["1º lugar", "2º lugar", "3º lugar"]

    for i, (mafia, pontos) in enumerate(ranking):
        resultado += f"{medalhas[i]}: *{mafia}* — {pontos} pontos\n"

    resultado += f"\n*Domínio no submundo garantido por:* *{ranking[0][0]}*"

    bot.send_message(chat_id, resultado, parse_mode='Markdown')

# Flask
@app.route("/", methods=["POST"])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "OK", 200

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=os.getenv("RENDER_EXTERNAL_URL"))
    app.run(host="0.0.0.0", port=10000)