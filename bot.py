import sqlite3
import telebot
from datetime import datetime as dt
from telebot import types
bot = telebot.TeleBot("7357998584:AAHdd5IUuS1iiAYIsP17htAsCEYz7xDHnTU")

conn = sqlite3.connect('db/database.db', check_same_thread=False)
cursor = conn.cursor()
@bot.message_handler(commands=['start'])
def start_message(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	btn1 = types.KeyboardButton("Написать в тех. поддержку")
	markup.add(btn1)

	us_id = [message.chat.id, message.chat.username]
	u_id = message.chat.id
	db_table_user(T_id=us_id, u_id=u_id)
	bot.send_message(message.chat.id, "Добро пожаловать", reply_markup=markup)

def db_table_user(T_id: list, u_id: int):

	cursor.execute(f'SELECT Telegram_id FROM User WHERE Telegram_id = {u_id}')
	data = cursor.fetchone()
	if data is None:
		cursor.execute('INSERT INTO User VALUES(?, ?);', T_id)

		conn.commit()
	else:
		pass

def db_table_feedback(feedback_list: list):
	cursor.execute("INSERT INTO Feedback VALUES(?, ?, ?);", feedback_list)
	conn.commit()
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
	if (message.text == 'Написать в тех. поддержку'):
		bot.send_message(message.chat.id, "Опишите вашу проблему", reply_markup=types.ReplyKeyboardRemove(), parse_mode='Markdown')
	else:
		f_text = message.text
		f_us_name = message.chat.username
		cur_date = dt.now()
		f_date = cur_date.strftime('%d.%m.%Y %H:%M')
		f_l = [f_us_name, f_date, f_text]
		db_table_feedback(feedback_list=f_l)



bot.polling(none_stop=True)