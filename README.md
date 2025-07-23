# 🤖 FIPE Telegram Bot

Um bot de Telegram que permite consultar preços de veículos direto da Tabela FIPE, de forma rápida e prática — sem precisar acessar sites ou instalar apps.

---

## 🧠 O que este bot faz?

Com ele, você pode:

- Ver a lista de marcas de veículos (ex: Fiat, Honda, Toyota...)
- Escolher um modelo e ano
- Receber o valor atualizado diretamente da **Tabela FIPE**
- Tudo isso **dentro do Telegram**, em uma conversa com o bot

---

## 💡 Tecnologias utilizadas

- **Python 3**
- **[python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)** – biblioteca para criar bots do Telegram
- **API pública da Tabela FIPE**

---

## 🧰 Como rodar o projeto no seu computador 

> ⚠️ Você precisa ter **Python 3 instalado**.  
> Se não tiver, baixe aqui: [https://www.python.org/downloads](https://www.python.org/downloads)

---

🔹 Passo 1 – Baixe os arquivos do projeto

Você pode clicar em **"Code > Download ZIP"** aqui no repositório:  
https://github.com/Allannomi/tabela-fipe-bot  
Depois, extraia o ZIP em alguma pasta no seu computador.

Ou, se você usa Git:

bash
git clone https://github.com/Allannomi/tabela-fipe-bot.git
cd tabela-fipe-bot

🔹 Crie um ambiente virtual
bash
python -m venv venv
Ative o ambiente:
Windows:
bash
venv\Scripts\activate
Linux/macOS:
bash
source venv/bin/activate

 Instale as dependências
Essas são as bibliotecas que o bot precisa para funcionar.

bash
pip install -r requirements.txt

Obtenha um Token do Bot no Telegram
Siga exatamente os passos abaixo:

No Telegram, procure por @BotFather (o bot oficial do Telegram para criar outros bots)

Clique em Iniciar

Digite o comando:

bash
/newbot
Ele vai pedir:

Nome do bot (ex: Tabela FIPE Bot)

Nome de usuário (precisa terminar com "bot", ex: meufipebot)

Ele vai te responder com algo assim:
Done! Use this token to access the HTTP API:
123456789:AAHkfa1Fjsdfjsdfj...

Crie um arquivo .env com seu token
Na pasta do projeto, crie um novo arquivo chamado .env
(coloque o ponto antes do nome).

Dentro dele, escreva assim:
TOKEN=123456789:AAHkfa1Fjsdfjsdfj...

Rode o bot
Execute o comando abaixo no terminal:
bash
python olabot.py
