# from aiogram.exceptions import TelegramBadRequest
from typing import Any
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, ReplyKeyboardRemove # , ContentType
from aiogram import F, Bot, Dispatcher, Router
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder #, KeyboardButton, KeyboardButtonPollType
from datetime import datetime
import logging
import asyncio
import requests
import aiohttp
from aiogram.client.session.aiohttp import AiohttpSession
# import json
from aiogram.utils.markdown import text, bold, italic, code, pre


router = Router()

region = "62"
href_weather = f'https://yandex.com/time/sync.json?geo={region}'
img_led_on  = '  ON  🔴 '  # ⚪  🌕🟡
img_led_off = ' OFF  🟢 '  # 🔵   🌑

API_TOKEN = '6909476636:AAGsmlwshjrFSun6vOglJ11Lk3UHOX8RLWs'  # "6349601788:AAGgrNqYBhyvIBHJnFEN_RBljR4BYJMdhxY"
BLYNK_TOKEN = 'fu9VBk46dSwdxjxKdgG3A0pMvHyOj2U1'
ADMIN_ID = 468763535


class RelBtn():
    def __init__(self, id = '', pin='V0', state: int = 0, img="", name='Rel_') -> None:   
        self.id = id
        self.pin = pin
        self.url_get = f'https://api.blynk.tk/{BLYNK_TOKEN}/get/{self.pin}'
        self.state = state
        self.last_state = state
        # self.last_state = int(requests.get(self.url_get).text[2])
        self.img = img_led_on if self.state else img_led_off 
        self.name = f'Rel_{self.id}{self.img}'
        self.update()

    def update(self):
        # self.last_state = int(requests.get(self.url_get).text[2])
        if self.state != self.last_state:  
            self.last_state = self.state          
            self.img = img_led_on if self.state==1 else img_led_off 
            self.name = f'Rel_{self.id}{self.img}'

        
    def toggle(self):        
        self.state = 1 if self.last_state == 0 else  0
        self.update()       
        state = '1' if self.state else '0'  
        print('toggle', self.name)
        self.url_update = f'https://api.blynk.tk/{BLYNK_TOKEN}/update/{self.pin}?value={state}'
        response = requests.get(self.url_update)      
        # print(f'response.status_code ..... {response.status_code}')
       



btn_rel_1 = RelBtn(id='1')
btn_rel_2 = RelBtn(id='2')
btn_rel_3 = RelBtn(id='3')
btn_rel_4 = RelBtn(id='4')
btn_rel_5 = RelBtn(id='5')
btn_rel_6 = RelBtn(id='6')

btn_rels = [btn_rel_1, btn_rel_2, btn_rel_3, btn_rel_4, btn_rel_5, btn_rel_6]
v_pins = ["V2", "V4", "V6", "V8", "V10", "V12"]


print ('\nCreate btn_rels[] ')
for i in range(len(btn_rels)):
    btn_rels[i].pin = v_pins[i]
    btn_rels[i].update()
    # int(requests.get(btn_rels[i].url_get).text[2])
    print ( btn_rels[i].name, btn_rels[i].last_state, btn_rels[i].pin)   #  # rels_kb.add(btn_rels[i].name)



names_btns = [
    "Rel_1", "Rel_2", 
    "Rel_3", "Rel_4", 
    "Rel_5", "Rel_6"
    ]

names_btns2 = [
    "Led Warm UP", "Led Warm DOWN",
    "Led Cold UP", "Led Cold DOWN"
    ]



def keyboard_rels2():
    builder = ReplyKeyboardBuilder()
    for i in range(len(names_btns2)):       
    #     btn_rels[i].img = img_led_on if btn_rels[i].urlstate else img_led_off
        # btn_rels[i].update()
        # btn_rels[i].name = 'Rel_' + btn_rels[i].id + btn_rels[i].img
        builder.button(text= f'{names_btns2[i]}')
        builder.adjust(2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=False, input_field_placeholder='leds ')


def keyboard_rels():
    builder = ReplyKeyboardBuilder()
    for i in range(len(names_btns)):       
    #     btn_rels[i].img = img_led_on if btn_rels[i].urlstate else img_led_off
        # btn_rels[i].update()
        btn_rels[i].name = 'Rel_' + btn_rels[i].id + btn_rels[i].img
        builder.button(text= f'{btn_rels[i].name}')
        builder.adjust(2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=False, input_field_placeholder='кнопки...')



# kb_hide = ReplyKeyboardRemove() # Remove keyboard     
async def hide_keyboard(message: Message):
    kb = ReplyKeyboardRemove()
    await message.answer (f"прячу клавиатуру", reply_markup=kb )


def get_web():    
    builder = InlineKeyboardBuilder()
    builder.button(text=f" На сайт погоды 🌤⛅☀", url='https://yandex.ru/pogoda/62?lat=56.010563&lon=92.852572') # 🌦⛈🌥
    builder.adjust(1)
    return builder.as_markup()



@router.message(F.text.contains('Rel_')) 
async def cmd_relays(message: Message):   
    for i in range(len(btn_rels)):  # if message.text == btn_rels[i].name:
        if message.text.startswith(f'Rel_{btn_rels[i].id}'):
            btn_rels[i].toggle() 

    kb = keyboard_rels()
    await message.answer(f'{btn_rels[i].name}', reply_markup=kb) #



@router.message(Command("start")) 
async def get_start(message: Message):
    kb = ReplyKeyboardRemove()
    await message.answer (f'Привет {message.from_user.first_name}!\n С возвращением !', reply_markup=kb)


# @router.message(Command("show")) 
async def get_keyboard(message: Message):
    kb = keyboard_rels()
    await message.answer ('Кнопки ', reply_markup=kb)


# @router.message(F.text.contains("show2")) 
async def get_keyboard2(message: Message):
    kb = keyboard_rels2()
    await message.answer ('Кнопки ', reply_markup=kb)

  

async def start_bot(bot: Bot):
    print ("Бот запущен!")
    kb = ReplyKeyboardRemove()
    await bot.send_message(ADMIN_ID, text="<b>Бот запущен!</b>", reply_markup=kb)



async def stop_bot(bot: Bot):
    print ("Бот остановлен!")
    # await bot.send_message(ADMIN_ID, text=f"<b>Бот остановлен!</b>")



async def get_weather(message: Message, bot: Bot):
    await message.answer(f"Секунду, получаю погоду...\n")
    req = requests.get(href_weather) #, data = {'key':'value'}
    json_weather = req.json()    
    time = json_weather['time']
    temp = json_weather['clocks'][region]['weather']['temp']
    sunrise = json_weather['clocks'][region]['sunrise']
    sunset = json_weather['clocks'][region]['sunset']
    # dt = datetime.fromtimestamp(time)
    dt = datetime.now().strftime("%Y-%m-%d %H:%M")
    print (f'Дата и время [ {dt} ] ')
    print (f'Теипература в Красноярске {temp} °C')
    await message.answer(f"О как! Сегодня {dt}\nтемпература сейчас <code>{temp} °C.</code>\nВосхлд в <b>{sunrise}</b>, а закат в <b>{sunset}</b>", reply_markup=get_web())
    # await message.answer(f"Можно посетить сайт погоды...\n")
    

async def get_help(message: Message):   
    await message.reply('not availible')
  
 

async def start():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - "
        "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    )
    # session = AiohttpSession(proxy='http://proxy.server:3128')
    # bot = Bot(token=API_TOKEN , parse_mode='HTML', session=session)
    bot = Bot(token=API_TOKEN , parse_mode='HTML')
    dp = Dispatcher()
    dp.include_router(router)    
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    

    dp.message.register(get_start, Command(commands=['start']))
    dp.message.register(get_weather, Command(commands=['weather']))
    dp.message.register(get_keyboard, Command(commands=['show']))
    dp.message.register(get_keyboard2, Command(commands=['show2']))
    dp.message.register(hide_keyboard, Command(commands=['hide']))
    dp.message.register(get_help, Command(commands=['help']))

    # dp.message.register(get_start, F.text == '/start')     
    # dp.message.register(get_keyboard, F.text.lower().contains('show')) # & F.from_user.id == get_set.bots.admin_id))
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close() 



if __name__ == "__main__":
    asyncio.run(start())        




# match color:
#     case "red":
#         print("красный")
#     case "blue":
#         print("синий")
#     case "green":
#         print("зелёный")
#     case _:
#         print("это не красный, синий или зелёный")
