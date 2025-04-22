from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask, request
import os

# Aqui o bot vai receber o token do Telegram, você pode colocar o seu token aqui
TELEGRAM_TOKEN = '7970673691:AAEQxRN8EBJsMoF2ANYtEpNR8YHZwhjr6zQ'

# Inicializando o Flask
app = Flask(__name__)

# Funções para o bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Copenhague, Dinamarca.\n"
        "Você acaba de pousar. A névoa cobre o teto do Palácio Marienborg, onde o maior leilão clandestino da Europa está prestes a começar.\n\n"
        "As três máfias mais perigosas do submundo americano desembarcaram na Europa com o mesmo objetivo:\n"
        "• Roubar a Lança de Salomão, símbolo de poder oculto e a relíquia mais requisitada do leilão.\n"
        "• Sequestrar o Embaixador Rashid al-Hariri, peça-chave de uma nova era geopolítica.\n\n"
        "Quem controlar um domina o mercado negro.\n"
        "Quem controlar os dois garante uma nova aliança e poder no submundo.\n\n"
        "Quem é você nessa guerra?\n\n"
        "Escolha a sua máfia:\n"
        "• Outfit\n"
        "• Camorra\n"
        "• Famiglia"
    )

async def cofre(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Você chega à entrada do cofre subterrâneo. A segurança aqui é implacável, com sensores e guardas a cada esquina. A Lança de Salomão está em seu interior, aguardando a grande revelação no leilão.\n\n"
        "O tempo está contra você. Em menos de uma hora, o leilão começa, e a obra será exposta ao público.\n"
        "A chave para o sucesso é o fator surpresa.\n\n"
        "Como você procede?"
    )

async def cofre_parte2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Você se infiltra no cofre. O local é silencioso e frio. O brilho dourado da Lança de Salomão reflete em uma vitrine segura, guardada por câmeras de segurança e alarmes.\n\n"
        "Você se prepara para agir, mas a tensão no ar é palpável. O sistema de segurança pode ser desligado, mas isso pode ativar uma reação em cadeia...\n\n"
        "É sua hora de fazer a jogada decisiva. O que você fará?"
    )

async def sala_vip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Você entra na **Sala VIP**. O luxo é evidente, mas a tensão também. O **Embaixador Rashid al-Hariri** está cercado de seguranças e assessores, com um sorriso falso no rosto. Ele sabe que o leilão é um jogo de poder, e você está pronto para roubá-lo dessa mesa.\n\n"
        "A missão de sequestrar o Embaixador está em seus pensamentos, mas uma distração pode mudar tudo.\n\n"
        "Como você vai abordar o Embaixador? Qual será o seu próximo movimento?"
    )

async def sala_vip_parte2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "A tensão está crescendo na **Sala VIP**. Você nota os seguranças se aproximando cada vez mais do **Embaixador**. Ele parece cada vez mais desconfortável e alerta.\n\n"
        "Uma abordagem direta pode ser arriscada, mas também pode ser a chave para o sucesso.\n\n"
        "Tudo pode mudar em um segundo. Está na hora de agir ou esperar?"
    )

async def final(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Você conseguiu sequestrar o **Embaixador** e agora precisa escapar.\n\n"
        "A fuga será tensa: você pode escolher usar o **Embaixador** como barganha, ou tentar uma fuga direta com ele em sua posse.\n\n"
        "A hora é agora. O que você fará? Sua vida e futuro dependem dessa decisão!"
    )

async def pontuacao_atual(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    texto = "\n".join([f"{mafia}: {pontos} pontos" for mafia, pontos in pontuacao.items()])
    await update.message.reply_text(f"Pontuação atual:\n\n{texto}")

# Função para o webhook do Flask
@app.route("/webhook", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = Update.de_json(json_str)
    application.process_update(update)
    return "ok", 200

# Inicializando o bot no Telegram
async def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("Cofre", cofre))
    application.add_handler(CommandHandler("Cofre2", cofre_parte2))
    application.add_handler(CommandHandler("SalaVIP", sala_vip))
    application.add_handler(CommandHandler("SalaVIP2", sala_vip_parte2))
    application.add_handler(CommandHandler("Final", final))
    application.add_handler(CommandHandler("Pontuacao", pontuacao_atual))

    await application.run_polling()

if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())