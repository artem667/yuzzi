import config
import telebot
import random
bot = telebot.TeleBot(config.token)
BAD_WORDS = ['блять','хуй','пизда','тварь','залупа','чурка','мразь','сука','сучка']
jokes = ['если бы я был деректором ....................... я бы депнул школу в казик','сайт гос.услуг: у вас нет задолжиностей((((','я на крыше и завтра у меня егэ по физики, и я буду проверять гравитацию']
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я твой Telegram бот. Напиши что-нибудь!")


@bot.message_handler(commands=['joke'])
def joke(message):
    joke = random.choice(jokes)
    bot.reply_to(message,joke)
@bot.message_handler(content_types=['photo'])
def photo(message):
    #with open('Без названия (1).jpg', 'rb') as photo:
    #    bot.send_photo(message.chat.id, photo, caption="Вот твоё фото!")
    file_id = message.photo[-1].file_id
    bot.send_photo(message.chat.id, file_id, caption="Вот твоё фото!")
@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.reply_to_message: #проверка на то, что эта команда была вызвана в ответ на сообщение 
        chat_id = message.chat.id # сохранение id чата
         # сохранение id и статуса пользователя, отправившего сообщение
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status 
         # проверка пользователя
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно забанить администратора.")
        else:
            bot.ban_chat_member(chat_id, user_id) # пользователь с user_id будет забанен в чате с chat_id
            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был забанен.")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите забанить.")



@bot.message_handler(commands=['info'])
def info(message):
    if message.reply_to_message:
        chat_id = message.chat.id # сохранение id чата
         # сохранение id и статуса пользователя, отправившего сообщение
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status 
        bot.reply_to(message, f"id of user: {chat_id}\nhim id: {user_id}\nand him status: {user_status}")
    else:
        chat_id = message.chat.id
        user_id = message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status 
        bot.reply_to(message, f"id of chat: {chat_id}\nyour id: {user_id}\nand your status: {user_status}")


@bot.message_handler(func=lambda m: any(word in m.text.lower() for word in BAD_WORDS))
def bad_word_handler(message):
    bot.reply_to(message, "если ты напишешь ещё 1 брание слово")  
    with open('угроза2.jpg', 'rb') as photo:  
        bot.send_photo(message.chat.id, photo)


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)

bot.infinity_polling()
