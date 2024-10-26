import telebot
import os
from dotenv import load_dotenv
import moviepy.editor as mp
from telebot import types
load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN'))
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,'скиньте сюда видео', reply_markup=help())

def help():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('/help')
    markup.add(btn1)
    return markup

@bot.message_handler(content_types=['video'])
def video(message):
    print(message)
    fileid = message.video.file_id
    fileinfo = bot.get_file(fileid)
    downloaded_file = bot.download_file(fileinfo.file_path)
    with open('sigma_video.mp4','wb') as file:
        file.write(downloaded_file)
        bot.send_message(message.chat.id,'Пожалуйста, подождите')
    clip = mp.VideoFileClip('sigma_video.mp4')

    width, height = clip.size
    min_length = min(height, width)

    if min_length > 600:
        min_length = 600
    if clip.duration > 60:
        clip = clip.subclip(0,60)

    clip_resized = clip.resize((min_length, min_length))
    clip_resized.write_videofile('sigma_video_resized.mp4')
    with open('sigma_video_resized.mp4', 'rb') as file:
        bot.send_video_note(message.chat.id, file)

@bot.message_handler(commands=['help'])
def help_command(message):
    if message.text == 'Help':
        bot.send_message(message.chat.id, 'Необходимо прислать видео, бот обработает его и пришлет вам кружок.\n'
                            '1. Если длительность больше 60 секунд, бот его обрежет\n'
                            '2.Видео весит не более 12 МБ\n '
                            '3. Если видео больше 640x640 пикселей, бот его обрежет.\n4. Видео прислано не документом')

bot.polling(non_stop=True)