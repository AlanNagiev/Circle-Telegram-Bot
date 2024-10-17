import telebot
import os
from dotenv import load_dotenv
import moviepy.editor as mp
load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN'))
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,'скиньте сюда видео')

@bot.message_handler(content_types=['video'])
def video(message):
    print(message)
    fileid = message.video.file_id
    fileinfo = bot.get_file(fileid)
    downloaded_file = bot.download_file(fileinfo.file_path)
    with open('sigma_video.mp4','wb') as file:
        file.write(downloaded_file)
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


bot.polling(non_stop=True)