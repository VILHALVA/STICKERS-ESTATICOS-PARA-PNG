from TOKEN import TOKEN
import telebot
import requests
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_instructions(message):
    instructions = "Olá! Envie-me um sticker e eu enviarei de volta a versão em foto PNG."
    bot.send_message(message.chat.id, instructions)

@bot.message_handler(content_types=['sticker'])
def handle_sticker(message):
    try:
        file_info = bot.get_file(message.sticker.file_id)
        file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}"
        response = requests.get(file_url)
        sticker_path = os.path.join(BASE_DIR, 'sticker.png')
        with open(sticker_path, 'wb') as f:
            f.write(response.content)
        bot.send_document(message.chat.id, open(sticker_path, 'rb'))
        os.remove(sticker_path)

    except Exception as e:
        print(f"Erro ao processar o sticker: {e}")

bot.polling()
