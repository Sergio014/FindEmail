import json
import telebot
import requests
from django.core.management.base import BaseCommand
from telebot import types
from .token import TOKEN
from .spam_protection import check_message_count

# initialize bot using it token
bot = telebot.TeleBot(TOKEN)

# some russian
def webAppKeyboard(message): #создание клавиатуры с webapp кнопкой
   keyboard = types.ReplyKeyboardMarkup(row_width=1) #создаем клавиатуру
   webAppTest = types.WebAppInfo(f"https://sergio014.github.io/FindEmail/webapp.html") #создаем webappinfo - формат хранения url
   one_butt = types.KeyboardButton(text="Go to web app", web_app=webAppTest) #создаем кнопку типа webapp
   keyboard.add(one_butt) #добавляем кнопки в клавиатуру

   return keyboard

def delete_message_from_user(tel_id, message_id):
    bot.delete_message(tel_id, message_id)

def send_full_info_to_user(tel_id, data):
    from api.models import NotificationHistory
    message = bot.send_message(tel_id, data)
    NotificationHistory.objects.create(text=data, telegram_id=tel_id, message_id=message.id)

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
    bot.reply_to(message, "Hello! You can go to our website and choose what i can find", reply_markup=webAppKeyboard(message))
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

@bot.message_handler(commands=['history'])
# if user send /start command
def history(message):
    from api.models import NotificationHistory
    if check_message_count(message.chat.id):
        return
    bot.reply_to(message, "Hello! Here is your notifications history:")
    for notification in NotificationHistory.objects.filter(telegram_id=message.chat.id):
        bot.send_message(notification.telegram_id, f"Text: {notification.text}\n Date of sending: {notification.date_of_sending}")
    bot.reply_to(message, "Please rate our app fom 1 to 5")
    bot.register_next_step_handler(message, get_stars)

def get_stars(message):
    rating = message.text
    requests.post('https://findemail.pythonanywhere.com/api-v1/add_rating', data={'stars': rating})

@bot.message_handler(content_types="web_app_data") 
def answer(webAppMes):
    bot.send_message(webAppMes.chat.id, f"Data succesfully catched, waiting for server response...")
    data = json.loads(webAppMes.web_app_data.data)
    data_for_api = {
        "telegram_id": webAppMes.from_user.id,
        "data": data['data'],
        "email": data.get('email', False),
        "hwid": data.get('hwid', False),
    }
    response = requests.post('https://findemail.pythonanywhere.com/api-v1/check_data', data=data_for_api)
    if response.status_code == 404:
        bot.send_message(data_for_api['telegram_id'], response.json()['error'])

class Command(BaseCommand):
    help = 'Implemented to Django application telegram bot setup command'

    def handle(self, *args, **kwargs):
            print('All works')
            bot.infinity_polling()

