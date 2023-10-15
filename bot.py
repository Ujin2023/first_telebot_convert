import telebot
from config import keys, TOKEN
from utils import Converter, ConvertionExeption
import requests

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands= ["start"])
def instruction(message):
    text = f"Приветствую тебя, {message.chat.username}!\n" \
f"Бот конвертатор - поможет тебе узнать актуальный курс валюты.\n" \
"Просто отправь ему данные в следующем формате:\n" \
"<в какую валюту перевести> \n" \
"<какую валюту перевести> \n" \
"<количество переводимой валюты>\n" \
"Пример: Рубль Доллар 6\n" \
"Список доступных валют: /currency\n" \
"Для уточнения актуального курса валют в рублях введите: /curs\n" \
"Для вызова меню: /help"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands= ["help"])
def help(message):
    text = "Для конвертации валюты введите данные в следующем формате:\n" \
           "<в какую валюту перевести> \n" \
           "<какую валюту перевести> \n" \
           "<количество переводимой валюты>\n" \
           "Список доступных валют: /currency\n" \
           "Для уточнения актуального курса в рублях введите: /curs"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=["currency"])
def currency(message):
    text = "Доступные валюты:"
    text = "\n".join(keys)
    bot.reply_to(message, text)

@bot.message_handler(commands = ["curs"])
def curs(message):
    text = "Выберете интересующую валюту:"
    text = "\n/".join(keys.values())
    bot.reply_to(message, text)

@bot.message_handler(commands= ["USD", "EUR", "CNY"])
def today_curs(message):
    try:
        message_text = message.text
        message_text = message.text[1:]
        r = requests.get("https://www.cbr-xml-daily.ru/daily_json.js").json()
        tcurs = r["Valute"][f"{message_text}"]["Value"]
    except ConvertionExeption as e:
        bot.reply_to(message, f"Не удалось обработать запрос\n {e}")
    else:
        otvet = f"Один {message_text} стоит {tcurs} рублей"
        bot.reply_to(message, otvet)

@bot.message_handler(content_types = ["text"])
def converter(message):
    try:
        values = message.text.lower().split(" ")
        if len(values) != 3:
            raise ConvertionExeption("Недостаточно пармаетров.")

        quote, base, amount = values
        total_data = Converter.converter(quote, base, amount)
    except ConvertionExeption as e:
        bot.reply_to(message, f"Не удалось обработать запрос\n {e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать запрос\n {e}")
    else:
        otvet = f"Цена {amount} {base} в {quote} = {total_data}"
        bot.reply_to(message, otvet)

bot.polling()