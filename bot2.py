import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import settings
import ephem
import datetime


def greet_user(update, context):
    user_name = update.message.from_user.first_name
    print(f'Greetings, my dear little {user_name}! :) You push /start')
    update.message.reply_text(f'Greetings, my dear little {user_name}! :) You push /start')
    

def talk_to_me(update, context):
    user_text = update.message.text 
    l = user_text.split()
    current_time = datetime.datetime.now() 
    if l[0] == '/planet':
        plnt = eval('ephem.'+l[1])(f'{current_time.year}/{current_time.day}/{current_time.month}')
        constellation = ephem.constellation(plnt)
        print(constellation)
        update.message.reply_text(constellation)
    else:
        user_name = update.message.from_user.first_name
        print(f'{user_name}: {user_text}')
        update.message.reply_text(f'{user_name}: {user_text}')

def error_callback(update, error):
    try:
        raise error
    except:
        print("Telegram Error")
        print(f'I do not now such planet as {update.message.text.split()[1]}')
        update.message.reply_text(f'I do not now such planet as {update.message.text.split()[1]}. Try again')


def main():
    PROXY = {'proxy_url': settings.PROXY_URL, 'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}

    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)
    logging.basicConfig(filename='bot.log', level=logging.INFO)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start',greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    dp.add_error_handler(error_callback)

    logging.info("Bot has just started")
    mybot.start_polling()
    mybot.idle()



if __name__ == "__main__":
    main()