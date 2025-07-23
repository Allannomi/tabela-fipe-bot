# main.py
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from tabelafipe import obter_tabela, obter_modelos, obter_anos, obter_valor

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    print("Erro: TOKEN não encontrado.")
    exit()

# --- Handlers da Conversa ---

async def marcas(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Função de entrada, chamada com /start."""
    context.user_data.clear()
    await update.message.reply_text("Buscando as marcas, por favor aguarde...")

    lista_marcas = obter_tabela()
    if lista_marcas:
        resposta = "Marcas encontradas:\n\n"
        for marca in lista_marcas[:50]: # Limita a 50 para não sobrecarregar
            resposta += f"Código: {marca['codigo']} | Nome: {marca['nome']}\n"
        
        resposta += "\nEnvie o código da marca para ver os modelos."
        await update.message.reply_text(resposta)
        
        # Retorna 0 para ir para o próximo estado da conversa
        return 0
    else:
        await update.message.reply_text("Não consegui encontrar as marcas. Tente com /start.")
        return ConversationHandler.END

async def modelos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Recebe o código da marca e mostra os modelos."""
    codigo_marca = update.message.text
    context.user_data['codigo_marca'] = codigo_marca
    
    await update.message.reply_text(f"Buscando modelos para a marca {codigo_marca}...")

    dados = obter_modelos(codigo_marca)
    if dados and 'modelos' in dados and dados['modelos']:
        resposta = f"Modelos da marca {codigo_marca}:\n\n"
        for modelo in dados['modelos'][:50]: # Limita a 50
            resposta += f"Código: {modelo['codigo']} | Nome: {modelo['nome']}\n"
        
        resposta += "\nAgora, envie o código do modelo."
        await update.message.reply_text(resposta)
        
        # Retorna 1 para ir para o estado seguinte
        return 1
    else:
        await update.message.reply_text(f"Não encontrei modelos para a marca '{codigo_marca}'. Comece de novo com /start.")
        return ConversationHandler.END

async def anos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Recebe o código do modelo e mostra os anos."""
    codigo_modelo = update.message.text
    context.user_data['codigo_modelo'] = codigo_modelo
    codigo_marca = context.user_data['codigo_marca']

    await update.message.reply_text(f"Buscando os anos para o modelo {codigo_modelo}...")

    lista_anos = obter_anos(codigo_marca, codigo_modelo)
    if lista_anos:
        resposta = f"Anos do modelo {codigo_modelo}:\n\n"
        for ano in lista_anos:
            resposta += f"Código: {ano['codigo']} | Ano: {ano['nome']}\n"
        
        resposta += "\nPara ver o valor, envie o código do ano (ex: 2015-1)."
        await update.message.reply_text(resposta)
        
        # Retorna 2 para o próximo estado
        return 2
    else:
        await update.message.reply_text(f"Não encontrei os anos para o modelo '{codigo_modelo}'. Comece de novo com /start.")
        return ConversationHandler.END

async def valor(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Recebe o código do ano e mostra o valor final."""
    codigo_ano = update.message.text
    codigo_marca = context.user_data['codigo_marca']
    codigo_modelo = context.user_data['codigo_modelo']

    await update.message.reply_text("Consultando o valor do veículo...")

    dados_valor = obter_valor(codigo_marca, codigo_modelo, codigo_ano)
    if dados_valor:
        resposta = (
            f"Consulta Concluída!\n\n"
            f"Valor: {dados_valor.get('Valor', 'N/A')}\n"
            f"Marca: {dados_valor.get('Marca', 'N/A')}\n"
            f"Modelo: {dados_valor.get('Modelo', 'N/A')}\n"
            f"Ano Modelo: {dados_valor.get('AnoModelo', 'N/A')}\n"
            f"Combustível: {dados_valor.get('Combustivel', 'N/A')}\n"
            f"Código FIPE: {dados_valor.get('CodigoFipe', 'N/A')}\n"
            f"Mês de Referência: {dados_valor.get('MesReferencia', 'N/A')}"
        )
        await update.message.reply_text(resposta)
    else:
        await update.message.reply_text("Não foi possível encontrar o valor. Tente novamente com /start.")
    
    context.user_data.clear()
    return ConversationHandler.END

async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancela a operação."""
    context.user_data.clear()
    await update.message.reply_text("Operação cancelada. Digite /start para começar de novo.")
    return ConversationHandler.END

def main() -> None:
    """Função principal que executa o bot."""
    print("Criando a aplicação...")
    application = Application.builder().token(TOKEN).build()
    print("Bot em funcionamento.")

    # O ConversationHandler gerencia o fluxo da conversa
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", marcas)],
        states={
            0: [MessageHandler(filters.TEXT & ~filters.COMMAND, modelos)],
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, anos)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, valor)],
        },
        fallbacks=[CommandHandler("cancelar", cancelar)],
    )

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == "__main__":
    main()
