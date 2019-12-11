import telebot
from yandex.Translater import Translater
import speech_recognition as sr
import glob
import subprocess
import os
import core.data.initdata as initdata
import core.translator.translate_service as trans

def init_bot():
    bot = telebot.TeleBot(initdata.bot_token())
    return bot

def init_yandex_service():
    tr = Translater()
    tr.set_key(initdata.yandex_token())
    tr.set_from_lang('en')
    tr.set_to_lang('ru')
    return tr

#инициализация бота
bot = init_bot()
#инициализация сервиса для перевода от яндекса
tr = init_yandex_service()
#библиотечка для преоброзования аудиофайлов
r = sr.Recognizer()

def bot_run():

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        bot.send_sticker(message.chat.id, "CAADAgADmioAAulVBRixfEtUq4naOhYE")
        bot.send_message(message.chat.id, "Привет, я бот под именем What I Say, "
                                          "я помогу перевести тебе текстовые и голосовые сообщения, "
                                          "не сворачивая telegram напиши команду /help для детального описания!")

    @bot.message_handler(commands=['secret'])
    def send_secret(message):
        print(message)
        bot.send_sticker(message.chat.id, "CAADAgADiCoAAulVBRhNv6XML0lONxYE")


    @bot.message_handler(commands=['help'])
    def send_help_info(message):
        bot.send_message(message.chat.id, "TODO")

    #для получения информации о стикере!
    @bot.message_handler(content_types=['sticker'])
    def send_sticker_id(message):
        print(message)


    @bot.message_handler(content_types=['text'])
    def send_trans(message):
        print(message)

        #функция для перевода аргументом, является текст сообщения от пользователя
        translate_text = trans.translate_text_message(message.text)
        bot.send_message(message.chat.id, translate_text)


    # for translate voice message
    @bot.message_handler(content_types=['voice'])
    def translate_audio_message(message):
        print("translate_audio_message")
        print(message)
        #python -m pip install --upgrade pip

        #download voice on PC
        voice = message.voice
        file_id = voice.file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        FILE_NAME = 'new_file.mp3'

        with open(FILE_NAME, 'wb') as new_file:
            new_file.write(downloaded_file)

        wav_files = glob.glob('./*.mp3')
        print(wav_files)

        subprocess.call(['ffmpeg', '-i', 'C:\\Python\\translate-telegram-bot\\new_file.mp3',
                         'C:\\Python\\translate-telegram-bot\\TEST.wav'])

        #record wav file from PC
        try:
            harvard = sr.AudioFile("C:\\Python\\translate-telegram-bot\\TEST.wav")
            with harvard as source:
                audio = r.record(source)

            # result
            str = r.recognize_google(audio, language='en', show_all=True)
            print(str)

            str = str.get('alternative')[0].get('transcript')
            tr.set_text(str)
            translate_text = tr.translate()
            bot.send_message(message.chat.id, translate_text)
        except:
            bot.send_message(message.chat.id, "Не могу распознать сообщение, повторите еще раз!")

        os.remove("C:\\Python\\translate-telegram-bot\\TEST.wav")

        #start bot
    bot.polling()