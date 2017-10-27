# TOKEN = demjson.decode(open('../files/constants.json','r').read())['TOKEN']

from colors import colors
import sys
import asyncio
import subprocess
import telepot
import demjson
import time
import codecs
from random import randint
from telepot import message_identifier, glance
from telepot.aio.loop import MessageLoop
from telepot.aio.delegate import pave_event_space, per_chat_id, create_open
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

app_constants = demjson.decode(open('../files/constants.json', 'r').read())
curent_hafez_faal = {}


def is_admin(user_id):
    admins = app_constants['ADMIN IDS']
    for admin in admins:
        if(user_id == admin):
            print('>> ADMIN PERMISSION <<')
            return True
        else:
            return False


async def on_chat_message(msg):
    # defaults
    print(colors.HEADER + '@' + msg['from']['username'] + ': ' + colors.OKBLUE + '\"' + msg['text'] + '\"' +
          colors.WARNING + ' (' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(msg['date'])) + ')' + colors.ENDC)
    log_file = codecs.open('../files/logs.txt', 'a', 'utf-8')
    log_file.write('@' + msg['from']['username'] + ' \"' + msg['text'] + '\"' +
                   ' (' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(msg['date'])) + ')\n')
    log_file.close()
    hafez_faal_recieved = False
    # 📗 فال حافظ
    if(msg['text'] == '📗 فال حافظ'):
        curent_hafez_faal[msg['chat']['id']] = randint(1, 495)
        await bot.sendMessage(msg['chat']['id'], 'علاقه مند هستین که فال خود را به چه صورتی دریافت کنید ؟', reply_markup={'keyboard': [['📷 دریافت عکس از فال'], ['🗣 دریافت فایل صوتی'], ['✒ دریافت متن فال'], ['➡ بازگشت به منو اصلی']], 'selective': True})
    # 📷 دریافت عکس از فال
    elif(msg['text'] == '📷 دریافت عکس از فال'):
        await bot.sendPhoto(msg['chat']['id'], open('../files/hafez/images/' + str(curent_hafez_faal[msg['chat']['id']]) + '.png', 'rb'), reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text='دریافت تعبیر فال 🔮', callback_data='yes'),
        ]]))
    # 🗣 دریافت فایل صوتی
    elif(msg['text'] == '🗣 دریافت فایل صوتی'):
        await bot.sendVoice(msg['chat']['id'], open('../files/hafez/voices/' + str(curent_hafez_faal[msg['chat']['id']]) + '.ogg', 'rb'), reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text='دریافت تعبیر فال 🔮', callback_data='yes'),
        ]]))
    # ✒ دریافت متن فال
    elif(msg['text'] == '✒ دریافت متن فال'):
        vars = codecs.open('../files/hafez/texts/' + str(
            curent_hafez_faal[msg['chat']['id']]) + '.txt', 'r', "utf-8").readlines()
        # vars = codecs.open('../files/hafez/texts/2.txt','r',"utf-8").readlines()
        result = ''
        for var in vars:
            result += var.replace('\\n\\t', '\n') + '\n'
        # await bot.sendMessage(msg['chat']['id'],result,reply_markup= {'keyboard': [['📷 دریافت عکس از فال','🗣 دریافت فایل صوتی'],['🔮 دریافت تعبیر فال','✒ دریافت متن فال'],['➡ بازگشت به منو اصلی']], 'selective': True})
        await bot.sendMessage(msg['chat']['id'], result, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text='دریافت تعبیر فال 🔮', callback_data='yes'),
        ]]))
    # on admin commands
    elif(msg['text'] == 'ipconfig'):
        if(is_admin(msg['chat']['id'])):
            ip_details =  str(subprocess.check_output("ipconfig")).strip('\n')
            ip_details =  ip_details.strip('\r')
            await bot.sendMessage(msg['chat']['id'],ip_details)            
    # on any message
    else:
        hafez_faal_recieved = False
        await bot.sendMessage(msg['chat']['id'], 'گزینه ی دلخواه خود را انتخاب کنید ', reply_markup={'keyboard': [['📗 فال حافظ']], 'selective': True})


async def on_callback_query(msg):
    query_id, from_id, query_data = glance(msg, flavor='callback_query')
    if query_data ==  'yes':
        result = codecs.open('../files/hafez/interpretations/' + str(
            curent_hafez_faal[from_id]) + '.txt', 'r', "utf-8").readlines()
        await bot.sendMessage(from_id,str(result[0]))
        

bot = telepot.aio.Bot(app_constants['TOKEN'])
loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(
    bot, {'chat': on_chat_message, 'callback_query': on_callback_query}).run_forever())
print(colors.OKGREEN + 'Bot start\'s running ...' + colors.ENDC)
loop.run_forever()
