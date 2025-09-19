from telebot import TeleBot
from telebot import types
from telebot.types import Message
import translators
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_TOKEN')

bot = TeleBot(TOKEN)

user_translator = {}
languages_translate_into = {
    "English": "en",
    "Spanish": "es",
    "Portuguese": "pt",
    "German": "de",
    "French": "fr",
    "Italian": "it",
}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    show_main_menu(message=message)

@bot.message_handler(func=lambda message: message.text in ['English', 'Spanish', 'Portuguese', 'German', 'French', 'Italian'])
def send_welcome(message):
    if message.from_user.id not in user_translator:
        user_translator[message.from_user.id] = {}

    user_translator[message.from_user.id]['language_translate_into'] = languages_translate_into[message.text]
    user_name = message.from_user.first_name
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Alibaba')
    itembtn2 = types.KeyboardButton('Baidu')
    itembtn3 = types.KeyboardButton('Bing')
    itembtn4 = types.KeyboardButton('Google')
    itembtn5 = types.KeyboardButton('MyMemory')
    itembtn6 = types.KeyboardButton('ModernMt')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6)
    bot.send_message(message.chat.id, f"{user_name.capitalize()}, please select which translater you want to use.", reply_markup=markup)
    return user_translator

@bot.message_handler(func=lambda message: message.text in ['Alibaba', 'Baidu', 'Bing', 'Google', 'MyMemory', 'ModernMt'])
def handle_translator(message):
    user_translator[message.from_user.id]['translator'] = message.text
    remove_markup = types.ReplyKeyboardRemove()
    bot.reply_to(message, f"Perfect! Now we are working with {message.text} translator. Please write what do you want to translate.", reply_markup=remove_markup)
    return user_translator

@bot.message_handler(func=lambda message: message.text not in ['Alibaba', 'Baidu', 'Bing', 'Google', 'MyMemory', 'ModernMt', 'Change translator'])
def translate_message(message):
    try:
        text_to_translate = message.text
        to_language = user_translator[message.from_user.id]['language_translate_into']
        translator = user_translator[message.from_user.id]['translator']
        translated_text = translators.translate_text(
            query_text = text_to_translate,
            translator = translator.lower(),
            from_language = 'auto',
            to_language = to_language
        )

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        itembtn1 = types.KeyboardButton('Change translator')
        markup.add(itembtn1)
        bot.reply_to(message, translated_text, reply_markup=markup)
    except Exception as e:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        itembtn1 = types.KeyboardButton('Change translator')
        markup.add(itembtn1)
        bot.reply_to(message, f"Unable to translate text. Error: {e}", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Change translator')
def start_again(message):
    remove_markup = types.ReplyKeyboardRemove()
    bot.reply_to(message, "Changing...", reply_markup=remove_markup)
    show_main_menu(message=message)

def show_main_menu(*, message: Message) -> None:
    user_name = message.from_user.first_name
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    itembtn1 = types.KeyboardButton('English')
    itembtn2 = types.KeyboardButton('Spanish')
    itembtn3 = types.KeyboardButton('Portuguese')
    itembtn4 = types.KeyboardButton('German')
    itembtn5 = types.KeyboardButton('French')
    itembtn6 = types.KeyboardButton('Italian')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6)
    bot.send_message(message.chat.id,f"{user_name.capitalize()}, welcome to Translater! Which language would you like to translate into?", reply_markup=markup)

bot.infinity_polling()