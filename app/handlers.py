from app import bot
from app import http_requests
import time


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Enter the number of shows to show: ")


@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id,
                     "I'll show you most popular shows at https://anilist.co/")
    bot.send_message(message.chat.id, "The commands are:\n"
                                      "\n/help"
                                      "\n/start")


@bot.message_handler(content_types=['text'])
def handle_page_size(message):
    try:
        shows_number = int(message.text)
        messages = http_requests.ParseData(http_requests.GetData(shows_number))
        for one_message in messages:
            caption = ""
            if (type(one_message[2]) != str):
                continue
            if (type(one_message[1]) != str and
                    type(one_message[0]) != str):
                continue
            if (type(one_message[0]) != str):
                caption = one_message[1]
            elif (type(one_message[1]) != str):
                caption = one_message[0]
            else:
                caption = one_message[0] + ' / ' + one_message[1]
            bot.send_photo(message.chat.id, one_message[2], caption=caption)
            time.sleep(1)
    except (TypeError, ValueError):
        bot.send_message(message.chat.id, 'A number, would you?')
