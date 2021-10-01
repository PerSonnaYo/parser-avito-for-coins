from turtle import title

from django.core.management.base import BaseCommand
from telegram import Bot
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater
from telegram.utils.request import Request
from django.conf import settings
from av_parser.models import Product

def log_errors(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as ex:
            error_mesage = f'Произошла ошибка {ex}'
            print(error_mesage)
            raise ex
    return inner

@log_errors
def add_product(update: Update, context: CallbackContext, p):
    chat_id = update.message.chat_id
    text = update.message.text

    p.price = text

@log_errors
def do_echo(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text
    p = Product.objects.filter(
        title__contains = text,).all()
    p = Product.objects.filter(
        id=p[0].id
    ).update(price="11110000")
    reply_text = "Boss ID = {}\n\n{}\n\n".format(chat_id, text,)
    update.message.reply_text(
        text=reply_text,
    )
class Command(BaseCommand):
    help = 'Telega+avito'

    def handle(self, *args, **options):
        request = Request(
            connect_timeout=0.5,
            read_timeout=1.0
        )
        bot = Bot(
            request=request,
            token=settings.TOKEN
        )
        updater = Updater(
            bot=bot,
            use_context=True,
        )
        message_handler = MessageHandler(Filters.text, do_echo)
        updater.dispatcher.add_handler(message_handler)

        updater.start_polling()
        updater.idle()