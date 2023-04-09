import telebot

bot = telebot.TeleBot('6271128564:AAHGIdO8qTc7Ykp0_H4HCR9L7pdo74JpGA4')


# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, "Привет ✌️ ")


@bot.message_handler(commands=['button'])
def button_message(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Кнопка")
    markup.add(item1)




# Обрабатывается все документы и аудиозаписи
@bot.message_handler(content_types=['text'])
def handle_docs_audio(message):
    bot.reply_to(message, "This is a message handler")

bot.polling(none_stop=True)