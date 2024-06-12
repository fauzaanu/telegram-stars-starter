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
            LabeledPrice('Basic', 100)
        ],
        provider_token='',
    )


async def precheckout_callback(update, context):
    query = update.pre_checkout_query
    if query.invoice_payload != 'WPBOT-PYLD':
        await query.answer(ok=False, error_message="Something went wrong...")
    else:
        await query.answer(ok=True)


async def successful_payment_callback(update, context):
    """
    This is recieved on successful payment.
    chargeback id can be found by clicking the service message in the chat. (if you are testing).
    This is a good place to store the charg id in your database and to process your internal balance
    or subscription logic.
    """
    print(update.message.successful_payment)


async def refund_payment(update, context):
    """
    This is a sample refund function.
    """
    db = "LETS SAY THIS IS YOUR DB AND YOU HAVE PAYMENTS STORED HERE"  # just an example, dont be insane
    status = await context.bot.refund_star_payment(
        user_id=update.message.chat.id,
        telegram_payment_charge_id=db.telegram_charge_id
    )
    if status:
        await context.bot.send_message(
            chat_id=update.message.chat.id,
            text=f'Your payment {db.telegram_charge_id} has been refunded successfully.'
        )


if __name__ == '__main__':
    load_dotenv()
    token = os.environ['TELEGRAM_BOT_TOKEN']
    application = ApplicationBuilder().token(token).build()

    commands = CommandHandler('start', start_command)
    invoice = CommandHandler('invoice', send_invoice)
    refund = CommandHandler('refund', refund_payment)
    successful_payment = MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback)
    links = MessageHandler(filters.TEXT, hi_hello)

    application.add_handler(commands)
    application.add_handler(invoice)

    # Pre-checkout handler to final check
    application.add_handler(PreCheckoutQueryHandler(precheckout_callback))

    application.add_handler(links)

    application.run_polling()
