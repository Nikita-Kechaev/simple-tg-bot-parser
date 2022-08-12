import datetime
import os
import sqlite3

import pandas
import requests
import numpy
from dotenv import load_dotenv
from lxml import html
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from telegram import ReplyKeyboardMarkup

load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')


def load_in_sqlite(con, df):
    cursor = con.cursor()
    cursor.execute("""CREATE TABLE if not exists test_table
                  (name text,URL text,xpath text)""")
    data_tuple = (
        df.columns[0],
        df.columns[1],
        df.columns[2]
    )
    sqlite_insert_query = """INSERT INTO test_table
                             (name, URL, xpath) VALUES
                             (?, ?, ?)"""
    cursor.execute(sqlite_insert_query, data_tuple)
    con.commit()


def create_message(df):
    name = df.columns[0]
    URL = df.columns[1]
    xpath = df.columns[2]
    mesage = (f"Вы направили данные: название сайта: {name}, URL: {URL}, "
              f"xpath: {xpath}")
    return mesage


def downloader(update, context):
    con = sqlite3.connect('mydb.db')
    chat = update.effective_chat
    uniq_filename = f"{'_'.join((str(datetime.datetime.now()).split()))}.xls"
    with open(f"files/{uniq_filename}", 'wb') as f:
        context.bot.get_file(update.message.document).download(out=f)
    df = pandas.read_excel(f"files/{uniq_filename}")
    load_in_sqlite(con, df)
    message = create_message(df)
    context.bot.send_message(
        chat_id=chat.id,
        text=message
    )


def wake_up(update, context):
    chat = update.effective_chat
    button = ReplyKeyboardMarkup([['/average']], resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        reply_markup=button,
        text='Спасибо, что включили меня!',
    )


def count_average():
    con = sqlite3.connect('mydb.db')
    cursor = con.cursor()
    sqlite_select_query = """SELECT * from test_table"""
    cursor.execute(sqlite_select_query)
    records = cursor.fetchall()
    average_array = []
    for row in records:
        url = requests.get(f'{row[1]}')
        content = html.fromstring(url.content)
        xpath = row[2]
        price = content.xpath(xpath)
        average_array.append(int(price[0]))
    average = numpy.average(average_array)
    return f"Средняя цена на диски god of war: {str(average)}"


def send_count_average(update, context):
    chat = update.effective_chat
    message = count_average()
    context.bot.send_message(
        chat_id=chat.id,
        text=message,
        )


def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    updater.dispatcher.add_handler(
        CommandHandler('start', wake_up)
    )
    updater.dispatcher.add_handler(
        CommandHandler('average', send_count_average)
    )
    updater.dispatcher.add_handler(
        MessageHandler(Filters.document, downloader)
    )

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
