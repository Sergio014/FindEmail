import telebot
import requests
import json
from django.core.management.base import BaseCommand
from telebot import types
from .token import TOKEN
# initialize bot using it token
bot_token = TOKEN
bot = telebot.TeleBot(bot_token)

# some russian
def webAppKeyboard(link): #создание клавиатуры с webapp кнопкой
   keyboard = types.ReplyKeyboardMarkup(row_width=1) #создаем клавиатуру
   webAppTest = types.WebAppInfo(link) #создаем webappinfo - формат хранения url
   one_butt = types.KeyboardButton(text="Go to website", web_app=webAppTest) #создаем кнопку типа webapp
   keyboard.add(one_butt) #добавляем кнопки в клавиатуру

   return keyboard

user = {}

@bot.message_handler(commands=['start'])
# if user send /start command
def start(message):
    bot.reply_to(message, "Hello! Please provide your email")
    bot.register_next_step_handler(message, check_email) # connect another handler to check response of user

def check_email(message):
    # spam protection
    if message.text == '/start':
        return
    # checking through API
    response = requests.get(f'https://findemail.pythonanywhere.com/api-v1/check/{message.text}')
    response_dict = response.json()
    # if all is OK
    if response.status_code == 200:
        bot.reply_to(message, f'{response_dict["success"]}\n to see mo information please click button below and confirm your email', reply_markup=webAppKeyboard("https://findemail.pythonanywhere.com"))
    else:
        bot.reply_to(message, response_dict['error'])

class Command(BaseCommand):
    help = 'Implemented to Django application telegram bot setup command'

    def handle(self, *args, **kwargs):
            bot.enable_save_next_step_handlers()
            bot.load_next_step_handlers()
            bot.infinity_polling()

