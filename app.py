import telebot
from config import keys, TOKEN
from Utils import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start','help'])
def help(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Чтобы начать работу, введите команду боту в следующем формате: <имя валюты, цену \
которой он хочет узнать> <имя валюты, в которой надо узнать цену первой валют> <количество первой валюты>. \
Ввод осуществлять через пробел, запись валюты в единственном числе.\nУвидеть список всех доступных валют: /value ")

@bot.message_handler(commands=['value'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(" ")

        if len(values) != 3:
            raise ConvertionException('Введены неверные параметры')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать \n {e}')

bot.polling()
