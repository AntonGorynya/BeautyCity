from django.core.management.base import BaseCommand
from beautycity import settings
from ...models import Master, Service, MasterSchedule, Shift, ClientOffer
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
from phonenumbers import is_valid_number, parse

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

        def show_masters_time(update, _):
            query = update.callback_query
            masters = Master.objects.all()
            keyboard = []
            for master in masters:
                keyboard.append([
                    InlineKeyboardButton(master.name, callback_data=f"master_{master.pk}")
                ])
            keyboard.append([InlineKeyboardButton("На главную", callback_data="to_start")])
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.answer()
            query.edit_message_text(
                text="Выберите Мастера", reply_markup=reply_markup
            )
            return 'SHOW_MASTERS_TIME'

        def show_masters_producer(update, _):
            query = update.callback_query
            masters = Master.objects.all()
            keyboard = []
            for master in masters:
                keyboard.append([
                    InlineKeyboardButton(master.name, callback_data=f"master_{master.pk}")
                ])
            keyboard.append([InlineKeyboardButton("На главную", callback_data="to_start")])
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.answer()
            query.edit_message_text(
                text="Выберите Мастера", reply_markup=reply_markup
            )
            return 'SHOW_MASTERS_PROCEDURE'

        def show_service_time(update, _):
            query = update.callback_query
            services = Service.objects.all()
            keyboard = []
            for service in services:
                keyboard.append([InlineKeyboardButton(service.name, callback_data=f"service_{service.pk}")])
            keyboard.append([InlineKeyboardButton("Цены на услуги", callback_data="service_prices")])
            keyboard.append([InlineKeyboardButton("На главную", callback_data="to_start")])
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.answer()
            query.edit_message_text(text="Выберите услугу", reply_markup=reply_markup)
            return 'SHOW_SERVICE_TIME'

        def show_service_procedure(update, _):
            query = update.callback_query
            services = Service.objects.all()
            keyboard = []
            for service in services:
                keyboard.append([InlineKeyboardButton(service.name, callback_data=f"service_{service.pk}")])
            keyboard.append([InlineKeyboardButton("!!Цены на услуги", callback_data="service_prices")])
            keyboard.append([InlineKeyboardButton("На главную", callback_data="to_start")])
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.answer()
            query.edit_message_text(text="Выберите услугу", reply_markup=reply_markup)
            return 'SHOW_SERVICE_PROCEDURE'

        def show_prices(update, _):
            query = update.callback_query
            keyboard = [
                [InlineKeyboardButton("Назад", callback_data="back_to_service")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.answer()
            services = Service.objects.all()
            text = 'Наши услуги \n'
            for service in services:
                text +=f'- {str(service)}\n'
            query.edit_message_text(
                text=text,
                reply_markup=reply_markup
            )
            return 'SHOW_PRICES'

        def select_time(update, context):
            # Выбор id из контекста и 2 return должно быть в зависимости от context, фильтр должен быть по дате, выбор даты должен быть на предыдущем шаге.
            master_scdeule_id = 1

            query = update.callback_query
            client_offers = ClientOffer.objects.filter(master_schedule__id=master_scdeule_id)
            shifts = Shift.objects.exclude(pk__in=client_offers.values_list('shift'))
            keyboard = []
            for shift in shifts:
                keyboard.append(
                    [
                        InlineKeyboardButton(f'{shift.star_time} -- {shift.end_time}', callback_data=f"time_{shift.pk}"),
                    ]
                )
            keyboard.append([InlineKeyboardButton("Позвонить нам", callback_data='to_contacts')])
            keyboard.append([InlineKeyboardButton("На главную", callback_data="to_start")])

            reply_markup = InlineKeyboardMarkup(keyboard)
            query.answer()
            query.edit_message_text(
                text="Выберите время", reply_markup=reply_markup
            )
            return 'SELECT_TIME'

        def make_record(update, _):
            query = update.callback_query
            query.answer()
            query.edit_message_text("Введите ваше имя:")
            return 'GET_NAME'

        def get_name(update, _):
            name = update.message.text.strip()
            if name:
                update.message.reply_text("Введите ваш номер телефона:")
                return 'GET_PHONE'
            else:
                update.message.reply_text("Пожалуйста, введите ваше имя.")
                return 'GET_NAME'

        def get_phone(update, context):
            phone_number = update.message.text
            parsed_number = parse(phone_number, 'RU')

            if is_valid_number(parsed_number):
                update.message.reply_text("Спасибо за запись! До встречи ДД.ММ ЧЧ:ММ по адресу: ул. улица д. дом")
                context.user_data['phone_number'] = phone_number
                keyboard = [
                    [InlineKeyboardButton("Оплатить услугу сразу", callback_data="to_pay_now")],
                    [InlineKeyboardButton("На главную", callback_data="to_start")],
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                update.message.reply_text("Желаете записаться снова?", reply_markup=reply_markup)

                return 'WAITING_FOR_CONFIRMATION'
            else:
                update.message.reply_text("Пожалуйста, введите корректный номер телефона.")
                return 'GET_PHONE'


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
                    CallbackQueryHandler(show_service_time, pattern='to_choose_service'),
                    CallbackQueryHandler(show_masters_producer, pattern='to_choose_master'),
                    CallbackQueryHandler(start_conversation, pattern='to_start'),
                    CallbackQueryHandler(call_salon, pattern='to_contacts'),
                ],
                'CALL_SALON': [
                    CallbackQueryHandler(start_conversation, pattern='to_start'),
                ],
                'SHOW_SERVICE_TIME': [
                    CallbackQueryHandler(start_conversation, pattern='to_start'),
                    CallbackQueryHandler(select_time, pattern=r'service_\d+$'),
                    CallbackQueryHandler(show_prices, pattern='service_prices'),
                ],
                'SHOW_SERVICE_PROCEDURE': [
                    CallbackQueryHandler(start_conversation, pattern='to_start'),
                    CallbackQueryHandler(select_time, pattern=r'service_\d+$'),
                    CallbackQueryHandler(show_prices, pattern='service_prices'),
                ],
                'SHOW_PRICES': [
                    CallbackQueryHandler(show_service_time, pattern='back_to_service')
                ],
                'SHOW_MASTERS_TIME': [
                    CallbackQueryHandler(make_record, pattern=r'^master_\d+$'),
                    CallbackQueryHandler(start_conversation, pattern='to_start'),
                ],
                'SHOW_MASTERS_PROCEDURE': [
                    CallbackQueryHandler(show_service_procedure, pattern=r'master_\d+$'),
                    CallbackQueryHandler(start_conversation, pattern='to_start'),
                ],
                'SELECT_TIME': [
                    CallbackQueryHandler(start_conversation, pattern='to_start'),
                    CallbackQueryHandler(call_salon, pattern='to_contacts'),
                    CallbackQueryHandler(show_masters_time, pattern='time_*'),
                ],
                'GET_PHONE': [
                    CallbackQueryHandler(send_invoice, pattern='to_pay_now'),
                    CallbackQueryHandler(start_conversation, pattern='to_start'),
                ],
                'COMMON_INFO': [
                    CallbackQueryHandler(start_conversation, pattern='to_start'),
                    CallbackQueryHandler(call_salon, pattern='to_contacts'),
                ],
                'SHOW_ANSWER': [
                    CallbackQueryHandler(start_conversation, pattern='to_start'),
                ],
                'GET_NAME': [
                    MessageHandler(Filters.text, get_name),
                ],

            },
            fallbacks=[CommandHandler('cancel', cancel)]
        )

        dispatcher.add_handler(conv_handler)
        start_handler = CommandHandler('start', start_conversation)
        dispatcher.add_handler(start_handler)
        dispatcher.add_handler(MessageHandler(Filters.text, get_phone))
        dispatcher.add_handler(CallbackQueryHandler(send_invoice, pattern='to_pay_now'))
        dispatcher.add_handler(CallbackQueryHandler(start_conversation, pattern='to_start'))
        updater.start_polling()
        updater.idle()
