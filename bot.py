import logging
import os

from dotenv import load_dotenv
from telegram import LabeledPrice
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, PreCheckoutQueryHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start_command(update, context):
    await context.bot.send_message(
        chat_id=update.message.chat.id,
        text='Welcome to the bot! How can I help you?'
    )


async def hi_hello(update, context):
    await context.bot.send_message(
        chat_id=update.message.chat.id,
        text='Hi, Hello! How is life?'
    )


async def send_invoice(update, context):
    await context.bot.send_invoice(
        chat_id=update.message.chat.id,
        title='Sample Invoice',
        description='This is a sample invoice',
        payload='WPBOT-PYLD',
        currency='XTR',
        prices=[
            LabeledPrice('Basic', 100),
            LabeledPrice('Premium', 200),
            LabeledPrice('Pro', 300),
        ],
        provider_token='',
    )


async def precheckout_callback(update, context):
    query = update.pre_checkout_query
    if query.invoice_payload != 'WPBOT-PYLD':
        await query.answer(ok=False, error_message="Something went wrong...")
    else:
        await query.answer(ok=True)


if __name__ == '__main__':
    load_dotenv()
    token = os.environ['TELEGRAM_BOT_TOKEN']
    application = ApplicationBuilder().token(token).build()

    commands = CommandHandler('start', start_command)
    invoice = CommandHandler('invoice', send_invoice)
    links = MessageHandler(filters.TEXT, hi_hello)

    application.add_handler(commands)
    application.add_handler(invoice)

    # Pre-checkout handler to final check
    application.add_handler(PreCheckoutQueryHandler(precheckout_callback))

    application.add_handler(links)

    application.run_polling()
