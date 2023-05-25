from django.core.management.base import BaseCommand
from beautycity import settings
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove,
    ParseMode,
    LabeledPrice
)
from telegram.ext import (
    Updater,
    Filters,
    MessageHandler,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
)


def send_invoice(update, context):
    token = settings.payments_token
    chat_id = update.effective_message.chat_id
    context.bot.send_invoice(
        chat_id,
        'title',
        'description',
        payload='payload',
        provider_token=token,
        currency='RUB',
        need_phone_number=False,
        need_email=False,
        is_flexible=False,
        prices=[
            LabeledPrice(label='Название услуги', amount=int(10000))
        ],
        start_parameter='start_parameter',
    )


class Command(BaseCommand):
    help = 'Телеграм-бот'

    def handle(self, *args, **kwargs):
        # tg_token = settings.TOKEN
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
                ],
                [
                    InlineKeyboardButton("Позвонить нам", callback_data='to_contacts'),
                ],
                [
                    InlineKeyboardButton("Оставить отзыв о мастере", callback_data='to_leave_feedback'),
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

        def leave_feedback(update, _):
            query = update.callback_query
            query.answer()
            query.edit_message_text("Оставьте свой отзыв о мастере: ")
            return 'GET_FEEDBACK'

        def get_feedback(update, _):
            feedback_text = update.message.text
            # feedback = Feedback(name="User", feedback=feedback_text)
            # feedback.save()
            update.message.reply_text("Спасибо за ваш отзыв!")
            start_conversation(update, _)
            return 'GREETINGS'

        def make_reservation(update, _):
            query = update.callback_query
            keyboard = [
                [
                    InlineKeyboardButton("Выбор Мастера", callback_data="to_choose_master"),
                    InlineKeyboardButton("Выбор Услуги", callback_data="to_choose_service"),
                ],
                [
                    InlineKeyboardButton("Позвонить нам", callback_data='to_contacts'),
                    InlineKeyboardButton("На главную", callback_data="to_start"),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.answer()
            query.edit_message_text(
                text="Как вы хотите записаться", reply_markup=reply_markup
            )
            return 'MAKE_RESERVATION'

        def call_salon(update, _):
            query = update.callback_query
            keyboard = [
                [
                    InlineKeyboardButton("На главную", callback_data="to_start"),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.answer()
            query.edit_message_text(
                text="Рады звонку в любое время.\n Телефон:8 800 555 35 35", reply_markup=reply_markup
            )
            return 'CALL_SALON'

        def show_masters(update, _):
            query = update.callback_query
            keyboard = [
                [
                    InlineKeyboardButton("Ольга", callback_data="master_olga"),
                    InlineKeyboardButton("Татьяна", callback_data="master_tatiana"),
                ],
                [
                    InlineKeyboardButton("На главную", callback_data="to_start"),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.answer()
            query.edit_message_text(
                text="Выберите Мастера", reply_markup=reply_markup
            )
            return 'SHOW_MASTERS'

        def show_service(update, _):
            query = update.callback_query
            keyboard = [

                [
                    InlineKeyboardButton("Покраска волос", callback_data="to_hair_dyeing"),
                ],
                [
                    InlineKeyboardButton("Мейкап", callback_data="to_do_make-up"),
                    InlineKeyboardButton("Маникюр", callback_data="to_do_manicure")
                ],
                [
                    InlineKeyboardButton("Цены на услуги", callback_data="service_prices"),
                ],
                [
                    InlineKeyboardButton("На главную", callback_data="to_start")
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.answer()
            query.edit_message_text(
                text="Выберите услугу", reply_markup=reply_markup
            )
            return 'SHOW_SERVICE'

        def show_prices(update, _):
            query = update.callback_query
            keyboard = [
                [InlineKeyboardButton("Назад", callback_data="back_to_service")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.answer()
            query.edit_message_text(
                text="Цены на услуги:\n"
                     "- Покраска волос: $50\n"
                     "- Маникюр: $30\n"
                     "- Мейкап: $40",
                reply_markup=reply_markup
            )
            return 'SHOW_PRICES'

        def select_time(update, _):
            query = update.callback_query
            keyboard = [
                [
                    InlineKeyboardButton("10:00", callback_data="time_10"),

                ],
                [
                    InlineKeyboardButton("13:00", callback_data="time_13"),

                ],
                [
                    InlineKeyboardButton("Выбор Услуг", callback_data="back_to_service"),
                    InlineKeyboardButton("Выбор Мастера", callback_data="to_choose_master"),

                ],
                [
                    InlineKeyboardButton("Позвонить нам", callback_data='to_contacts')
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.answer()
            query.edit_message_text(
                text="Выберите время", reply_markup=reply_markup
            )
            return 'SELECT_TIME'

        def make_record(update, _):
            query = update.callback_query
            query.answer()
            query.edit_message_text(
                "Введите ваше имя и номер телефона в формате:\n\n <ваше имя>:<ваш номер телефона>")
            return 'GET_CONTACT'

        def get_contact(update, _):
            contact_info = update.message.text
            name = None
            phone = None
            if contact_info:
                contact_info = contact_info.strip().split(':')
                if len(contact_info) == 2:
                    name = contact_info[0].strip()
                    phone = contact_info[1].strip()

            if name and phone:

                update.message.reply_text("Спасибо за запись! До встречи ДД.ММ ЧЧ:ММ по адресу: ул. улица д. дом")

                keyboard = [
                    [InlineKeyboardButton("Оплатить сразу", callback_data="to_pay_now")],
                    [InlineKeyboardButton("На главную", callback_data="to_start")],
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                update.message.reply_text("Желаете записаться снова?", reply_markup=reply_markup)

                return 'WAITING_FOR_CONFIRMATION'
            else:
                update.message.reply_text(
                    "Пожалуйста, введите имя и номер телефона в указанном формате: <имя>:<номер>.")
                return 'GET_CONTACT'




        def show_common_info(update, context):
            query = update.callback_query
            keyboard = [
                [
                    InlineKeyboardButton("Позвонить нам", callback_data='to_contacts'),
                    InlineKeyboardButton("На главную", callback_data="to_start"),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.answer()
            query.edit_message_text(
                text="Информация о салоне, что делаем и т.д", reply_markup=reply_markup
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
                    CallbackQueryHandler(call_salon, pattern='to_contacts'),
                    CallbackQueryHandler(leave_feedback, pattern='to_leave_feedback'),
                ],
                'GET_FEEDBACK': [
                    MessageHandler(Filters.text, get_feedback),
                ],
                'MAKE_RESERVATION': [
                    CallbackQueryHandler(show_service, pattern='to_choose_service'),
                    CallbackQueryHandler(show_masters, pattern='to_choose_master'),
                    CallbackQueryHandler(start_conversation, pattern='to_start'),
                    CallbackQueryHandler(call_salon, pattern='to_contacts'),
                ],
                'CALL_SALON': [
                    CallbackQueryHandler(start_conversation, pattern='to_start'),
                ],
                'SHOW_SERVICE': [
                    CallbackQueryHandler(start_conversation, pattern='to_start'),
                    CallbackQueryHandler(select_time, pattern='to_hair_dyeing'),
                    CallbackQueryHandler(select_time, pattern='to_do_make-up'),
                    CallbackQueryHandler(select_time, pattern='to_do_manicure'),
                    CallbackQueryHandler(show_prices, pattern='service_prices'),
                ],
                'SHOW_PRICES': [
                    CallbackQueryHandler(show_service, pattern='back_to_service')
                ],

                'SHOW_MASTERS': [
                    CallbackQueryHandler(select_time, pattern='master_olga'),
                    CallbackQueryHandler(select_time, pattern='master_tatiana'),
                    CallbackQueryHandler(start_conversation, pattern='to_start'),

                ],
                'SELECT_TIME': [
                    CallbackQueryHandler(show_masters, pattern='to_choose_master'),
                    CallbackQueryHandler(show_service, pattern='back_to_service'),
                    CallbackQueryHandler(call_salon, pattern='to_contacts'),
                    CallbackQueryHandler(make_record, pattern='time_10'),
                    CallbackQueryHandler(make_record, pattern='time_13'),

                ],
                'GET_CONTACT': [
                    CallbackQueryHandler(show_masters, pattern='to_pay_now'),
                    CallbackQueryHandler(start_conversation, pattern='to_start'),
                ],
                'COMMON_INFO': [
                    CallbackQueryHandler(start_conversation, pattern='to_start'),
                    CallbackQueryHandler(call_salon, pattern='to_contacts'),
                ],
                'SHOW_ANSWER': [
                    CallbackQueryHandler(start_conversation, pattern='to_start'),
                ],

            },
            fallbacks=[CommandHandler('cancel', cancel)]
        )

        dispatcher.add_handler(conv_handler)
        start_handler = CommandHandler('start', start_conversation)
        dispatcher.add_handler(start_handler)
        dispatcher.add_handler(MessageHandler(Filters.text, get_contact))
        updater.start_polling()
        updater.idle()
