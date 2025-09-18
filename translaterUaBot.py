from telebot import TeleBot
from telebot import types
import translators
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_TOKEN')

bot = TeleBot(TOKEN)

user_translators = {}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user_name = message.from_user.first_name
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Alibaba')
    itembtn2 = types.KeyboardButton('Bing')
    itembtn3 = types.KeyboardButton('Deep')
    itembtn4 = types.KeyboardButton('Google')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    bot.send_message(message.chat.id, f"{user_name.capitalize()} welcome to Translater! Please select which translater you want to use", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ['Alibaba', 'Bing', 'Deep', 'Google'])
def handle_translator(message):
    user_translators[message.from_user.id] = message.text
    remove_markup = types.ReplyKeyboardRemove()
    bot.reply_to(message, f"Perfect! Now we are working with {message.text} translator", reply_markup=remove_markup)

@bot.message_handler(func=lambda message: message.text not in ['Alibaba', 'Bing', 'Deep', 'Google'])
def translate_message(message):
    try:
        text_to_translate = message.text
        to_language = 'en'
        translator = user_translators[message.from_user.id]
        translated_text = translators.translate_text(
            query_text = text_to_translate,
            translator = translator.lower(),
            from_language = 'auto',
            to_language = to_language
        )
        bot.reply_to(message, translated_text)
    except Exception as e:
        bot.reply_to(message, f"Не вдалось перекласти текст. Помилка {e}")

bot.infinity_polling()