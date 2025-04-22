import os
import json
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# Pega o token e a URL do webhook
TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")  # ex: 'https://seu-app.onrender.com/webhook'

app = Flask(__name__)
application = ApplicationBuilder().token(TOKEN).build()

# Exemplo de pontuação simulada
pontuacoes = {}

# Comandos
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(f"Bem-vindo, {user.first_name}! Missão iniciada.")
    # Pode colocar Cena 1 aqui também

async def pontuacao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    pontos = pontuacoes.get(user_id, 0)
    await update.message.reply_text(f"Sua pontuação atual: {pontos} pontos.")

# Cena exemplo
async def cena2_parte2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Cena 2 - Parte 2:\n\n"
        "Enquanto os mafiosos se encaram com armas apontadas, o som da sirene da polícia começa a ecoar ao fundo. "
        "Você precisa decidir rapidamente: confrontar as máfias ou escapar com a lança?"
    )

# Fallback para mensagens comuns
async def fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Comando não reconhecido. Use /start para começar.")

# Adiciona os handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("pontuacao", pontuacao))
application.add_handler(CommandHandler("cena2_parte2", cena2_parte2))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fallback))

# Rota raiz só pra teste
@app.route('/')
def index():
    return 'Bot está rodando!'

# Webhook
@app.route('/webhook', methods=['POST'])
async def webhook():
    if request.method == "POST":
        data = request.get_json(force=True)
        update = Update.de_json(data, application.bot)
        await application.process_update(update)
        return "ok"
    return "método não permitido", 405

# Configura o webhook assim que o app inicia
async def setup_webhook():
    await application.bot.delete_webhook()
    await application.bot.set_webhook(url=WEBHOOK_URL)

if __name__ == '__main__':
    import asyncio

    async def main():
        await setup_webhook()
        app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

    asyncio.run(main())