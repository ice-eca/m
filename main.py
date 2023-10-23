import telebot
from telebot import types
import re

TOKEN = '6611451445:AAHTjfg2wkR7Yd5OHfDFi3Z5eC07G9m46wk'

bot = telebot.TeleBot(TOKEN)

phone_number_regex = re.compile(r'^(\+7|8)\d{10}$')
age_regex = re.compile(r'^\d.*')
district_regex = re.compile(r'^\D.*')
data = {}
request_chat_id = '-4014020164'

@bot.message_handler(commands=['start'])
def enter_district(message):
    clear_data(message)
    data[message.chat.id] = {'stage':0}
    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton(text='Гагарина, 21', callback_data='Гагарина, 21')
    itembtn2 = types.InlineKeyboardButton(text='Восточная 3А', callback_data='Восточная 3А')
    
    markup.add(itembtn1, itembtn2)
    bot.send_message(message.chat.id, '\U0001F60A Школа программирования для детей KIBERone Березовский приветствует вас!\n \nНа этой неделе мы проводим бесплатный мастер-класс по программированию для детей 7-14 лет\n \nВаш ребенок создаст свой первый мультфильм и запрограммирует своего героя в игре Майнкрафт\n \nРасскажем, как избавить ребенка от игромании и научить компьютерной грамотности, чтобы подготовить к успешному будущему\n \nДлительность занятия 60 минут. Все необходимое предоставим. Ничего брать с собой не нужно.\n \nВыберите удобную для обучения локацию' , reply_markup=markup)

def enter_age(message):
    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton(text='6-8 лет', callback_data='6-8')
    itembtn2 = types.InlineKeyboardButton(text='9-11 лет', callback_data='9-11')
    itembtn3 = types.InlineKeyboardButton(text='12-14 лет', callback_data='12-14')
    markup.add(itembtn1, itembtn2, itembtn3)
    bot.send_message(message.chat.id, 'Пожалуйста, укажите возраст вашего ребенка',reply_markup=markup)


def enter_phone_number(message):
    bot.send_message(message.chat.id, 'Спасибо! Остался последний шаг\n \nПожалуйста, введите номер телефона, по которому мы можем с Вами связаться')
    
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
    if district_regex.match(data[message.chat.id]['district']) and age_regex.match(data[message.chat.id]['age']):
        bot.send_message(message.chat.id, 'Спасибо! Скоро с вами свяжется наш администратор, отправит вам расписание мастер-классов на ближайшую неделю и согласует точное время')
        bot.send_message(request_chat_id, 'Адрес ' + data[message.chat.id]['district']+' возраст '+data[message.chat.id]['age']+' '+data[message.chat.id]['phone_number'])
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
        if data[call.message.chat.id]['stage'] == 0:
            data[call.message.chat.id]['district'] = call.data
            data[call.message.chat.id]['stage'] = 1
            enter_age(call.message)
        elif data[call.message.chat.id]['stage'] == 1:
            data[call.message.chat.id]['age'] = call.data
            data[call.message.chat.id]['stage'] = 2
            enter_phone_number(call.message)
bot.infinity_polling()
