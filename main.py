from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import re

# Замените 'YOUR_BOT_TOKEN' на ваш токен
TOKEN = '6423569377:AAFCRXLl6DkrtrCXvelGfgUgNI_VkEsi42E'

# Замените 'YOUR_USER_ID' на ваш Telegram ID
YOUR_USER_ID = '867798233'


def start(update, context):
    update.message.reply_text('Привет! Я бот, который будет принимать приглашения к каналам и парсить их сообщения.')


def invite_handler(update, context):
    channel_invite_links = re.findall(r'https://t.me/[^\s]+', update.message.text)
    for link in channel_invite_links:
        try:
            invite = context.bot.create_chat_invite_link(link)
            chat_member = context.bot.get_chat_member(invite.chat.id, context.bot.id)

            if chat_member.status in ['left', 'kicked']:
                context.bot.join_chat(invite.chat.id)
                update.message.reply_text(f'Присоединился к каналу {invite.chat.title} ({invite.chat.username}).')
                # Добавляем обработчик сообщений в присоединенном канале
                dp.add_handler(MessageHandler(Filters.chat(invite.chat.id), forward_message))
            else:
                update.message.reply_text(f'Бот уже участвует в канале {invite.chat.title} ({invite.chat.username}).')
        except Exception as e:
            update.message.reply_text(f'Не удалось присоединиться к каналу. Ошибка: {str(e)}')


def forward_message(update, context):
    # Пересылаем сообщение в личный чат
    context.bot.forward_message(chat_id=YOUR_USER_ID, from_chat_id=update.message.chat_id,
                                message_id=update.message.message_id)


def main():
    updater = Updater(TOKEN, use_context=True)

    global dp
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, invite_handler))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
