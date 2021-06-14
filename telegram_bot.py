"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
"""

import telegram
from telegram import Update, ForceReply, ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
from decouple import config
import logging
import requests

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_BOT = config('TELEGRAM_BOT')
TELEGRAM_BOT_TOKEN = config('TELEGRAM_BOT_TOKEN')
API_TOKEN = config('API_TOKEN')

API_URL = 'http://juanbrusco.pythonanywhere.com/api/get_shift'


def error_callback(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def start(update, context):
    # Send a message when the command /start is issued.
    user = update.effective_user
    update.message.reply_text(
        'Hola 👋 \n\n'
        'Te enviaré la farmacia de turno \n\n'
        'Recordá que podés usar la app <a href="https://farma-salto.web.app/">FarmaSalto</a>', parse_mode=ParseMode.HTML
    )

    shift(update, context)


def end(update: Update, context: CallbackContext) -> int:
    # Cancels and ends the conversation
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Adiós! Suerte y que tengas buen día.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def shift(update, context):
    r = requests.get(url=API_URL, headers={"Authorization": "Token " + API_TOKEN})
    data = r.json()

    pharmacy = data['shift'][0]['pharmacy']['name']
    address = data['shift'][0]['pharmacy']['address']
    city = data['shift'][0]['pharmacy']['city']['name']
    state = data['shift'][0]['pharmacy']['city']['province_state']
    phone = data['shift'][0]['pharmacy']['phone']

    map = '<a href="http://maps.google.com/?q=' + address + ',' + city + ',' + state + '">' + address + '</a>'
    msg = 'Farmacia: <b>' + pharmacy + '</b>\n\nDirección: ' + map + '\n\nTeléfono: +549' + phone

    logger.debug(msg)
    update.message.reply_text(text=msg,
                              parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        'Enviá /turno y te responderé con la farmacia del día en Salto (Bs.As.).')


def reply_message(update: Update, context: CallbackContext) -> None:
    # reply the user message
    msg = update.message.text
    if "hola" in msg.lower():
        start(update, context)
    elif "adios" in msg.lower() or "chau" in msg.lower():
        end(update, context)
    elif "turno" in msg.lower():
        shift(update, context)
    elif "ayuda" in msg.lower():
        help_command(update, context)
    else:
        update.message.reply_text('Ese mensaje no es válido')
        help_command(update, context)


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('inicio', start))
    dp.add_handler(CommandHandler('hello', start))
    dp.add_handler(CommandHandler('hola', start))

    dp.add_handler(CommandHandler('help', help_command))
    dp.add_handler(CommandHandler('ayuda', help_command))
    dp.add_handler(CommandHandler('info', help_command))

    dp.add_handler(CommandHandler('shift', shift))
    dp.add_handler(CommandHandler('turno', shift))
    dp.add_handler(CommandHandler('hoy', shift))

    dp.add_handler(CommandHandler('end', end))
    dp.add_handler(CommandHandler('cancel', end))
    dp.add_handler(CommandHandler('cancelar', end))
    dp.add_handler(CommandHandler('chau', end))

    # on non command i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, reply_message))

    # on error
    dp.add_error_handler(error_callback)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    print(TELEGRAM_BOT + ' started')
    main()
