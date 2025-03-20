import telebot
from telebot import types
import random

bot = telebot.TeleBot("TOKEN")

@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton("Help")
    btn2 = types.KeyboardButton("Info")
    markup.row(btn1, btn2)
    file = open("./images.png", "rb")
    bot.send_photo(message.chat.id, file, reply_markup=markup)
    bot.register_next_step_handler(message, on_click)

def on_click(message):
    if message.text == "Help":
        bot.send_message(message.chat.id, "Hello! Just send me your photo, document, or audio, and I will give you a reaction about it.")
    elif message.text == "Info":
        bot.send_message(
            message.chat.id,
            "Hello! I am a test bot. Here's what I can do:\n"
            "- React to your photos, documents, and audios.\n"
            "- Allow you to delete or edit specific messages.\n"
            "- Provide helpful and fun information!\n"
            "Try sending me something!"
        )

@bot.message_handler(content_types=["photo"])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Go to website", url="https://google.com")
    markup.row(btn1)
    btn2 = types.InlineKeyboardButton("Delete photo", callback_data="delete")
    btn3 = types.InlineKeyboardButton("Change text", callback_data="edit")
    markup.row(btn2, btn3)
    bot.reply_to(message, "What a beautiful photo! 🌟", reply_markup=markup)

@bot.message_handler(content_types=["document", "audio", "video"])
def handle_file(message):
    if message.content_type == "document":
        bot.reply_to(message, "This is an interesting document! 📄")
    elif message.content_type == "audio":
        bot.reply_to(message, "What a nice sound! 🎵")
    elif message.content_type == "video":
        bot.reply_to(message, "Wow, this video is amazing! 🎥")
    else:
        bot.reply_to(message, "Hmm, not sure what to say about this file, but thanks for sending it!")

@bot.message_handler(content_types=["text"])
def random_reaction(message):
    if message.text == "Help":
        bot.send_message(message.chat.id, "Hello! Just send me your photo, document, or audio, and I will give you a reaction about it.")
    elif message.text == "Info":
        bot.send_message(
            message.chat.id,
            "Hello! I am a test bot. Here's what I can do:\n"
            "- React to your photos, documents, and audios.\n"
            "- Allow you to delete or edit specific messages.\n"
            "- Provide helpful and fun information!\n"
            "Try sending me something!"
        )
    else:
        reactions = [
            "That's quite interesting! 🤔",
            "Hmm, I like your energy! 😄",
            "Wow, that's a thought-provoking message! 📖",
            "Thanks for sharing! 🙌"
        ]
        bot.reply_to(message, random.choice(reactions))

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == "delete":
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
        bot.send_message(callback.message.chat.id, "Message deleted successfully! 🗑")
    elif callback.data == "edit":
        bot.edit_message_text(
            "The text has been edited! ✏️",
            callback.message.chat.id,
            callback.message.message_id
        )

bot.polling()
