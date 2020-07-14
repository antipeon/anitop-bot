import telebot

bot = None

def init_bot(token):
    global bot
    bot = telebot.TeleBot(token)

    from app import handlers
