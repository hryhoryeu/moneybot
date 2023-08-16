import logging
from telegram import (
    Update,
    InlineQueryResultArticle,
    InputTextMessageContent,
    ReplyKeyboardMarkup,
    BotCommand,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    InlineQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
    ConversationHandler,
    CallbackQueryHandler,
)

from settings import settings


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

LOVE_ANSWER = 0


async def keyboard_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [
        ["Lova"],
        ["Love"],
        ["Luv"],
        ["❤️"],
        ["🫶🏻"],
        ["not so much"],
    ]
    await update.message.reply_text(
        text="Hi! Tell me how much do you like Yahor?",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=reply_keyboard,
            one_time_keyboard=True,
            input_field_placeholder="Hello",
            resize_keyboard=True,
        ),
    )
    return LOVE_ANSWER


async def love_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = update.message.text
    text_reply = (
        "U better shut up your f*cking mouth..."
        if answer == "not so much"
        else "he loves you too. TO THE MOON AND BACK"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_reply)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a bot, please talk to me!",
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=update.message.text,
    )


async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return
    results = []
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title="Caps",
            input_message_content=InputTextMessageContent(query.upper()),
        )
    )
    await context.bot.answer_inline_query(update.inline_query.id, results)


async def update_commands_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    commands = [
        BotCommand(command="/one", description="start the app"),
    ]
    await context.bot.set_my_commands(commands=commands)
    await context.bot.get_my_commands()


async def unexpected_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Sorry, I don't recognize the command ;("
    )


if __name__ == "__main__":
    application = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("keyboard", keyboard_check)],
        states={
            LOVE_ANSWER: [
                MessageHandler(
                    filters.Regex("^(Lova|Love|Luv|❤️|🫶🏻|not so much)$"), love_answer
                )
            ]
        },
        fallbacks=[],
        allow_reentry=True,
    )
    start_handler = CommandHandler("start", start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    unexpected_handler = MessageHandler(filters.COMMAND, unexpected_input)
    inline_caps_handler = InlineQueryHandler(inline_caps)
    commands_handler = CommandHandler("update_commands", update_commands_list)

    application.add_handlers(
        handlers=[
            commands_handler,
            conv_handler,
            start_handler,
            echo_handler,
            inline_caps_handler,
            unexpected_handler,
        ]
    )

    application.run_polling()
