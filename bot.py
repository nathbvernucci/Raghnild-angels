import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio

# Configuração de logging
logging.basicConfig(level=logging.INFO)

# Pontuação oculta
pontuacao_mafias = {
    'Outfit': 0,
    'Camorra': 0,
    'Famiglia': 0
}

# Funções de comandos
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = """
Copenhague, Dinamarca.
Você acaba de pousar. A névoa cobre o teto do Palácio Marienborg, onde o maior leilão clandestino da Europa está prestes a começar.

As três máfias mais perigosas do submundo americano desembarcaram na Europa com o mesmo objetivo:
• Roubar a Lança de Salomão, símbolo de poder oculto e a relíquia mais requisitada do leilão. 
• Sequestrar o Embaixador Rashid al-Hariri, peça-chave de uma nova era geopolítica.

Quem controlar um domina o mercado negro. 
Quem controlar os dois garante uma nova aliança e poder no submundo. 

Quem é você nessa guerra?
Escolha a sua máfia:
• Outfit
• Camorra
• Famiglia
"""
    await update.message.reply_text(texto)

async def cofre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = """
[Cena 2 – Parte 1: Cofre Subterrâneo]

22h00.

O leilão começa. A Lança de Salomão será exibida em minutos.  
Enquanto os convidados brindam champanhe, agentes infiltrados das três máfias acessam corredores restritos.

Sensores, armadilhas, códigos.  
Três caminhos, três planos distintos.

• Outfit hackeia o sistema de vigilância e desativa alarmes.  
• Camorra seduz um funcionário para obter o acesso biométrico.  
• Famiglia planta explosivos de precisão nos dutos de ventilação.

A tensão cresce. O cofre se aproxima.

[Cena 2 – Parte 2: Confronto no Cofre]

Portas blindadas se abrem. A Lança brilha no pedestal.  
Mas há um problema: todos chegaram ao mesmo tempo.

Tiros. Luzes piscam. Sirenes soam.  
Cada máfia tenta garantir a relíquia enquanto lida com a presença das outras duas.

• Outfit pega a lança e tenta fugir pelos túneis.  
• Camorra tenta explodir a saída secundária.  
• Famiglia bloqueia a escada com fogo.

Quem sai com a lança? Quem fica ferido?  
O caos decide.

(Pontuação aplicada conforme a escolha de cada máfia.)
"""
    await update.message.reply_text(texto)
    pontuacao_mafias["Outfit"] += 2
    pontuacao_mafias["Camorra"] += 1
    pontuacao_mafias["Famiglia"] += 3

async def salavip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = """
[Cena 3 – Parte 1: Sala VIP]

O Embaixador Rashid al-Hariri faz um brinde com magnatas russos.  
Ao redor, agentes da Interpol disfarçados e seguranças armados.

As máfias se preparam.

• Outfit usa gás sonífero no sistema de ar.  
• Camorra invade como convidados e causa tumulto.  
• Famiglia sequestra um assessor e troca de identidade.

O embaixador é isolado. Mas a resposta é rápida.

[Cena 3 – Parte 2: Explosão de Conflito]

Alarmes tocam. As luzes se apagam.

• Outfit é descoberta, mas já tem o embaixador sedado.  
• Camorra troca tiros com seguranças.  
• Famiglia domina a sala de controle e bloqueia as portas.

O tempo corre.  
Três mafias com um refém valioso.  
Só uma vai escapar com ele.

(Cena 3 – Parte 3: Fuga)

• Outfit foge de helicóptero do terraço.  
• Camorra escapa pelo subsolo, usando um barco.  
• Famiglia aciona um carro blindado no portão principal.

Drones seguem cada rota. A perseguição é cinematográfica.

(Pontuação secreta aplicada.)
"""
    await update.message.reply_text(texto)
    pontuacao_mafias["Outfit"] += 3
    pontuacao_mafias["Camorra"] += 2
    pontuacao_mafias["Famiglia"] += 1

async def final(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = """
[Final da Missão – O Destino]

A noite termina com helicópteros militares sobrevoando o palácio.  
O mundo amanhece com manchetes de um atentado diplomático.

Mas... alguém conseguiu os dois alvos?

A máfia com mais pontos detém:
• A Lança de Salomão
• O Embaixador Rashid al-Hariri

Um novo império do submundo será fundado.

A guerra mal começou.
"""
    await update.message.reply_text(texto)

async def pontuacao_atual(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = "**Pontuação Final (oculta até o final da missão):**\n"
    for mafia, pontos in pontuacao_mafias.items():
        texto += f"{mafia}: {pontos} pontos\n"
    await update.message.reply_text(texto)

# Execução principal
async def main():
    application = ApplicationBuilder().token("7970673691:AAEQxRN8EBJsMoF2ANYtEpNR8YHZwhjr6zQ").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("cofre", cofre))
    application.add_handler(CommandHandler("salavip", salavip))
    application.add_handler(CommandHandler("final", final))
    application.add_handler(CommandHandler("pontuacao", pontuacao_atual))

    await application.run_polling()

import asyncio

if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except RuntimeError:
        # Se o loop já estiver rodando, usa esse fallback
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())