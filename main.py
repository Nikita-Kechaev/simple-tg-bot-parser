import datetime
import os
import sqlite3

import pandas
from dotenv import load_dotenv
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


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
    context.bot.send_message(
        chat_id=chat.id,
        text='Спасибо, что включили меня!',
    )


def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    updater.dispatcher.add_handler(
        CommandHandler('start', wake_up)
    )
    updater.dispatcher.add_handler(
        MessageHandler(Filters.document, downloader)
    )

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
