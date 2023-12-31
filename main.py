#!/usr/bin/python
import telebot
import os
from telebot import types
# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.

from telebot.async_telebot import AsyncTeleBot

token = open('tokens/telegram.txt').readline()
admins =  open('tokens/admins.txt').read().split('\n')

bot = AsyncTeleBot(token)

# Handle '/start' and '/help'
@bot.message_handler(commands=['start', 'help'])  # старт
async def send_welcome(message):
    usr_id = str(message.from_user.id)  # userid
    usr_name = str(message.from_user.first_name)  # имя юзера
    keyboard = types.ReplyKeyboardMarkup(True)  # генерируем клаву
    butt_cabinet = types.KeyboardButton(text='Личный кабинет')
    butt_shop = types.KeyboardButton(text='Магазин')
    butt_admin = types.KeyboardButton(text='АдминОЧКА')
    if usr_id in admins:
        keyboard.add(butt_cabinet, butt_shop, butt_admin)
    else:
        keyboard.add(butt_shop, butt_cabinet)
    await bot.reply_to(message, "Привет, " + str(message.from_user.first_name), reply_markup=keyboard)  # здороваемся
    await bot.reply_to(message, "Я продаю ключики от самого лучшего ВПНа *VPNname*. По всем вопросам к @mihailovily")


@bot.message_handler(commands=['main']) 
@bot.message_handler(regexp="Главная")  # старт
async def main_page(message):
    usr_id = str(message.from_user.id)  # userid
    usr_name = str(message.from_user.first_name)  # имя юзера
    keyboard = types.ReplyKeyboardMarkup(True)  # генерируем клаву
    butt_cabinet = types.KeyboardButton(text='Личный кабинет')
    butt_shop = types.KeyboardButton(text='Магазин')
    butt_admin = types.KeyboardButton(text='АдминОЧКА')
    if usr_id in admins:
        keyboard.add(butt_cabinet, butt_shop, butt_admin)
    else:
        keyboard.add(butt_shop, butt_cabinet)  # здороваемся
    await bot.reply_to(message, "Ты на главной странице", reply_markup=keyboard)

@bot.message_handler(commands=['/admin'])
@bot.message_handler(regexp="АдминОЧКА")
async def admin_cabinet(message):
    usr_id = str(message.from_user.id)  # userid
    usr_name = str(message.from_user.first_name)  # имя юзера
    if usr_id in admins:
        keyboard = types.ReplyKeyboardMarkup(True)  # генерируем клаву
        butt_main = types.KeyboardButton(text='Главная')
        butt_add_admin = types.KeyboardButton(text='Добавить админа')
        butt_delete_admin = types.KeyboardButton(text='Убрать админа')
        if usr_id in admins:
            keyboard.add(butt_main, butt_add_admin, butt_delete_admin)
        await bot.reply_to(message, get_report(), reply_markup=keyboard)
    else:
        await bot.reply_to(message, 'Недостаточный уровень доступа')

@bot.message_handler(commands=['/shutdown'])
async def admin_cabinet(message):
    usr_id = str(message.from_user.id)  # userid
    usr_name = str(message.from_user.first_name)  # имя юзера
    if usr_id in admins:
        await shutdown()
    else:
        await bot.reply_to(message, 'Недостаточный уровень доступа')


def get_report():
    myCmd = os.popen('uptime').read()
    return myCmd

def shutdown():
    os.system('shutdown now')
    
def get_keys_list():
    m = os.popen('cd keys && ls').read()
    a = m.split()
    return a

def count_keys():
    return len(get_keys_list())
    

@bot.message_handler(commands=['/shop'])
@bot.message_handler(regexp="Магазин")
async def shop(message):
    usr_id = str(message.from_user.id)  # userid
    keys_left = count_keys()
    usr_name = str(message.from_user.first_name)
    if usr_id in admins:
        answer_about_keys = 'Ключей осталось в базе: ' + str(keys_left)
        await bot.send_message(usr_id, answer_about_keys)
    keyboard = types.InlineKeyboardMarkup()  # генерируем клаву
    butt_buy = types.InlineKeyboardButton(text='Купить ключ')
    butt_valid = types.InlineKeyboardButton(text='Проверить срок действия ключа')
    keyboard.add(butt_buy, butt_valid)
    await bot.reply_to(message, 'Добро пожаловать в магазин. Что желаете сделать?', reply_markup=keyboard)
    

@bot.message_handler(func=lambda message: True)
async def dont_understand(message):
    await bot.reply_to(message, 'Я тебя не понял')


import asyncio
asyncio.run(bot.polling())