import telebot
import requests
from django.core.management.base import BaseCommand
from telebot import types
from .token import TOKEN

bot_token = TOKEN
bot = telebot.TeleBot(bot_token)

def webAppKeyboard(link):
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    webAppTest = types.WebAppInfo(link)
    one_butt = types.KeyboardButton(text="Go to website", web_app=webAppTest)
    keyboard.add(one_butt)

    return keyboard

def send_full_info_to_user(tel_id, data):
    bot.send_message(tel_id, data, reply_markup=types.ReplyKeyboardRemove(selective=True))

user = {}

# Function to check if the bot is active
def is_bot_active():
    response = requests.get('https://findemail.pythonanywhere.com/api-v1/check_bot').json()
    return response['is_active']

# Handler for inactive bot
if not is_bot_active():
    @bot.message_handler(func=lambda message: True)
    def handle_message_if_inactive(message):
        bot.reply_to(message, "Sorry, the bot is currently inactive.")

@bot.message_handler(commands=['start'])
def start(message):
    if not is_bot_active():
        return
    bot.reply_to(message, "Hello! Please, provide your email")
    bot.register_next_step_handler(message, check_email)

def check_email(message):
    if message.text == '/start':
        return

    if not is_bot_active():
        return

    response = requests.get(f'https://findemail.pythonanywhere.com/api-v1/check/{message.text}/{message.chat.id}')
    response_dict = response.json()

    if response.status_code == 200:
        bot.reply_to(message, f'{response_dict["success"]}\n to see more information, please click the button below and confirm your email', reply_markup=webAppKeyboard("https://findemail.pythonanywhere.com"))
    else:
        bot.reply_to(message, response_dict['error'])

class Command(BaseCommand):
    help = 'Implemented Django application telegram bot setup command'

    def handle(self, *args, **kwargs):
        bot.enable_save_next_step_handlers()
        bot.load_next_step_handlers()
        bot.infinity_polling()
