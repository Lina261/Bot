import telebot
from telebot import types


bot = telebot.TeleBot(TOKEN)
mood = {'fun': 'Веселое', 'angry': 'Злое', 'sad': 'Грустное', 'anxious': 'Тревожное', 'depressed': 'Подавленное',
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


bot.polling()
