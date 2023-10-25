import telebot
from telebot import types
import re

TOKEN = '6975023482:AAHWC_T5FXtONkKnCpZPPXVpGErWRdXO29Q'

bot = telebot.TeleBot(TOKEN)

phone_number_regex = re.compile(r'^(\+7|8)\d{10}$')
age_regex = re.compile(r'^\d.*')
district_regex = re.compile(r'^\D.*')
data = {}
request_chat_id = '-4067267677'

@bot.message_handler(commands=['start'])
def enter_district(message):
    clear_data(message)
    data[message.chat.id] = {'stage':1}
    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton(text='6-8 лет', callback_data='6-8')
    itembtn2 = types.InlineKeyboardButton(text='9-11 лет', callback_data='9-11')
    itembtn3 = types.InlineKeyboardButton(text='12-14 лет', callback_data='12-14')
    markup.add(itembtn1, itembtn2, itembtn3)
    bot.send_photo(message.chat.id, open('kiber1.png', 'rb'))
    bot.send_message(message.chat.id, 'Школа программирования для детей KIBERone на Компрессорном приветствует вас!\U0001F60A\n \nНа этой неделе мы проводим бесплатный мастер-класс по программированию для детей 7-14 лет\U0001F4BB\n \n\U00002705Ваш ребенок создаст свой первый мультфильм и запрограммирует своего героя в игре Майнкрафт\U0001F5A5\n \n\U00002705Расскажем, как избавить ребенка от игромании и научить компьютерной грамотности, чтобы подготовить к успешному будущему\n \n\U00002705Длительность занятия 60 минут. Все необходимое предоставим. Ничего брать с собой не нужно.\n \n\U0001F4CDЗанятия будут проходить по адресу: ул. Латвийская, 19 КСК "Олимп"' )
    bot.send_message(message.chat.id, 'Пожалуйста, укажите возраст вашего ребенка',reply_markup=markup)

def enter_phone_number(message):
    bot.send_message(message.chat.id, 'Пожалуйста, введите номер телефона, по которому мы можем с Вами связаться')
    
@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text.startswith('/start'):
        return
    if message.text.startswith('/getID'):
        bot.send_message(message.chat.id, message.chat.id)
        return
    if message.text.startswith('/'):
        bot.send_message(message.chat.id, 'Неверная команда')
        return
    if phone_number_regex.match(message.text) and data[message.chat.id]['stage'] == 2:
        data[message.chat.id]['phone_number'] = message.text
        data[message.chat.id]['stage'] = 3
        check_and_send(message)
        return
    else:
        bot.send_message(message.chat.id, 'Повторите попытку')
        return

def check_and_send(message):
    if age_regex.match(data[message.chat.id]['age']):
        bot.send_message(message.chat.id, 'Спасибо! Скоро с вами свяжется администратор!')
        bot.send_message(request_chat_id,'Возраст '+data[message.chat.id]['age']+' тел: '+data[message.chat.id]['phone_number'])
        clear_data(message)
    else:
        bot.send_message(message.chat.id, 'Неправильно сформированы ответы на вопросы, поробуйте еще раз')
        enter_district(message)
    
def clear_data(message):
    if message.chat.id in data:
        del data[message.chat.id]
  
@bot.callback_query_handler(func=lambda call: True)
def answering(call):
    if call.message.chat.id in data:
        if data[call.message.chat.id]['stage'] == 1:
            data[call.message.chat.id]['age'] = call.data
            data[call.message.chat.id]['stage'] = 2
            enter_phone_number(call.message)
bot.infinity_polling()
