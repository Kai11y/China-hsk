import telebot
from telebot import types # для указания типов
import configparser
import json # бибилотека для чтения json
from pathlib import Path # для определения пути к файлу json с иероглифами
import random # библиотека отвечающая за случайные выборы, чтобы из файла data.json рандомно брались иероглифы (? с повторениями или без хз)
from facts import facts
from google_trans_new import google_translator
import gtts
import os

path = Path(__file__).parents[0] # местонахождение файла hskbot1.py
path_json = path / 'data.json' # местонахождение файла data.json
with open(path_json,encoding='utf-8') as json_file: # открывает файл data.json
    data = json.load(json_file) # читает этот файл (data.json) как обычный текст и превращает в словарь

translator = google_translator() #обращяемся к переводчику

TOKEN = "5837517226:AAGWxGdfNt7mHl292iF2EOUHOkcb3oEBezc" # token бота

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start']) #создаем команду
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Новый иероглиф")
    button2 = types.KeyboardButton("Не сегодня")
    markup.add(button1,button2)
    bot.send_message(message.chat.id, "Привет, {0.first_name}!\n\nЯ бот для изучения HSK-1.\nЗдесь ты можешь получать новые иероглифы каждый день в любое время или почитать интересные факты о Китае.\n\nОбращай внимание на тон, прежде чем произносить слово - это важно.\n\nНажми на нужную кнопку в меню 🐼".format(message.from_user), reply_markup=markup)

@bot.message_handler(content_types=['text'])
def func(message):
    if(message.text == "Не сегодня"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Факты о Китае")
        button2 = types.KeyboardButton("Тоже не сегодня")
        markup.add(button1,button2)
        bot.send_message(message.chat.id, text="Может хочешь немного фактов о Китае?", reply_markup=markup)

    elif(message.text == "Факты о Китае"):
        item = random.choice(facts)
        bot.send_message(message.chat.id, text=f'{item}')

    elif(message.text == "Тоже не сегодня"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton("Назад")
        markup.add(back)
        bot.send_message(message.chat.id, text="Хорошо отдохни и возвращайся завтра!❤️", reply_markup=markup)

    elif(message.text == "Новый иероглиф"):
        item = random.choice(data) # где item случайны объект из data.json
        dictionary = item.get('data',{}) # get - вытащит все данные из data, {} - заполнитель, если item.get ничегоне  вернет, то он вернет пустой словарь 
        translate = dictionary.get('translate')
        pinyin = dictionary.get('pinyin')
        simplified = dictionary.get('simplified')
        traditional = dictionary.get('traditional')
        audiofile = path / f"{simplified}({translate}) .mp3"
        voice = gtts.gTTS(simplified, lang='zh-CN') # делаем гс
        voice.save(audiofile) # сохраняем гс
     
        bot.send_message(message.chat.id, parse_mode="MARKDOWN", text=f'*{translate}*\n\nПиньин: {pinyin}\nУпрощённый: {simplified}\nТрадиционный: {traditional}')

        bot.send_audio(message.chat.id, audio=open(audiofile, "rb")) # отправляем озвучку
        os.remove(audiofile)

    elif (message.text == "Назад"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Новый иероглиф")
        button2 = types.KeyboardButton("Не сегодня")
        markup.add(button1, button2)
        bot.send_message(message.chat.id, text="Ты снова в начале пути", reply_markup=markup)

bot.polling(none_stop=True) # должен быть в конце

