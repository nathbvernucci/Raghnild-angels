from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Pontuação oculta
pontuacao = {
    "Outfit": 0,
    "Camorra": 0,
    "Famiglia": 0
}

# Cena 1 - Introdução
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Copenhague, Dinamarca.\n"
        "Você acaba de pousar. A névoa cobre o teto do Palácio Marienborg, onde o maior leilão clandestino da Europa está prestes a começar.\n\n"
        "As três máfias mais perigosas do submundo americano desembarcaram com o mesmo objetivo:\n"
        "• Roubar a Lança de Salomão.\n"
        "• Sequestrar o Embaixador Rashid al-Hariri.\n\n"
        "Quem controlar um domina o mercado negro.\n"
        "Quem controlar os dois garante uma nova aliança e poder no submundo.\n\n"
        "Quem é você nessa guerra?\n\n"
        "Escolha sua máfia:\n• Outfit (Chicago)\n• Camorra (Las Vegas)\n• Famiglia (Nova York)"
    )

# Cena 2 - Cofre (parte 1)
async def cofre(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Palácio Marienborg – Subsolo\n"
        "Você desce silenciosamente por um corredor de mármore. Câmeras ocultas, sensores de calor e dois guardas vigiam o cofre subterrâneo.\n\n"
        "A Lança de Salomão está a poucos metros de você.\n"
        "Cada máfia escolheu um método:\n"
        "- Outfit hackeia os sensores\n"
        "- Camorra suborna os seguranças\n"
        "- Famiglia cria um blefe para desviar a atenção\n\n"
        "As ações geram tensão. Quem age rápido, ganha vantagem."
    )
    pontuacao["Outfit"] += 1
    pontuacao["Camorra"] += 1
    pontuacao["Famiglia"] += 1

# Cena 2 - Cofre (parte 2)
async def cofre_parte2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "O cofre se abre com um estalo metálico.\n"
        "Alarme silencioso é ativado. O tempo começa a correr.\n\n"
        "- Outfit remove a lança usando uma maleta forrada com chumbo.\n"
        "- Camorra causa uma explosão de distração.\n"
        "- Famiglia planta evidências para incriminar os rivais.\n\n"
        "Os corredores agora ecoam passos acelerados. A segurança está em alerta.\n"
        "Cada decisão tem seu preço."
    )
    pontuacao["Outfit"] += 2
    pontuacao["Camorra"] += 2
    pontuacao["Famiglia"] += 2

# Cena 3 - Sala VIP (parte 1)
async def sala_vip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Salão Imperial – 22h10\n"
        "Rashid al-Hariri faz um brinde.\n"
        "A sala está cheia de figuras perigosas.\n\n"
        "- Outfit se infiltra como segurança.\n"
        "- Camorra causa pânico usando gás lacrimogêneo.\n"
        "- Famiglia manipula a tecnologia da sala para apagar as luzes.\n\n"
        "A confusão começa. O alvo está isolado.\n"
        "Quem agiu melhor, tem o embaixador nas mãos."
    )
    pontuacao["Outfit"] += 1
    pontuacao["Camorra"] += 2
    pontuacao["Famiglia"] += 1

# Cena 3 - Sala VIP (parte 2)
async def sala_vip_parte2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Tiros. Gritos. Alarmes. O caos está instalado.\n\n"
        "- A Camorra rende Rashid com uma seringa no pescoço.\n"
        "- A Famiglia tenta negociar com o motorista do embaixador.\n"
        "- A Outfit já está no elevador com um refém parecido.\n\n"
        "Cada segundo conta. Quem escapar primeiro com ele vivo, ganha acesso às rotas diplomáticas."
    )
    pontuacao["Camorra"] += 2
    pontuacao["Famiglia"] += 1
    pontuacao["Outfit"] += 1

# Cena Final - Fuga
async def final(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Copenhague em chamas.\n"
        "O aeroporto foi fechado. Embaixadas negam envolvimento.\n\n"
        "- Outfit foge em helicóptero de guerra pela costa.\n"
        "- Camorra usa túneis subterrâneos até o porto.\n"
        "- Famiglia se esconde em um comboio diplomático.\n\n"
        "Agora, só resta saber quem venceu a guerra silenciosa do submundo..."
    )

# Comando para mostrar pontuação (somente se quiser)
async def pontuacao_atual(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    texto = "\n".join([f"{mafia}: {pontos} pontos" for mafia, pontos in pontuacao.items()])
    await update.message.reply_text(f"Pontuação atual:\n\n{texto}")

# Inicializa o bot
if __name__ == "__main__":
    import os
    from telegram.ext import Application

    TOKEN = "7970673691:AAEQxRN8EBJsMoF2ANYtEpNR8YHZwhjr6zQ"

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("Cofre", cofre))
    app.add_handler(CommandHandler("Cofre2", cofre_parte2))
    app.add_handler(CommandHandler("SalaVIP", sala_vip))
    app.add_handler(CommandHandler("SalaVIP2", sala_vip_parte2))
    app.add_handler(CommandHandler("Final", final))
    app.add_handler(CommandHandler("Pontuacao", pontuacao_atual))

    print("Bot iniciado...")
    app.run_polling()
