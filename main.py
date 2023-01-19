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
from dotenv import load_dotenv
from constants import *

load_dotenv()

path = Path(__file__).parents[0] # местонахождение файла hskbot1.py
path_json = path / 'data.json' # местонахождение файла data.json
with open(path_json,encoding='utf-8') as json_file: # открывает файл data.json
    data = json.load(json_file) # читает этот файл (data.json) как обычный текст и превращает в словарь

translator = google_translator() #обращяемся к переводчику

TOKEN = os.getenv('TOKEN') # token бота

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start']) #создаем команду
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Новый иероглиф")
    button2 = types.KeyboardButton("Про Китай")
    markup.add(button1,button2)
    bot.send_message(message.chat.id, "Привет, {0.first_name}!\n\nЯ бот для изучения HSK-1 (Твои первые 150 китайских слов).\nЗдесь ты можешь получать новые иероглифы каждый день в любое время или читать факты о языке и провинциях Китая.\n\nОбращай внимание на тон, прежде чем произносить слово - это важно.\n\nНажми на нужную кнопку в меню 🐼".format(message.from_user), reply_markup=markup)

@bot.message_handler(content_types=['text'])
def func(message):
    if(message.text == "Про Китай"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Факты о языке")
        button2 = types.KeyboardButton("Провинции Китая")
        markup.add(button1,button2)
        bot.send_message(message.chat.id, text="О чем ты хочешь почитать сегодня?", reply_markup=markup)

    elif(message.text == "Факты о языке"):
        item = random.choice(facts)
        bot.send_message(message.chat.id, text=f'{item}')

    elif(message.text == "Провинции Китая"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        provinces = []
        for province in provinces_list:
           provinces.append(types.KeyboardButton(province)) 
        back = types.KeyboardButton("На главную")
        markup.add(back,*provinces) # * распаковывает список
        bot.send_message(message.chat.id, text="Сейчас в состав Китайской Народной Республики (КНР) входят 23 провинции, включая Тайвань.\n\nВыбери про какую провинцию ты хочешь узнать, нажав нужную кнопку из списка ниже.", reply_markup=markup)

    elif(message.text in provinces_list):
        province_fact = provinces_facts.get(message.text,'Фактов не найдено')
        if type(province_fact)==str: # если провинс факт это строка то фактов не найдено
            bot.send_message(message.chat.id, parse_mode="MARKDOWN", text=province_fact)
            return # выход из функции
        translate_name = province_fact.get('translate_name')
        name_province = province_fact.get('name_province')
        translate_name_province = province_fact.get('translate_name_province')
        province_facts = province_fact.get('province_facts')
        audiofile = path / f"{name_province}({translate_name}) .mp3"
        voice = gtts.gTTS(translate_name, lang='zh-CN') # делаем гс
        voice.save(audiofile) # сохраняем гс
        bot.send_message(message.chat.id, parse_mode="MARKDOWN", text=f'{name_province} {translate_name_province}\n\n {province_facts}')

        bot.send_audio(message.chat.id, audio=open(audiofile, "rb")) # отправляем озвучку
        os.remove(audiofile)

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

    elif (message.text == "На главную"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Новый иероглиф")
        button2 = types.KeyboardButton("Про Китай")
        markup.add(button1, button2)
        bot.send_message(message.chat.id, text="Ты снова в начале пути", reply_markup=markup)

bot.infinity_polling(interval=0, timeout=600) # должен быть в конце

