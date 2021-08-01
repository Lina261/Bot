from PIL import Image
from telebot import TeleBot
from telebot import types
import requests
import shutil

from io import BytesIO

cats_url = 'https://cataas.com/cat'

bot = TeleBot()
mood = {'angry': 'Злое', 'sad': 'Грустное', 'anxious': 'Тревожное', 'depressed': 'Подавленное',
        'joyful': 'Радостное', 'calm': 'Спокойное'}


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.send_message(message.from_user.id, 'Привет! Как тебя зовут?')
    bot.register_next_step_handler(message, ask_about_mood)


def ask_about_mood(message):
    name = message.text
    keyboard = types.InlineKeyboardMarkup()
    for k, v in mood.items():
        keyboard.add(types.InlineKeyboardButton(text=v, callback_data=k))
    bot.send_message(message.from_user.id, f'{name}, какое у тебя сегодня настроение?', reply_markup=keyboard)

    @bot.callback_query_handler(func=lambda call: True)
    def callback_worker(call):
        print(call.data)
        response = requests.get(cats_url)
        img = Image.open(BytesIO(response.content))
        bot.send_photo(photo=img, chat_id=call.message.chat.id, caption=generate_advice(call.data))

    def generate_advice(user_mood):
        print(user_mood)


bot.polling()