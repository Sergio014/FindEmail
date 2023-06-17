import telebot
import requests
from django.core.management.base import BaseCommand
from telebot import types
from .token import TOKEN
from .spam_protection import check_message_count


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

def send_full_info_to_user(tel_id, data):
    bot.send_message(tel_id, data, reply_markup=types.ReplyKeyboardRemove(selective=True))

user = {}

# response = requests.get('https://findemail.pythonanywhere.com/api-v1/check_bot').json()

# # if bot is inactive stop replaying to any messages
# if not response['is_active']:
#     @bot.message_handler(func=lambda message: True)
#     def handle_message_if_inactive():
#         pass

@bot.message_handler(commands=['start'])
# if user send /start command
def start(message):
    if check_message_count(message.chat.id):
        return
    bot.reply_to(message, "Hello! You can go to our website and choose what i can find", reply_markup=webAppKeyboard(f"https://findemail.pythonanywhere.com/{message.chat.id}"))
    # bot.register_next_step_handler(message, check_email) # connect another handler to check response of user

# def check_email(message):
#     # spam protection
#     if check_message_count(message.chat.id):
#         return
#     if message.text == '/start':
#         return
#     # checking through API
#     response = requests.get(f'https://findemail.pythonanywhere.com/api-v1/check/{message.text}/{message.chat.id}')
#     response_dict = response.json()
#     # if all is OK
#     if response.status_code == 200:
#         bot.reply_to(message, f'{response_dict["success"]}\n to see mo information please click button below and confirm your email', reply_markup=webAppKeyboard("https://findemail.pythonanywhere.com"))
#     else:
#         bot.reply_to(message, response_dict['error'])

class Command(BaseCommand):
    help = 'Implemented to Django application telegram bot setup command'

    def handle(self, *args, **kwargs):
            bot.enable_save_next_step_handlers()
            bot.load_next_step_handlers()
            bot.infinity_polling()

