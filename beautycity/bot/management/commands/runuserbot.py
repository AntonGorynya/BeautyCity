from django.core.management.base import BaseCommand
from beautycity import settings

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove,
    ParseMode,
)
from telegram.ext import (
    Updater,
#    Filters,
    MessageHandler,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
)

class Command(BaseCommand):
    help = 'Телеграм-бот'

    def handle(self, *args, **kwargs):
        tg_token = settings.tg_token
        updater = Updater(token=tg_token, use_context=True)
        dispatcher = updater.dispatcher

        def start_conversation(update, _):
            query = update.callback_query
            if query:
                query.answer()
            keyboard = [
                [
                    InlineKeyboardButton("Записаться к нам", callback_data='to_make_reservation'),
                    InlineKeyboardButton("Мои записи", callback_data="to_show_orders"),
                    InlineKeyboardButton("О нас", callback_data="to_common_info"),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            if query:
                query.edit_message_text(
                    text=f"Описание компании", reply_markup=reply_markup,
                    parse_mode=ParseMode.HTML
                )
            else:
                update.message.reply_text(
                    text=f"Описание компании", reply_markup=reply_markup,
                    parse_mode=ParseMode.HTML
                )

            return 'GREETINGS'

        def make_reservation(update, _):
            query = update.callback_query
            keyboard = [
                [
                    InlineKeyboardButton("Выбор салона", callback_data='to_choose_site'),
                    InlineKeyboardButton("Выбор Мастера", callback_data="to_choose_master"),
                ],
                [
                    InlineKeyboardButton("Позвонить нам", callback_data='to_contacts'),
                    InlineKeyboardButton("На главный", callback_data="to_start"),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.answer()
            query.edit_message_text(
                text="Как вы хотите записаться", reply_markup=reply_markup
            )
            return 'MAKE_RESERVATION'

        def show_contacts(update, _):
            query = update.callback_query
            keyboard = [
                [
                    InlineKeyboardButton("На главный", callback_data="to_start"),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.answer()
            query.edit_message_text(
                text="Наши контакты", reply_markup=reply_markup
            )
            return 'SHOW_ANSWER'

        def show_common_info(update, _):
            query = update.callback_query
            keyboard = [
                [
                    InlineKeyboardButton("Контакты", callback_data='to_contacts'),
                    InlineKeyboardButton("На главный", callback_data="to_start"),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.answer()
            query.edit_message_text(
                text="Информация о мастерах", reply_markup=reply_markup
            )
            return 'COMMON_INFO'


        def show_orders(update, _):
            query = update.callback_query
            keyboard = [
                [
                    InlineKeyboardButton("На главный", callback_data="to_start"),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.answer()
            query.edit_message_text(
                text="Вы записаны", reply_markup=reply_markup
            )
            return 'SHOW_ANSWER'

        def cancel(update, _):
            user = update.message.from_user
            update.message.reply_text(
                'До новых встреч',
                reply_markup=ReplyKeyboardRemove()
            )
            return ConversationHandler.END

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', start_conversation)],
            states={
                'GREETINGS': [
                    CallbackQueryHandler(make_reservation, pattern='to_make_reservation'),
                    CallbackQueryHandler(show_orders, pattern='to_show_orders'),
                    CallbackQueryHandler(show_common_info, pattern='to_common_info'),
                ],
                'COMMON_INFO': [
                    CallbackQueryHandler(start_conversation, pattern='to_start'),
                    CallbackQueryHandler(show_contacts, pattern='to_contacts'),
                ],
                'SHOW_ANSWER': [
                    CallbackQueryHandler(start_conversation, pattern='to_start'),
                ],
                'MAKE_RESERVATION': [
                    CallbackQueryHandler(start_conversation, pattern='to_start'),
                    CallbackQueryHandler(show_contacts, pattern='to_contacts'),
                ]
            },
            fallbacks=[CommandHandler('cancel', cancel)]
        )

        dispatcher.add_handler(conv_handler)
        start_handler = CommandHandler('start', start_conversation)
        dispatcher.add_handler(start_handler)

        updater.start_polling()
        updater.idle()

