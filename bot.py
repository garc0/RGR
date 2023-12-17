import telebot
import sqlite3
import numpy as np
import pandas as pd
from telebot import types


TOKEN = "6685029885:AAFa5RURuqztb7aGigWN8qc0Fyw_cUTBUxs"
bot = telebot.TeleBot(TOKEN)
df = pd.read_csv('text.csv')
keyboard = types.InlineKeyboardMarkup(row_width=3)

BPMN_button = types.InlineKeyboardButton('Диаграмма BPMN', callback_data='bpmn')
dashboard_button = types.InlineKeyboardButton('Дашборд', callback_data='dashboard')
find_item_button = types.InlineKeyboardButton('Проверить товар', callback_data='lookforitem')
about_bot_button = types.InlineKeyboardButton('Функции бота', callback_data='about_bot')
help_button = types.InlineKeyboardButton('Помощь', callback_data='help')
order_button = types.InlineKeyboardButton('Оформить заказ', callback_data='order')
keyboard.add(BPMN_button, help_button, about_bot_button, find_item_button,dashboard_button, order_button)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Привет! Этот бот для регистрации внутренней логистики.'
                        'Тут можно создавать запросы на заказ, регистрировать пользователя, генерировать смотреть отчетность. ')
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=keyboard)

@bot.message_handler(commands=['help'])
def help(message):   
   
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=keyboard)

# Ответ на запрос о создателе
def About_(message):
    bot.reply_to(message, 'В.О. Ярманов 2ИБ-1')

# кнопки для действий с Дашбордом
def Dashboard_but(message):
    dashboard_markup = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton('Описание дашборда', callback_data='dashboard_function1')
    button2 = types.InlineKeyboardButton('Ссылка на GitHub', callback_data='dashboard_function2')
    dashboard_markup.add(button1, button2)
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=dashboard_markup)

# кнопки для действий с помощью
def Help_but(message):
    help_markup = types.InlineKeyboardMarkup(row_width=1)
    button16 = types.InlineKeyboardButton('Контакты поддержки', callback_data='help_function2')
    help_markup.add(button15, button16)
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=keyboard)

# кнопки для действий с оформлением заказа
def order_handler(message):
    bot.send_message(message.chat.id, 'Давайте начнем оформление заказа. Введите ваше имя:')
    bot.register_next_step_handler(message, enter_sender_name)

# Ввод имени и пропуск данных дальше    
def enter_sender_name(message):
    order = {}
    order['sender_name'] = message.text
    bot.send_message(message.chat.id, f'Отлично, {message.text}! Выберите товар для приобретения:')
    bot.register_next_step_handler(message, enter_item, order)

#Обработчик для ввода места подачи груза
def enter_item(message, order):
    order['item'] = message.text
    found = df[df['Товар'] == order['item']]
    if(len(found) == 0):
        bot.send_message(me.chat.id, "Товаров с таким названием не найдено.... Извините")
        return
    bot.send_message(message.chat.id, f'Товар: {message.text}. Теперь введите пункт назначения:')
    bot.register_next_step_handler(message, enter_destination, order)

#Обработчик для ввода пункта назначения
def enter_destination(message, order):
    order['destination'] = message.text
    bot.send_message(message.chat.id, f'Пункт назначения: {message.text}. Заказ оформлен!')
    # отчет
    report = f'Отчет по заказу:\n\n' \
             f'Имя отправителя: {order["sender_name"]}\n' \
             f'Товар для приобретения: {order["item"]}\n' \
             f'Пункт назначения: {order["destination"]}\n'

    # Отправка отчета пользователю
    bot.send_message(message.chat.id, report)
    # Создание подключения к базе данных SQLite
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()

    # Создание таблицы для заказов, если ее еще нет
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_name TEXT,
            item TEXT,
            destination TEXT
        )
    ''')

    # Добавление(включение) данных о заказе в ДБ
    cursor.execute('''
        INSERT INTO orders (sender_name, item, destination)
        VALUES (?, ?, ?)
    ''', (order['sender_name'], order['item'], order['destination']))
    conn.commit()

def look_for_item(message):
    bot.send_message(message.chat.id, 'Введите название товара:')
    bot.register_next_step_handler(message, look_for_item_)

def look_for_item_(message):
    me = message
    item_name = message.text
    found = df[df['Товар'] == item_name]
    if(len(found) == 0):
        bot.send_message(me.chat.id, "Товаров с таким названием не найдено....")
    else:
        bot.send_message(me.chat.id, f'Товар присутствует, всего {len(found)} \n'
                                    'Вот некоторые из найденных:')
        i = 3
        for x in found.index:
            i -= 1
            if i == 0:
                break
            item_date = found['Дата'][x]
            item_sum = found['Сумма'][x]
            bot.send_message(me.chat.id, f'{item_name}, дата {item_date}, стоимость {item_sum} рублей')



#INSERT INTO table_name
#VALUES (value1, value2, value3, ...);

bpmn_image_url = 'https://raw.githubusercontent.com/garc0/RGR/development/%D0%B1%D0%B0%D0%B7%D0%B0.png'
bpmn_but = lambda mes : bot.send_photo(mes.chat.id, bpmn_image_url, caption='BPMN карта')

image1_url = 'https://raw.githubusercontent.com/garc0/RGR/main/%D0%BA%D1%80%D1%83%D0%B3%D0%BE%D0%B2%D0%BE%D0%B9_%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D0%BA.png'
image2_url = 'https://raw.githubusercontent.com/garc0/RGR/main/%D0%93%D1%80%D0%B0%D1%84%D0%B8%D0%BA_%D1%80%D0%B0%D1%81%D1%81%D0%B5%D0%B8%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F.png'
image3_url = 'https://raw.githubusercontent.com/garc0/RGR/main/%D0%93%D1%80%D0%B0%D1%84%D0%B8%D0%BA_%D1%80%D0%B0%D1%81%D1%81%D0%B5%D0%B8%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F.png'

dashboard_2 = lambda mes : bot.send_message(mes.chat.id, 'Ссылка на GitHub: https://github.com/garc0/dashbordes')
dashboard_3 = lambda mes : bot.send_photo(mes.chat.id, image1_url, caption='Круговой график')
dashboard_4 = lambda mes : bot.send_photo(mes.chat.id, image2_url, caption='Временной график')
dashboard_5 = lambda mes : bot.send_photo(mes.chat.id, image3_url, caption='График рассеивания')

CALLBACK_D_BUTTON = {
    "bpmn" : bpmn_but, 
    "dashboard" : Dashboard_but, 
    "help": Help_but, 
    "order" : order_handler,
    "lookforitem" : look_for_item,
    "dashboard_function2" : dashboard_2,
    "dashboard_function3" : dashboard_3,
    "dashboard_function4" : dashboard_4,
    "dashboard_function5" : dashboard_5
}

# Обработчик на нажатие клавиш
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data in CALLBACK_D_BUTTON:
        CALLBACK_D_BUTTON[call.data](call.message)

    elif call.data == 'about_bot':
        bot.send_message(call.message.chat.id, 'Telegram-бот может значительно упростить и ускорить процесс обработки заказов '
                                                'для транспортной компании. Именно функции которые можно автоматизировать с ним:'
                                                '\nПрием заказов: Клиенты могут отправлять заказы через бота, указывая необходимую информацию,'
                                                ' такую как место погрузки, пункт назначения, тип груза и другие детали.'
                                                '\nИнтеграция с платежными системами: Для удобства клиентов бот может интегрироваться с платежными системами, '
                                                'позволяя им платить прямо через Telegram.'
                                                '\nОбратная связь и поддержка: Клиенты могут общаться с ботом, '
                                                'чтобы задать вопросы, уточнить детали заказа или оставить отзыв.')


    elif call.data == 'dashboard':
        dashboard_markup = types.InlineKeyboardMarkup(row_width=1)
        button1 = types.InlineKeyboardButton('Описание дашборда', callback_data='dashboard_function1')
        button2 = types.InlineKeyboardButton('Ссылка на GitHub', callback_data='dashboard_function2')
        dashboard_markup.add(button1, button2)
        bot.send_message(call.message.chat.id, 'Выберите действие:', reply_markup=dashboard_markup)
    elif call.data == 'dashboard_function1':
        bot.send_message(call.message.chat.id, 'Дашборд показывает информирует пользвоателя о наличии и '
                                            'распределении товаров по их категории, дате, количеству и их стоимости. '
                                        )

        dashboard_function_markup = types.InlineKeyboardMarkup(row_width=1)

        button3 = types.InlineKeyboardButton('Круговой график', callback_data='dashboard_function3')
        button4 = types.InlineKeyboardButton('Временной график', callback_data='dashboard_function4')
        button5 = types.InlineKeyboardButton('График рассеивания', callback_data='dashboard_function5')
        dashboard_function_markup.add(button3, button4, button5)
        bot.send_message(call.message.chat.id, 'Выберите график:', reply_markup=dashboard_function_markup)


if __name__ == "__main__":
    bot.infinity_polling()