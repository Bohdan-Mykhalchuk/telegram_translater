from telebot import TeleBot
import translators

TOKEN = "7961804737:AAENDBOOUF3D8XsSfjoPepeUOo9hxhZimgI"

bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    print(message)
    bot.reply_to(message, "It works!")

@bot.message_handler(func=lambda message: True)
def translate_message(message):
    try:
        text_to_translate = message.text
        to_language = 'en'
        translated_text = translators.translate_text(
            query_text = text_to_translate,
            translator = 'google',
            from_language = 'auto',
            to_language = to_language
        )
        bot.reply_to(message, translated_text)
    except Exception as e:
        bot.reply_to(message, f"Не вдалось перекласти текст. Помилка {e}")

bot.infinity_polling()