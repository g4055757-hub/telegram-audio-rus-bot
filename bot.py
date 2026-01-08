import os
import telebot

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    global STUDENT_ID

    if message.from_user.id != ADMIN_ID:
        STUDENT_ID = message.from_user.id
        bot.send_message(
            message.chat.id,
            "Привет! 👋\n"
            "Это аудио-тренажёр для практики русского языка.\n\n"
            "🎧 Слушай задания и записывай ответы голосом."
        )
    else:
        bot.send_message(
            message.chat.id,
            "Режим преподавателя активен.\n"
            "Отправь аудио — бот передаст его ученику."
        )

@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    global STUDENT_ID

    # если это ТЫ — отправляем ученику
    if message.from_user.id == ADMIN_ID:
        if STUDENT_ID:
            bot.send_voice(
                chat_id=STUDENT_ID,
                voice=message.voice.file_id
            )
        else:
            bot.send_message(
                ADMIN_ID,
                "Ученик ещё не запустил бота."
            )

    # если это УЧЕНИК — отправляем тебе
    else:
        bot.forward_message(
            chat_id=ADMIN_ID,
            from_chat_id=message.chat.id,
            message_id=message.message_id
        )
        bot.send_message(
            message.chat.id,
            "Аудио получено ✅\n"
            "Продолжай тренировку."
        )


bot.polling()
