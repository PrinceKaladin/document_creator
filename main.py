import telebot
from telebot import types
import requests
import json
import os
import threading
import time
from requests.auth import HTTPBasicAuth
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime
from coinbase_commerce.client import Client
from coinbase_commerce.webhook import Webhook
from googletrans import Translator

TOKEN = "7970079011:AAGykMNUVoPTlUFh3cbAwMn-3gz6EzPvcmY"
user_data = {}
current_step = {}
translator = Translator()
get_generator_url = "https://api.verifblog.com/api/integration/generator-full-information/"
get_generation_status = "https://api.verifblog.com/api/integration/generation-status/"
generate_url = "https://api.verifblog.com/api/integration/generate/"
pay_url = "https://api.verifblog.com/api/integration/pay-for-result/"
auth = HTTPBasicAuth("viber.sell@gmail.com", "80675630393Roma")
check_url = "https://api.verifblog.com/api/integration/generation-status"
user_language={}
# Инициализация Firebase
fb_key="""{
  "type": "service_account",
"project_id": "telegrampasportbot",
  "private_key_id": "f01d8e63bc2c3758eff71ebb9e737486babb50b3",
  "private_key": "-----BEGIN PRIVATE KEY-----\\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDXFTSKYwmkpAWA\\nzaceWMdu9NgZSXwXVmO9vM4mYhXItlZvD1IMtzyMOS7rE0IJwBEV+vnO+1BJJFeL\\n50OogxnrvesyE8NEl8afe7nyrhi3o/M733znsjIhjlRmFj5BiL8JrzmFaMz/d1dT\\nw7xoJcKIIowZczmU/eXK98UizjBemr6LCHciqxIVVbdiceNsPZIsJ648E6bjuTMj\\npXCawGXPuuXXNwkDE8kj8kBDo4jtB2tKVhM0RDQrxAqX3tLrFvStq2qEMAbz03NS\\n0hHrch8O8ofac5JA9rQOW9JfyqhTp1Ytwk9WxUs/sXMZi64Ltz1e0IQSxYEZf4OJ\\nobORhaT3AgMBAAECggEAIngkhnUey4L52s2aldN2isK0i0DqoTbYH0VN6HrZsOP/\\n8CaNaLpI+tQDP+tDLxrX4iTpuhEuqbooSaSThEMWeWBjfBAMwEZur4p9n3XlQjEF\\nPzgu5Vb6j8QmpIG2Enye2Sd62XWVPO/cT/FTlYFPrs+SklWUCduy4xdYQZ63w8FP\\ngI8D7z734eXQZzjOshiDvVKJh29r76/R0YIVi6IlVaEXqRSdagLLb9CW/qNR1YaJ\\njRy1Bj14qjs9VhfzBcmNgAFZg31jMW0zSIgVIeLJQ1HuMY8vDjxhdbYeg8AUouO1\\n6pWNnN7RH8Yg6Fq1/GjgUNvqejMZpshXH6Baqzzw8QKBgQD/vnwxmZl3M606BjWd\\n7Jk6hl7JougXT/I/JcvUA+kCDCrhucW0HX+WvZkg7Dgc68RhiTwkDir76q6HKYIV\\nvLsNkHRE0LLGlr5zETWuQhtkiBR4/AFUpr4m3EQwM+Npxaj3dfMAMtyGfav3A108\\ngNWHE/Fac5yS2dtKrf/PyPzW7wKBgQDXTE3Dww6OHN626AocoDNS/wLboR4GM+uT\\nK4278OkovFAmL4WAUOR5UDEIKAEqBz+ybkvsAYBGeLUyrAWAbFP5Z8dz+EyoTH+F\\nvBsLc+m5eeVPG1j/oi45ccR2w70d3q/87CEae2z/YybWCg1uz0dJAYZV6AxkcOCM\\nzYIZUYzSeQKBgQDLXht+icla3BItaRCr86BpxL6Nk2kCWMWnZ5PtleptgWV8OHE5\\n6Jc0NLMXViDNBsMUWMAlX8rYpueAfgZ+6KTKhYufyWHQv8DU2eOZHeKQkBHPn34j\\nZbEiT9g9iJWX3+GcXwQMrWVl4XulIty6pyyljLtJlVP2Bx32BeW9wvMkqwKBgG4n\\naSY+12SYms6kXAAXawsM1G6Aubbcu6v5vbOp5/Fin/NZnwlu2ebDw8JzjVzuhoWJ\\nbyjZ/8KOoc7COrJhOnnBwkewg7AcK6bF/mRWsv+lwVA/IsLwPIxBjA5jyY/Nzuct\\n/SXqfnMQTN94FzVZshRFRnEPn7+IDSudPfIsSkupAoGBAORE96OkPLoLkzXYAxc2\\nZpIaWFQLH/pIWGGYdqmbNcSH+pinDbED9DT6B6di/B9JdfBgyLfdgd51J98Ovdr8\\nw3cMLXvVfbn2zPbCvKgGkVXBCUxUYb7oZcI+f0l2gEyfhuGXYZ0bxXOWCvvm64qX\\nI7nl4MXMODYylKEWXVSeUMzX\\n-----END PRIVATE KEY-----\\n",
  "client_email": "firebase-adminsdk-7x8vk@telegrampasportbot.iam.gserviceaccount.com",
  "client_id": "104670815525630013630",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-7x8vk%40telegrampasportbot.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
"""
firebase_key = json.loads(fb_key)
cred = credentials.Certificate(firebase_key)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://telegrampasportbot-default-rtdb.europe-west1.firebasedatabase.app/'  # Замените на ваш URL базы данных
})
current_action = {}
admin_step={}
character_step={}
documents = {
    "Passport 📘": [
    "usa passport 🇺🇸", "uk passport 🇬🇧", "china passport 🇨🇳", "germany passport 🇩🇪",
    "france passport 🇫🇷", "canada passport 🇨🇦", "armenia passport 🇦🇲", "australia passport 🇦🇺",
    "austria passport 🇦🇹", "bangladesh passport 🇧🇩", "belarus passport 🇧🇾", "brazil passport 🇧🇷",
    "belgium passport 🇧🇪", "cameroon passport 🇨🇲", "croatia passport 🇭🇷", "czech passport 🇨🇿",
    "denmark passport 🇩🇰", "dominican republic passport 🇩🇴", "egypt passport 🇪🇬",
    "estonia passport 🇪🇪", "finland passport 🇫🇮", "georgia passport 🇬🇪", "greece passport 🇬🇷",
    "hungary passport 🇭🇺", "india passport 🇮🇳", "indonesia passport 🇮🇩",
    "ireland passport 🇮🇪", "israel passport 🇮🇱", "italy passport 🇮🇹", "ivory coast passport 🇨🇮",
    "kazakhstan passport 🇰🇿", "kenya passport 🇰🇪", "latvia passport 🇱🇻", "malaysia passport 🇲🇾",
    "mexico passport 🇲🇽", "netherlands passport 🇳🇱", "new zealand passport 🇳🇿",
    "norway passport 🇳🇴", "peru passport 🇵🇪", "poland passport 🇵🇱", "serbia passport 🇷🇸",
    "singapore passport 🇸🇬", "slovakia passport 🇸🇰", "slovenia passport 🇸🇮", "rsa passport 🇿🇦",
    "russia passport 🇷🇺", "russia passport old 🇷🇺", "russia external passport 1 🇷🇺",
    "south korea passport 🇰🇷", "spain passport 🇪🇸", "sweden passport 🇸🇪", "swiss passport 🇨🇭",
    "taiwan id 🇹🇼", "thailand passport newtt 🇹🇭", "uae passport 🇦🇪", "ukraine passport 🇺🇦",
    "turkey passport 🇹🇷", "venezuela passport 🇻🇪", "vietnam passport 🇻🇳", "chad passport 🇹🇩"
],
    "Driver's License 🪪": [
    "dl ri 🇺🇸", "dl texas 🇺🇸", "dl nm 🇺🇸", "dl la 🇺🇸", "dl michigan 🇺🇸", "dl mississippi 🇺🇸",
    "dl oklahoma 🇺🇸", "dl kentucky 🇺🇸", "dl maine 🇺🇸", "dl wyoming 🇺🇸", "dl sc 🇺🇸", "dl vermont 🇺🇸",
    "dl oregon 🇺🇸", "dl nebraska 🇺🇸", "dl nevada 🇺🇸", "dl nh 🇺🇸", "dl tennessee 🇺🇸", "dl texas new 🇺🇸",
    "dl montana 🇺🇸", "dl sd 🇺🇸", "dl hawaii 🇺🇸", "dl alaska 🇺🇸", "dl nc 🇺🇸", "dl delaware 🇺🇸",
    "dl connecticut 🇺🇸", "dl ks 🇺🇸", "dl texas old 🇺🇸", "dl id 🇺🇸", "dl nd 🇺🇸", "dl iowa 🇺🇸",
    "dl az 🇺🇸", "dl mo 🇺🇸", "dl minnesota 🇺🇸", "dl ga 🇺🇸", "dl ut 🇺🇸", "dl il 🇺🇸", "dl md 🇺🇸",
    "dl wi 🇺🇸", "dl va 🇺🇸", "dl wa 🇺🇸", "dl colorado 🇺🇸", "dl al 🇺🇸", "dl wv 🇺🇸", "dl ny 🇺🇸",
    "dl ar 🇺🇸", "dl ca 🇺🇸", "dl pa 🇺🇸", "dl ma 🇺🇸", "dl florida 🇺🇸", "dl nj 🇺🇸", "dl indiana 🇺🇸",
    "dl ohio 🇺🇸", "uk dl 🇬🇧", "uk dl new 🇬🇧", "russia dl 🇷🇺", "russia dl 2 🇷🇺", "france dl 🇫🇷",
    "australia dl 🇦🇺", "australia queensland dl 🇦🇺", "austria dl 🇦🇹", "belarus dl 🇧🇾",
    "belgium dl 🇧🇪", "czech dl 🇨🇿", "denmark dl 🇩🇰", "estonia dl 🇪🇪", "finland dl 🇫🇮",
    "germany dl 🇩🇪", "greece dl 🇬🇷", "ireland dl 🇮🇪", "israel dl 🇮🇱", "italy dl 🇮🇹",
    "japan dl 🇯🇵", "kazakhstan dl 🇰🇿", "nigeria dl 🇳🇬", "norway dl 🇳🇴", "poland dl 🇵🇱",
    "romania dl 🇷🇴", "slovakia dl 🇸🇰", "south korea dl 🇰🇷", "spain dl 🇪🇸", "sweden dl 🇸🇪"
],
    "ID Card 🆔": [
    "usa id 🇺🇸", "uk id 🇬🇧", "china id 🇨🇳", "germany id 🇩🇪", "france id 🇫🇷", "austria id 🇦🇹",
    "belgium id 🇧🇪", "bulgaria passport 🇧🇬", "czech id 🇨🇿", "estonia id 🇪🇪", "finland id 🇫🇮",
    "greece id card 🇬🇷", "hungary id 🇭🇺", "ireland passport card 🇮🇪", "italy id 🇮🇹",
    "kazakhstan id 🇰🇿", "latvia id 🇱🇻", "lithuania residense card 🇱🇹", "malaysia id 🇲🇾",
    "netherlands id 🇳🇱", "north macedonia id card 🇲🇰", "norway id 🇳🇴", "poland id 🇵🇱",
    "romania id 🇷🇴", "serbia id 🇷🇸", "singapore id 🇸🇬", "slovakia id 🇸🇰", "spain id 🇪🇸",
    "spain id new 🇪🇸", "sweden id 🇸🇪", "swiss id 🇨🇭", "uae id 🇦🇪", "ukraine id 🇺🇦", "turkey id 🇹🇷",
    "luxembourg residence permit 🇱🇺"
],
"Residence Permit 🏠": [
    "uk residence card 🇬🇧", "uk residence card new 🇬🇧", "russia residence permit 🇷🇺",
    "france residence card 🇫🇷", "canada residence card 🇨🇦", "malta residence permit 🇲🇹",
    "netherlands residence card 🇳🇱", "poland residence permit 🇵🇱", "greece residence permit 🇬🇷",
    "cyprus residence permit 🇨🇾", "uae residence permit card 🇦🇪",
    "estonia residence permit 🇪🇪", "estonia residence permit new 🇪🇪",
    "italy residence permit 🇮🇹", "portugal residence permit 🇵🇹"
],
"Utility Bills 🧾": [
    "bbva statement 🇺🇸", "tmobile bill pdf 🇺🇸", "california bill 🇺🇸", "texas bill 🇺🇸",
    "scana bill 🇺🇸", "china power bill 🇨🇳", "belgium bill 🇧🇪", "italy bill 🇮🇹",
    "uk bill scottish power 🇬🇧", "uk bill ee 🇬🇧", "canada bill rogers 🇨🇦"
],
  "Bank Statements 🏦": [
    "citibank statement pdf 🇺🇸", "bank of america statement 🇺🇸",
    "chase statement 🇺🇸", "nets statement 🇸🇬", "revolut statement 🇬🇧",
    "postbank statement 🇩🇪", "barclays statement 🇬🇧"
]
}
documents1 = {
    "Паспорт 📘": [
    "usa passport 🇺🇸", "uk passport 🇬🇧", "china passport 🇨🇳", "germany passport 🇩🇪",
    "france passport 🇫🇷", "canada passport 🇨🇦", "armenia passport 🇦🇲", "australia passport 🇦🇺",
    "austria passport 🇦🇹", "bangladesh passport 🇧🇩", "belarus passport 🇧🇾", "brazil passport 🇧🇷",
    "belgium passport 🇧🇪", "cameroon passport 🇨🇲", "croatia passport 🇭🇷", "czech passport 🇨🇿",
    "denmark passport 🇩🇰", "dominican republic passport 🇩🇴", "egypt passport 🇪🇬",
    "estonia passport 🇪🇪", "finland passport 🇫🇮", "georgia passport 🇬🇪", "greece passport 🇬🇷",
    "hungary passport 🇭🇺", "india passport 🇮🇳", "indonesia passport 🇮🇩",
    "ireland passport 🇮🇪", "israel passport 🇮🇱", "italy passport 🇮🇹", "ivory coast passport 🇨🇮",
    "kazakhstan passport 🇰🇿", "kenya passport 🇰🇪", "latvia passport 🇱🇻", "malaysia passport 🇲🇾",
    "mexico passport 🇲🇽", "netherlands passport 🇳🇱", "new zealand passport 🇳🇿",
    "norway passport 🇳🇴", "peru passport 🇵🇪", "poland passport 🇵🇱", "serbia passport 🇷🇸",
    "singapore passport 🇸🇬", "slovakia passport 🇸🇰", "slovenia passport 🇸🇮", "rsa passport 🇿🇦",
    "russia passport 🇷🇺", "russia passport old 🇷🇺", "russia external passport 1 🇷🇺",
    "south korea passport 🇰🇷", "spain passport 🇪🇸", "sweden passport 🇸🇪", "swiss passport 🇨🇭",
    "taiwan id 🇹🇼", "thailand passport newtt 🇹🇭", "uae passport 🇦🇪", "ukraine passport 🇺🇦",
    "turkey passport 🇹🇷", "venezuela passport 🇻🇪", "vietnam passport 🇻🇳", "chad passport 🇹🇩"
],
    "Водительские права 🪪": [
    "dl ri 🇺🇸", "dl texas 🇺🇸", "dl nm 🇺🇸", "dl la 🇺🇸", "dl michigan 🇺🇸", "dl mississippi 🇺🇸",
    "dl oklahoma 🇺🇸", "dl kentucky 🇺🇸", "dl maine 🇺🇸", "dl wyoming 🇺🇸", "dl sc 🇺🇸", "dl vermont 🇺🇸",
    "dl oregon 🇺🇸", "dl nebraska 🇺🇸", "dl nevada 🇺🇸", "dl nh 🇺🇸", "dl tennessee 🇺🇸", "dl texas new 🇺🇸",
    "dl montana 🇺🇸", "dl sd 🇺🇸", "dl hawaii 🇺🇸", "dl alaska 🇺🇸", "dl nc 🇺🇸", "dl delaware 🇺🇸",
    "dl connecticut 🇺🇸", "dl ks 🇺🇸", "dl texas old 🇺🇸", "dl id 🇺🇸", "dl nd 🇺🇸", "dl iowa 🇺🇸",
    "dl az 🇺🇸", "dl mo 🇺🇸", "dl minnesota 🇺🇸", "dl ga 🇺🇸", "dl ut 🇺🇸", "dl il 🇺🇸", "dl md 🇺🇸",
    "dl wi 🇺🇸", "dl va 🇺🇸", "dl wa 🇺🇸", "dl colorado 🇺🇸", "dl al 🇺🇸", "dl wv 🇺🇸", "dl ny 🇺🇸",
    "dl ar 🇺🇸", "dl ca 🇺🇸", "dl pa 🇺🇸", "dl ma 🇺🇸", "dl florida 🇺🇸", "dl nj 🇺🇸", "dl indiana 🇺🇸",
    "dl ohio 🇺🇸", "uk dl 🇬🇧", "uk dl new 🇬🇧", "russia dl 🇷🇺", "russia dl 2 🇷🇺", "france dl 🇫🇷",
    "australia dl 🇦🇺", "australia queensland dl 🇦🇺", "austria dl 🇦🇹", "belarus dl 🇧🇾",
    "belgium dl 🇧🇪", "czech dl 🇨🇿", "denmark dl 🇩🇰", "estonia dl 🇪🇪", "finland dl 🇫🇮",
    "germany dl 🇩🇪", "greece dl 🇬🇷", "ireland dl 🇮🇪", "israel dl 🇮🇱", "italy dl 🇮🇹",
    "japan dl 🇯🇵", "kazakhstan dl 🇰🇿", "nigeria dl 🇳🇬", "norway dl 🇳🇴", "poland dl 🇵🇱",
    "romania dl 🇷🇴", "slovakia dl 🇸🇰", "south korea dl 🇰🇷", "spain dl 🇪🇸", "sweden dl 🇸🇪"
],
    "ID Карты 🆔": [
    "usa id 🇺🇸", "uk id 🇬🇧", "china id 🇨🇳", "germany id 🇩🇪", "france id 🇫🇷", "austria id 🇦🇹",
    "belgium id 🇧🇪", "bulgaria passport 🇧🇬", "czech id 🇨🇿", "estonia id 🇪🇪", "finland id 🇫🇮",
    "greece id card 🇬🇷", "hungary id 🇭🇺", "ireland passport card 🇮🇪", "italy id 🇮🇹",
    "kazakhstan id 🇰🇿", "latvia id 🇱🇻", "lithuania residense card 🇱🇹", "malaysia id 🇲🇾",
    "netherlands id 🇳🇱", "north macedonia id card 🇲🇰", "norway id 🇳🇴", "poland id 🇵🇱",
    "romania id 🇷🇴", "serbia id 🇷🇸", "singapore id 🇸🇬", "slovakia id 🇸🇰", "spain id 🇪🇸",
    "spain id new 🇪🇸", "sweden id 🇸🇪", "swiss id 🇨🇭", "uae id 🇦🇪", "ukraine id 🇺🇦", "turkey id 🇹🇷",
    "luxembourg residence permit 🇱🇺"
],
"Вид на жительство 🏠": [
    "uk residence card 🇬🇧", "uk residence card new 🇬🇧", "russia residence permit 🇷🇺",
    "france residence card 🇫🇷", "canada residence card 🇨🇦", "malta residence permit 🇲🇹",
    "netherlands residence card 🇳🇱", "poland residence permit 🇵🇱", "greece residence permit 🇬🇷",
    "cyprus residence permit 🇨🇾", "uae residence permit card 🇦🇪",
    "estonia residence permit 🇪🇪", "estonia residence permit new 🇪🇪",
    "italy residence permit 🇮🇹", "portugal residence permit 🇵🇹"
],
"Коммунальные услуги 🧾": [
    "bbva statement 🇺🇸", "tmobile bill pdf 🇺🇸", "california bill 🇺🇸", "texas bill 🇺🇸",
    "scana bill 🇺🇸", "china power bill 🇨🇳", "belgium bill 🇧🇪", "italy bill 🇮🇹",
    "uk bill scottish power 🇬🇧", "uk bill ee 🇬🇧", "canada bill rogers 🇨🇦"
],
  "Выписки из банка 🏦": [
    "citibank statement pdf 🇺🇸", "bank of america statement 🇺🇸",
    "chase statement 🇺🇸", "nets statement 🇸🇬", "revolut statement 🇬🇧",
    "postbank statement 🇩🇪", "barclays statement 🇬🇧"
]
}

bot = telebot.TeleBot(TOKEN)
def glavnoe_menu(chatid):
        # Удаляем данные о текущем шаге и процессе, если они есть
    if chatid in current_step:
        del current_step[chatid]
    if chatid in user_data:
        del user_data[chatid]        

    
    if user_language[chatid] == "en":
        markup = types.ReplyKeyboardMarkup()
        create_document_button = types.KeyboardButton("Create Document📃")
        create_document_button1 = types.KeyboardButton("View Profile🏦")
        create_document_button2 = types.KeyboardButton("Top up Balance💵")
        create_document_button3 = types.KeyboardButton("Rules")
        create_document_button4 = types.KeyboardButton("Channel📡")
        create_document_button5 = types.KeyboardButton("Support💬")
        create_document_button6 = types.KeyboardButton("FAQ❓")
        markup.add(create_document_button)
        markup.add(create_document_button1)
        markup.add(create_document_button2)
        markup.row(create_document_button3,create_document_button4)
        markup.row(create_document_button5,create_document_button6)
        markup.add( types.KeyboardButton("Invite friends📩"))
        if str(chatid) in get_all_admins_ids():
            markup.add( types.KeyboardButton("Рассылка"))
            markup.add( types.KeyboardButton("Добавить админов"))
            markup.add( types.KeyboardButton("Убрать админов"))
            markup.add( types.KeyboardButton("Пользователи"))
            markup.add( types.KeyboardButton("Изменить реферал всем"))


        # Отправляем приветственное сообщение и показываем кнопку
        bot.send_message(chatid, "Click the button below to get started.", reply_markup=markup)
    elif user_language[chatid] == "ru":
        markup = types.ReplyKeyboardMarkup()
        create_document_button = types.KeyboardButton("Создать документ📃")
        create_document_button1 = types.KeyboardButton("Посмотреть профиль🏦")
        create_document_button2 = types.KeyboardButton("Пополнить баланс💵")
        create_document_button3 = types.KeyboardButton("правила⚖️")
        create_document_button4 = types.KeyboardButton("канал📡")
        create_document_button5 = types.KeyboardButton("Поддержка💬")
        create_document_button6 = types.KeyboardButton("FAQ❓")
        markup.add(create_document_button)
        markup.add(create_document_button1)
        markup.add(create_document_button2)
        markup.row(create_document_button3,create_document_button4)
        markup.row(create_document_button5,create_document_button6)
        markup.add( types.KeyboardButton("Пригласить друзей📩"))

        if str(chatid) in get_all_admins_ids():
            markup.add( types.KeyboardButton("Рассылка"))
            markup.add( types.KeyboardButton("Добавить админов"))
            markup.add( types.KeyboardButton("Убрать админов"))
            markup.add( types.KeyboardButton("Пользователи"))
            markup.add( types.KeyboardButton("Изменить реферал всем"))

        # Отправляем приветственное сообщение и показываем кнопку
        bot.send_message(chatid, "Нажми на кнопку ниже, чтобы начать.", reply_markup=markup)

def add_user(chatid, username, name, message):
    ref = db.reference(f'/users/{chatid}')
    user = ref.get()

    if user is None:  # Если пользователь еще не существует
        user_data = {
            'username': username,
            'chatid': chatid,
            'name': name,
            'registration_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'balance': 0,
            'referal(%)': 10,
        }
        ref.set(user_data)  # Добавляем нового пользователя
        print(f"Пользователь {username} добавлен в базу данных.")
        if message.text.startswith('/start'):
            referrer_id = message.text.split(' ')[-1]  # Получаем ID реферера из URL-параметра
        # Сохраняем информацию в Firebase, если реферер есть
        user_id = message.chat.id
        user_ref = db.reference(f'users/{user_id}')
        # Проверяем, есть ли реферер
        if referrer_id:
            user_ref.set({
                'username': username,
                'chatid': chatid,
                'name': name,
                'registration_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'balance': 0,
                'referal(%)': 10,
                'referrer': referrer_id  
            })
    else:
        print(f"Пользователь {username} уже существует.")

    
        

    
def get_user_balance(chatid):
    ref = db.reference(f'/users/{chatid}/balance')  # Ссылка на конкретное поле "balance" для пользователя
    balance = ref.get()  # Получаем значение balance для пользователя
    return balance
def update_user_balance(chatid, amount):
    ref = db.reference(f'/users/{chatid}/balance')  # Ссылка на поле balance пользователя
    current_balance = ref.get()  # Получаем текущий баланс пользователя
    if current_balance is not None:
        new_balance = current_balance + amount  # Увеличиваем баланс на указанную сумму (например, amount)
        ref.set(new_balance)  # Обновляем значение баланса в базе данных
        print(f"Баланс пользователя {chatid} обновлен. Новый баланс: {new_balance}")
    else:
        print(f"Пользователь с chatid {chatid} не найден.")

def save_to_firebase(path, value):
    # Генерация ключа как текущее время (метка времени в секундах)
    key = str(int(time.time()))  # метка времени в секундах
    # Данные для записи
    data = {key: value}
    
    # Сохранение данных в Firebase Realtime Database
    ref = db.reference(path)
    ref.update(data)

def generate(user, chatid):
    # Открытие файла, соответствующего chatid
    data = {
            "data": json.dumps(user["main_shablon"]),
            "generator": user["slug"]
        }

    with open(f'{str(chatid)}_1.jpg', 'rb') as file:
        files = {'image1': (f'{str(chatid)+".jpg"}', file)}

        
        if os.path.exists(f'{str(chatid)}_2.jpg'):
            with open(f'{str(chatid)}_2.jpg', 'rb') as file2:
                files['image2'] = (f'{str(chatid) + "_2.jpg"}', file2)
                response = requests.post(generate_url, data=data, files=files)


                if response.status_code == 201:
                    data = response.json()
                    print("pay", data["task_id"])
                    bot.send_message(chatid, "Ожидайте, фотография генерируется...",reply_markup=types.ReplyKeyboardRemove())
                    time.sleep(5)

                    pay = requests.get("https://api.verifblog.com/api/integration/generation-status/"+data["task_id"],params = {"_": time.time()}).json()
                    while pay["task_status"]!="end" and pay["task_status"]!="user_code_error" :
                        time.sleep(3)
                        print(pay)
                        pay = requests.get("https://api.verifblog.com/api/integration/generation-status/"+data["task_id"],params = {"_": time.time()}).json()
                    if pay["task_status"]=="0":
                        bot.send_message(chatid, "У вас возникла ошибка при вводе данных. Пожалуйста, повторите попытку")

                    pay = requests.post(pay_url,data={"task_id":data["task_id"]},auth = auth)
                    print(pay.text)

                    url = str(pay.json()["image_url"]).replace("old.verif.tools","api.verifblog.com")

                    name = str(chatid) + url.split("/")[-1]
                    response = requests.get(url)
                    if response.status_code == 200:
                        with open(name, "wb") as file:
                            file.write(response.content)

                        # Отправляем фотографию как локальный файл
                        with open(name, "rb") as photo:
                            bot.send_document(chatid, photo)

                    save_to_firebase(f"users/{chatid}/orders",url)
                else:
 
                    bot.send_message(chatid, "У вас возникла ошибка при вводе данных. Пожалуйста, повторите попытку")
            os.remove(f'{str(chatid)}_2.jpg')
        
        else:
            response = requests.post(generate_url, data=data, files=files)


            if response.status_code == 201:
                data = response.json()
                print("pay", data["task_id"])
                bot.send_message(chatid, "Ожидайте, фотография генерируется...",reply_markup=types.ReplyKeyboardRemove())
                time.sleep(5)

                pay = requests.get("https://api.verifblog.com/api/integration/generation-status/"+data["task_id"],params = {"_": time.time()}).json()
                while pay["task_status"]!="end":
                    time.sleep(3)
                    print(pay)
                    pay = requests.get("https://api.verifblog.com/api/integration/generation-status/"+data["task_id"],params = {"_": time.time()}).json()
                pay = requests.post(pay_url,data={"task_id":data["task_id"]},auth = auth)
                print(pay.text)

                url = str(pay.json()["image_url"]).replace("old.verif.tools","api.verifblog.com")

                response = requests.get(url)
                name = str(chatid) + url.split("/")[-1]
                if response.status_code == 200:
                    with open(name, "wb") as file:
                        file.write(response.content)

                    # Отправляем фотографию как локальный файл
                    with open(name, "rb") as photo:
                        bot.send_document(chatid, photo)
                save_to_firebase(f"users/{chatid}/orders",url)
            else:
                print(response.text)
                bot.send_message(chatid, "У вас возникла ошибка при вводе данных. Пожалуйста, повторите попытку")
    glavnoe_menu(chatid)
def generatebonk(user, chatid):

    data = {
            "data": json.dumps(user["main_shablon"]),
            "generator": user["slug"]
        }
    
    files = {key: (None, value) for key, value in data.items()}

    response = requests.post(generate_url, files=files)
    if response.status_code == 201:
        data = response.json()
        print("pay", data["task_id"])
        bot.send_message(chatid, "Ожидайте, фотография генерируется...",reply_markup=types.ReplyKeyboardRemove())
        time.sleep(5)

        pay = requests.get("https://api.verifblog.com/api/integration/generation-status/"+data["task_id"],params = {"_": time.time()}).json()
        while pay["task_status"]!="end" and pay["task_status"]!="user_code_error" :
            time.sleep(3)
            print(pay)
            pay = requests.get("https://api.verifblog.com/api/integration/generation-status/"+data["task_id"],params = {"_": time.time()}).json()
        if pay["task_status"]=="0":
            bot.send_message(chatid, "У вас возникла ошибка при вводе данных. Пожалуйста, повторите попытку")
            print(pay)
            return

        pay = requests.post(pay_url,data={"task_id":data["task_id"]},auth = auth)
        print(pay.text)

        url = str(pay.json()["image_url"]).replace("old.verif.tools","api.verifblog.com")

        response = requests.get(url)
        name = str(chatid) + url.split("/")[-1]
        if response.status_code == 200:
            with open(name, "wb") as file:
                file.write(response.content)
    
            # Отправляем фотографию как локальный файл
            with open(name, "rb") as photo:
                bot.send_document(chatid, photo)
        else:
            print("Ошибка загрузки изображения")
        save_to_firebase(f"users/{chatid}/orders",url)
    else:
        print (response.json())
        bot.send_message(chatid, "У вас возникла ошибка при вводе данных. Пожалуйста, повторите попытку")

    glavnoe_menu(chatid)
def get_all_user_ids():
    # Ссылка на узел /users
    ref = db.reference('users')
    
    # Получаем все данные из узла /users
    users_data = ref.get()
    
    # Если данные существуют, извлекаем ключи (IDs)
    if users_data:
        user_ids = list(users_data.keys())
        return user_ids
    else:
        print("Нет данных в узле /users.")
        return []
def get_all_admins_ids():
    # Ссылка на узел /users
    ref = db.reference('admins')
    
    # Получаем все данные из узла /users
    users_data = ref.get()
    
    # Если данные существуют, извлекаем ключи (IDs)
    if users_data:
        user_ids = list(users_data.keys())
        
        return user_ids
    else:
        print("Нет данных в узле /users.")
        return []
def get_from_fb(path):
    ref = db.reference(path)  # Ссылка на конкретное поле "balance" для пользователя
    balance = ref.get()  # Получаем значение balance для пользователя
    return balance

 
def update_balance(user_id, amount):
    # Ссылка на баланс пользователя
    user_ref = db.reference(f'users/{user_id}/balance')
    
    # Получаем текущий баланс
    current_balance = user_ref.get()
    if current_balance is None:
        current_balance = 0
    
    # Обновляем баланс
    new_balance = current_balance + amount
    user_ref.set(new_balance)
    print(f"Баланс пользователя {user_id} обновлён: {new_balance} USDT")
        

CRYPTO_PAY_API_TOKEN = "306451:AAjbwrpWlNK645gqy0Z01QaCgVBchFpZi7I"
CRYPTO_PAY_URL = "https://pay.crypt.bot/api/" 
 
@bot.message_handler(func=lambda message: get_from_fb(f"users/{message.chat.id}/ban") =="да" )
def ignore_banned_user(message):
    bot.delete_message(message.chat.id, message.message_id)
@bot.message_handler (commands=['balance'])
def check_balance(message):
    user_id = str(message.chat.id)
    # Получаем баланс из Realtime Database
    user_ref = db.reference(f'users/{user_id}/balance')
    balance = user_ref.get()
    if balance is None:
        balance = 0
    if user_language[message.chat.id]=="ru":
        bot.reply_to(message, f"Ваш баланс: {balance} USDT")
    else:
        bot.reply_to(message, f"Your balance: {balance} USDT")
active_invoices = {}

# Команда для пополнения баланса
@bot.message_handler(func=lambda message: message.text =="Пополнить баланс💵" or message.text == "Top up Balance💵")
def topup_balance(message):
    user_id = str(message.chat.id)
    if user_language.get(message.chat.id) == "ru":
        bot.reply_to(message, "Введите сумму пополнения в $ (например, 10):")
    else:
        bot.reply_to(message, "Enter the top-up amount in $ (e.g., 10):")
    
    bot.register_next_step_handler(message, process_topup_amount)

def process_topup_amount(message):
    try:
        amount = float(message.text)
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        
        # Создаем инвойс через Crypto Bot API
        payload = {
            "asset": "USDT",  # Валюта
            "amount": str(amount),  # Сумма пополнения
            "token": CRYPTO_PAY_API_TOKEN,
            "description": "Пополнение баланса бота",
            "payload": str(message.chat.id)  # Сохраняем ID пользователя
        }
        headers = {
        "Crypto-Pay-API-Token": CRYPTO_PAY_API_TOKEN
        }
        response = requests.post(f"{CRYPTO_PAY_URL}createInvoice", json=payload, headers=headers)
        
        result = response.json()
        print(result)
        # Проверяем ответ от Crypto Bot
        if result.get("ok"):
            pay_url = result["result"]["pay_url"]
            invoice_id = result["result"]["invoice_id"]  # ID инвойса для проверки статуса

            # Сохраняем инвойс
            active_invoices[invoice_id] = {
                "user_id": message.chat.id,
                "amount": amount,
                "status": "pending"
            }

            if user_language.get(message.chat.id) == "ru":
                bot.reply_to(message, f"Оплатите по ссылке: {pay_url}")
            else:
                bot.reply_to(message, f"Pay using this link: {pay_url}")
        else:
            if user_language.get(message.chat.id) == "ru":
                bot.reply_to(message, "Не удалось создать счет. Попробуйте позже.")
            else:
                bot.reply_to(message, "Failed to create the invoice. Please try again later.")

    except ValueError:
        if user_language.get(message.chat.id) == "ru":
            bot.reply_to(message, "Введите корректную сумму!")
        else:
            bot.reply_to(message, "Enter a valid amount!")

# Проверяем статус инвойсов каждые 10 секунд
def check_invoices():
    while True:
        headers = {
        "Crypto-Pay-API-Token": CRYPTO_PAY_API_TOKEN
        }
        for invoice_id, invoice_data in list(active_invoices.items()):
            response = requests.post(f"{CRYPTO_PAY_URL}getInvoices", json={"invoice_id": invoice_id}, headers=headers)
            result = response.json()
            print(result)
            if result.get("ok") and result['result']['items'][0]['status']=="paid":
                user_id = invoice_data["user_id"]
                amount = invoice_data["amount"]

                # Обновляем баланс в Firebase
                user_ref = db.reference(f'users/{user_id}/balance')
                current_balance = user_ref.get() or 0
                new_balance = current_balance + amount
                user_ref.set(new_balance)
                ref = db.reference(f'/users/{user_id}/referrer')
                user = ref.get()
                x =float( get_from_fb(f"users/{user}/referal(%)"))
                print(user)
                if not user is None:
                    update_user_balance(int(user),amount*x/100)
                    if user_language.get(user_id) == "ru":
                        bot.send_message(int(user),"Ваш баланс пополнен на " +str(amount*x/100)+"$")
                    else:
                        bot.send_message(int(user),"Your balance has been topped up by "+str(amount*x/100)+"$")

                if user_language.get(user_id) == "ru":
                    bot.send_message(user_id, f"Ваш баланс пополнен на {amount} USDT!")
                else:
                    bot.send_message(user_id, f"Your balance has been topped up by {amount} USDT!")

                # Удаляем инвойс из списка
                del active_invoices[invoice_id]

        time.sleep(10)  # Ждем перед следующим циклом проверки

# Запуск проверки инвойсов в отдельном потоке
import threading
invoice_checker_thread = threading.Thread(target=check_invoices, daemon=True)
invoice_checker_thread.start()



@bot.message_handler(commands=['start'])
def start_handler(message):
    chat_id = message.chat.id

    # Создаем клавиатуру для выбора языка
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row("🇬🇧 English", "🇷🇺 Русский")  # Добавляем кнопки языков
    bot.send_message(chat_id, "Please select your language / Пожалуйста, выберите язык:", reply_markup=markup)
    user_language[chat_id] = None  # Ожидание выбора языка
    chatid = message.chat.id
    username = message.from_user.username  # Получаем username пользователя
    name = message.from_user.full_name
    add_user(chatid,username,name,message)


@bot.message_handler(func=lambda message: message.text.lower() == "пригласить друзей📩" or message.text.lower() == "invite friends📩")
def invite_friends(message):
    user_id = message.chat.id

    # Получаем реферальную ссылку
    ref_link = f"https://t.me/fDocumentBot?start={user_id}"
    
    # Отправляем ссылку пользователю
    if user_language[user_id]=="ru":
        bot.send_message(message.chat.id, f"Вот твоя реферальная ссылка: {ref_link}")
    else:
        bot.send_message(message.chat.id, f"Your referal link: {ref_link}")


@bot.message_handler(func=lambda message: message.chat.id in user_language and user_language[message.chat.id] is None)
def language_selection_handler(message):
    chat_id = message.chat.id
    text = message.text

    if text == "🇬🇧 English":
        markup = types.ReplyKeyboardMarkup()
        user_language[chat_id] = "en"
        create_document_button = types.KeyboardButton("Create Document📃")
        create_document_button1 = types.KeyboardButton("View Profile🏦")
        create_document_button2 = types.KeyboardButton("Top up Balance💵")
        create_document_button3 = types.KeyboardButton("Rules⚖️")
        create_document_button4 = types.KeyboardButton("Channel📡")
        create_document_button5 = types.KeyboardButton("Support💬")
        create_document_button6 = types.KeyboardButton("FAQ❓")
        markup.add(create_document_button)
        markup.add(create_document_button1)
        markup.add(create_document_button2)
        markup.row(create_document_button3,create_document_button4)
        markup.row(create_document_button5,create_document_button6)
        markup.add( types.KeyboardButton("Invite friends📩"))
        chatid = message.chat.id
        username = message.from_user.username  # Получаем username пользователя
        name = message.from_user.full_name
        add_user(chatid,username, name,message)
        if str(chat_id) in get_all_admins_ids():
            markup.add( types.KeyboardButton("Рассылка"))
            markup.add( types.KeyboardButton("Добавить админов"))
            markup.add( types.KeyboardButton("Убрать админов"))
            markup.add( types.KeyboardButton("Пользователи"))
            markup.add( types.KeyboardButton("Изменить реферал всем"))

        # Отправляем приветственное сообщение и показываем кнопку
        bot.send_message(message.chat.id, "Hello! I will help you create a document. Click the button below to get started.", reply_markup=markup)
    elif text == "🇷🇺 Русский":
        user_language[chat_id] = "ru"
        markup = types.ReplyKeyboardMarkup()
        create_document_button = types.KeyboardButton("Создать документ📃")
        create_document_button1 = types.KeyboardButton("Посмотреть профиль🏦")
        create_document_button2 = types.KeyboardButton("Пополнить баланс💵")
        create_document_button3 = types.KeyboardButton("правила⚖️")
        create_document_button4 = types.KeyboardButton("канал📡")
        create_document_button5 = types.KeyboardButton("Поддержка💬")
        create_document_button6 = types.KeyboardButton("FAQ❓")

        markup.add(create_document_button)
        markup.add(create_document_button1)
        markup.add(create_document_button2)
        markup.row(create_document_button3,create_document_button4)
        markup.row(create_document_button5,create_document_button6)
        markup.add( types.KeyboardButton("Пригласить друзей📩"))

        if str(chat_id) in get_all_admins_ids():
            markup.add( types.KeyboardButton("Рассылка"))
            markup.add( types.KeyboardButton("Добавить админов"))
            markup.add( types.KeyboardButton("Убрать админов"))
            markup.add( types.KeyboardButton("Пользователи"))
            markup.add( types.KeyboardButton("Изменить реферал всем"))


        
             
        chatid = message.chat.id
        username = message.from_user.username  # Получаем username пользователя
        name = message.from_user.full_name
        add_user(chatid,username, name,message)
        # Отправляем приветственное сообщение и показываем кнопку
        bot.send_message(message.chat.id, "Привет! Я помогу тебе создать документ. Нажми на кнопку ниже, чтобы начать.", reply_markup=markup)
@bot.message_handler(func = lambda message:message.chat.id not in user_language)
def handler_rerae(message):
    user_language[message.chat.id] = "ru"


@bot.message_handler(func=lambda message: message.text == "правила⚖️")
def x(message):
    bot.send_message(message.chat.id,get_from_fb("soobshenya/rules_rus"))


@bot.message_handler(func=lambda message: message.text == "канал📡")
def x(message):
    bot.send_message(message.chat.id,get_from_fb("soobshenya/channel_rus"))


@bot.message_handler(func=lambda message: message.text == "Поддержка💬")
def x(message):
    bot.send_message(message.chat.id,get_from_fb("soobshenya/support_rus"))


@bot.message_handler(func=lambda message: message.text == "FAQ❓" and user_language[message.chat.id]=="ru")
def x(message):
    bot.send_message(message.chat.id,get_from_fb("soobshenya/faq_rus"))


@bot.message_handler(func=lambda message: message.text == "Rules⚖️")
def x(message):
    bot.send_message(message.chat.id,get_from_fb("soobshenya/rules_eng"))


@bot.message_handler(func=lambda message: message.text == "Channel📡")
def x(message):
    bot.send_message(message.chat.id,get_from_fb("soobshenya/channel_eng"))


@bot.message_handler(func=lambda message: message.text == "Support💬")
def x(message):
    bot.send_message(message.chat.id,get_from_fb("soobshenya/support_eng"))


@bot.message_handler(func=lambda message: message.text == "FAQ❓" and user_language[message.chat.id]=="en")
def x(message):
    bot.send_message(message.chat.id,get_from_fb("soobshenya/faq_eng"))
    






@bot.message_handler(func=lambda message: message.text == "Посмотреть профиль🏦" or message.text == "View Profile🏦")
def handle_create_document(message):
 
    balance = get_user_balance(message.chat.id)
    name = message.from_user.full_name
    referers = ""
    for i in get_all_user_ids():
        if get_from_fb(f"users/{str(i)}/referrer")==str(message.chat.id):
            referers+=f"{get_from_fb(f'users/{str(i)}/username')}\n"

    if user_language[message.chat.id]=="ru":
        bot.send_message(message.chat.id, f"Имя: {name}\nБаланс:{balance}$\nрефералы:\n{referers}")
    else:
        bot.send_message(message.chat.id, f"Name: {name}\nBalance:{balance}$\nreferrers:\n{referers}")

# Обработчик нажатия кнопки "Создать документ"
@bot.message_handler(func=lambda message: message.text == "Создать документ📃" or message.text == "Create Document📃")
def handle_create_document(message):
    # Создаем клавиатуру с типами документов
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if user_language[message.chat.id]=="ru":
        markup.add("назад")
        for category in documents1.keys():
            markup.add(types.KeyboardButton(category))
    else:
        markup.add("back")
        for category in documents.keys():
            markup.add(types.KeyboardButton(category))    
    
    # Отправляем сообщение с выбором типа документа
    if user_language[message.chat.id]=="ru":
        bot.send_message(message.chat.id, "Выберите тип документа:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Select document type:", reply_markup=markup)
        
user_cat={}
# Обработчик выбора типа документа
@bot.message_handler(func=lambda message: message.text in documents.keys() or message.text in documents1.keys())
def handle_document_selection(message):
    # Получаем выбранную категорию
    
    category = message.text
    # Создаем клавиатуру с документами внутри выбранной категории
    markup = types.ReplyKeyboardMarkup(row_width=2)
    if user_language[message.chat.id]=="ru":
        markup.add(types.KeyboardButton("назад"))
        for doc in documents1[category]:
            markup.add(types.KeyboardButton(doc))
    else:
        markup.add(types.KeyboardButton("back"))
        for doc in documents[category]:
            markup.add(types.KeyboardButton(doc))
    user_cat[message.chat.id]=category

    
    # Отправляем сообщение с выбором конкретного документа
    if user_language[message.chat.id]=="ru":
        bot.send_message(message.chat.id, f"Выберите документ из категории {category}:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, f"Select a document from a category {category}:", reply_markup=markup)

# Обработчик выбора конкретного документа
@bot.message_handler(func=lambda message: any(message.text in docs for docs in documents.values()) or any(message.text in docs for docs in documents1.values()))
def handle_document_choice(message):
    # Получаем выбранный документ
    selected_document = message.text
    # Выполнение функции для выбранного документа (ваша логика)
    # Пример выполнения функции:

    execute_function_for_document(selected_document, message)

def execute_function_for_document(document, message):
    document=document.split(" ")
    doc=''
    for i in document:
        if i!=document[-1]:
            if i==document[0]:
                doc+=i
            else:
                doc+="_"+i    

    GetBlank(message.chat.id, doc)
    

def GetGenerateData(data):
    response = requests.get(get_generator_url+data).text
    return  json.loads(response)

def GetBlank(chatid, data):
    """Запускает процесс сбора данных."""
    shablon = GetGenerateData(data)
    user_data[chatid] = {"price": str(float(shablon["price"])+float(get_from_fb("комиссия"))), "main_shablon": {}, "steps": shablon["steps"],"slug": shablon["slug"]}
    current_step[chatid] = {"step_index": 0, "field_index": 0}
    balance =float( get_user_balance(chatid))
    if balance>=float(user_data[chatid]["price"]):
        if user_data[chatid]=="ru":
            bot.send_message(chatid,"Эта услуга стоит " +str(user_data[chatid]["price"])+"$. \n Введите нужные данные, пожалуйста")
        else:
            bot.send_message(chatid,"This service costs " +str(user_data[chatid]["price"])+"$. \n Please enter the required data")

        ask_next_question(chatid)
    else:
        if user_language[chatid]=="ru":
            bot.send_message(chatid,"У вас недостаточно средств. Пожалуйста пополните счет до " +str(user_data[chatid]["price"])+"$")
        else:
            bot.send_message(chatid,"You don't have enough funds. Please top up your account up to " +str(user_data[chatid]["price"])+"$")

def ask_next_question(chatid):
    markup = types.ReplyKeyboardMarkup(row_width=5)
    if user_language[chatid] == "ru":
        create_document_button = types.KeyboardButton("пропустить")
        create_document_button1 = types.KeyboardButton("отменить")
        create_document_button2 = types.KeyboardButton("Главное меню")
    else:
        create_document_button = types.KeyboardButton("skip")
        create_document_button1 = types.KeyboardButton("cancel")
        create_document_button2 = types.KeyboardButton("Main menu")
    markup.row(create_document_button,create_document_button1)
    markup.add(create_document_button2)
    """Отправляет следующий вопрос пользователю."""
    step_index = current_step[chatid]["step_index"]
    field_index = current_step[chatid]["field_index"]
    steps = user_data[chatid]["steps"]
    
    if step_index < len(steps)-1 :
        fields = steps[step_index]["fields"]
        if field_index < len(fields):
            field = fields[field_index]
            question = f"{field['input_label']}. Example(Пример): {field['input_placeholder']}"
            user_data[chatid]["required"] = field["required"]
            bot.send_message(chatid, question, reply_markup=markup)
        else:
            # Переход к следующему шагу
            current_step[chatid]["step_index"] += 1
            current_step[chatid]["field_index"] = 0
            ask_next_question(chatid)

    else:
        # Все вопросы заданы
        finalize_blank(chatid)
        
@bot.message_handler(func=lambda message: message.text == "Добавить админов" and str(message.chat.id) in get_all_admins_ids())
def x(message):
    bot.send_message(message.chat.id, "Напишите никнейм админа")
    admin_step[message.chat.id]="waiting"
@bot.message_handler(func=lambda message: message.text == "Убрать админов" and str(message.chat.id) in get_all_admins_ids())
def x(message):
    bot.send_message(message.chat.id, "Напишите никнейм админа")
    admin_step[message.chat.id]="waitingfor"
@bot.message_handler(func=lambda message: admin_step.get(message.chat.id) == "waitingfor" )
def x(message):
    
    users = get_all_user_ids()
    
    for i in users:
        useri = get_from_fb(f"users/{i}")
        if str(useri["username"]).lower()==message.text.lower().replace("@",""):
            db.reference("admins/"+i).delete()
            bot.send_message(message.chat.id, f"Админ {message.text} удален")
        
    admin_step[message.chat.id]="complete"

@bot.message_handler(func=lambda message: admin_step.get(message.chat.id) == "waiting" )
def x(message):
    
    users = get_all_user_ids()
    for i in users:
        print(i)
        useri = get_from_fb(f"users/{i}")
        if str(useri["username"]).lower()==message.text.lower().replace("@",""):
            db.reference("admins/").update({i:int(i)})
            bot.send_message(message.chat.id, f"Админ {message.text} добавлен")
    if get_from_fb('admins/'+i) is None:
        bot.send_message(message.chat.id, f"Этого человека нет в боте.")
    admin_step[message.chat.id]="complete"

@bot.message_handler(func=lambda message: message.text == "Пользователи" and str(message.chat.id) in get_all_admins_ids())
def x(message):

    markup = types.ReplyKeyboardMarkup()
    create_document_button = types.KeyboardButton("Все пользователи")
    create_document_button1 = types.KeyboardButton("Редактировать пользователя")
    markup.add(types.KeyboardButton("назад"))
    markup.add(create_document_button)
    markup.add(create_document_button1)

    bot.send_message(message.chat.id, "Выберите нужное действие", reply_markup=markup)
@bot.message_handler(func=lambda message: message.text == "Все пользователи" and str(message.chat.id) in get_all_admins_ids())
def x(message):

    users = get_all_user_ids()
    x=""
    for i in users:
        print(i)
        useri = get_from_fb(f"users/{i}")
        x+=f"{useri['username']} : {useri['chatid']}\n\n"
    bot.send_message(message.chat.id,x) 
@bot.message_handler(func=lambda message: message.text == "Редактировать пользователя" and str(message.chat.id) in get_all_admins_ids())
def x(message):
    admin_step[message.chat.id]="userchose"
    bot.send_message(message.chat.id,"Напишите ник пользователя через @")
@bot.message_handler(func=lambda message: admin_step.get(message.chat.id) == "userchose" )
def x(message):
    if message.text[0]=="@":
        xy = get_all_user_ids()
        z=False
        for i in xy:
            if get_from_fb(f"users/{i}/username").lower()==message.text.replace("@","").lower():
                character_step[message.chat.id]=i
                if not get_from_fb(f"users/{i}/ban") is None:
                    referers=""
                    for iks in get_all_user_ids():
                        if get_from_fb(f"users/{str(iks)}/referrer")==str(i):
                            referers+=f"{get_from_fb(f'users/{str(iks)}/username')}\n"
                    dannye=f"""
Имя:{get_from_fb("users/"+i+"/name")}
Ник:{get_from_fb("users/"+i+"/username")}
Баланс:{get_from_fb("users/"+i+"/balance")} $
Бан: Есть
Дата регистрации:{get_from_fb("users/"+i+"/registration_date")}
реферал:{get_from_fb("users/"+i+"/referal(%)")}%
рефералы:{referers}
"""
                    zakazi=""
                    try:
                        for i,j in get_from_fb(f"users/{i}/orders").items():zakazi+=i+"\n"+j+"\n\n"
                    except:zakazi="отсутствуют"
                    bot.send_message(message.chat.id,dannye)
                    markup = types.ReplyKeyboardMarkup()
                    create_document_butto = types.KeyboardButton("назад")
                    create_document_button = types.KeyboardButton("Разбанить")
                    create_document_button1 = types.KeyboardButton("Изменить баланс")
                    create_document_button2 = types.KeyboardButton("Изменить реферал")
                    markup.add(create_document_butto)
                    markup.add(create_document_button)
                    markup.add(create_document_button1)
                    markup.add(create_document_button2)
                    admin_step[message.chat.id]="readyforknop"
                    bot.send_message(message.chat.id,"заказы:\n"+zakazi,reply_markup=markup)
                else:
                    referers=""
                    for iks in get_all_user_ids():
                        if get_from_fb(f"users/{str(iks)}/referrer")==str(i):
                            referers+=f"{get_from_fb(f'users/{str(iks)}/username')}\n"
                    dannye=f"""
Имя:{get_from_fb("users/"+i+"/name")}
Ник:{get_from_fb("users/"+i+"/username")}
Баланс:{get_from_fb("users/"+i+"/balance")} $
Бан: Есть
Дата регистрации:{get_from_fb("users/"+i+"/registration_date")}
реферал:{get_from_fb("users/"+i+"/referal(%)")}%
рефералы:{referers}
"""
                    
                    try:
                        for i,j in get_from_fb(f"users/{i}/orders").items():zakazi+=i+"\n"+j+"\n\n"
                    except:zakazi="отсутствуют"
                    bot.send_message(message.chat.id,dannye)
                    markup = types.ReplyKeyboardMarkup()
                    create_document_butto = types.KeyboardButton("назад")
                    create_document_button = types.KeyboardButton("Забанить")
                    create_document_button1 = types.KeyboardButton("Изменить баланс")
                    create_document_button2 = types.KeyboardButton("Изменить реферал")
                    markup.add(create_document_butto)
                    markup.add(create_document_button)
                    markup.add(create_document_button1)
                    markup.add(create_document_button2)
                    admin_step[message.chat.id]="readyforknop"
                    bot.send_message(message.chat.id,"заказы:\n"+zakazi,reply_markup=markup)
                a=False
                
                
                break
                
            else:
                a=True
        if a==True:
            bot.send_message(message.chat.id,"такого пользователя нет")
            admin_step[message.chat.id]="complete"


    else:
        bot.send_message(message.chat.id,"Некорректное сообщение")
        glavnoe_menu(message.chat.id)  
        admin_step[message.chat.id]="complete"

@bot.message_handler(func=lambda message: admin_step.get(message.chat.id) == "readyforknop" )
def x(message):

    myuserid=character_step[message.chat.id]
    if message.text == "назад":
        admin_step[message.chat.id]="complete"
        glavnoe_menu(message.chat.id)
    if message.text=="Забанить":
        db.reference(f"users/{myuserid}").update({"ban":"да"})
        bot.send_message(message.chat.id,"Пользователь забанен")
        admin_step[message.chat.id]="complete"
        glavnoe_menu(message.chat.id)
    if message.text=="Разбанить":
        db.reference(f"users/{myuserid}/ban").delete()
        
        bot.send_message(message.chat.id,"Пользователь разбанен")
        admin_step[message.chat.id]="complete"
        glavnoe_menu(message.chat.id)
    if message.text=="Изменить баланс":
        bot.send_message(message.chat.id,"Введите значение в цифрах")
        admin_step[message.chat.id]="readyfirbal"
        
    if message.text=="Изменить реферал":
        bot.send_message(message.chat.id,"Введите значение в цифрах(целое число)")
        admin_step[message.chat.id]="readyforref"

@bot.message_handler(func=lambda message: admin_step.get(message.chat.id) == "readyfirbal" )
def x(message):
    myuserid=character_step[message.chat.id]
    db.reference(f"users/{myuserid}").update({"balance":float(message.text)})
    admin_step[message.chat.id]="complete"
    glavnoe_menu(message.chat.id)

@bot.message_handler(func=lambda message: admin_step.get(message.chat.id) == "readyforref" )
def x(message):
    myuserid=character_step[message.chat.id]
    db.reference(f"users/{myuserid}").update({"referal(%)":int(message.text)})
    admin_step[message.chat.id]="complete"
    glavnoe_menu(message.chat.id)
       
@bot.message_handler(func=lambda message: message.text == "Текст рассылки" and str(message.chat.id) in get_all_admins_ids())
def handle_text_rassilka(message):
    current_action[message.chat.id] = "text"  # Сохраняем состояние для пользователя
    bot.send_message(message.chat.id, "Введите текст для рассылки:")


@bot.message_handler(func=lambda message: message.text == "Удалить все медиа" and str(message.chat.id) in get_all_admins_ids())
def handle_media_rassilka(message):
    db.reference("rassilka/media").delete()
    bot.send_message(message.chat.id, "Медиа рассыкли удалены")

@bot.message_handler(func=lambda message: message.text == "Медиа рассылки" and str(message.chat.id) in get_all_admins_ids())
def handle_media_rassilka(message):
    current_action[message.chat.id] = "media"  # Сохраняем состояние для пользователя
    bot.send_message(message.chat.id, "Отправьте медиа для рассылки (фото или видео):")

# Обработчик получения текста для рассылки
@bot.message_handler(func=lambda message: current_action.get(message.chat.id) == "text")
def save_text_rassilka(message):
    # Сохраняем текст в Firebase
    ref = db.reference("rassilka/text")
    ref.set(message.text)
    bot.send_message(message.chat.id, "Текст для рассылки сохранён.")
    current_action.pop(message.chat.id, None)  # Сбрасываем состояние










# Обработчик получения медиа для рассылки
@bot.message_handler(content_types=["photo", "video"], func=lambda message: current_action.get(message.chat.id) == "media")
def save_media_rassilka(message):
    if message.photo:
        media_id = message.photo[-1].file_id
        media_type = "photo"
    elif message.video:
        media_id = message.video.file_id
        media_type = "video"
    else:
        bot.send_message(message.chat.id, "Неверный тип медиа. Отправьте фото или видео.")
        return

    # Сохраняем медиа в Firebase
    ref = db.reference(f"rassilka/media/{media_type}")
    ref.set(media_id)
    bot.send_message(message.chat.id, f"{media_type.capitalize()} для рассылки сохранено.")
    current_action.pop(message.chat.id, None)  # Сбрасываем состояние

@bot.message_handler(func=lambda message: message.text == "Изменить реферал всем" and str(message.chat.id) in get_all_admins_ids())
def x(message):
    admin_step[message.chat.id]="allrefedit"
    bot.send_message(message.chat.id,"Введите значение(целое число)")

              
@bot.message_handler(func=lambda message:admin_step.get(message.chat.id) == "allrefedit" )
def x(message):
    try:
        for i in get_all_user_ids():
            db.reference(f"users/{i}/").update({"referal(%)":int(message.text)})
    except:
        pass
    bot.send_message(message.chat.id,"Реферал изменен")
    admin_step[message.chat.id]="complete"
@bot.message_handler(func=lambda message: message.text == "Начать рассылку" and str(message.chat.id) in get_all_admins_ids())
def start_rassilka(message):
    # Получаем данные из Firebase
    text_ref = db.reference("rassilka/text")
    media_ref = db.reference("rassilka/media")

    text = text_ref.get()
    media = media_ref.get()

    # ID чатов для рассылки (должны быть получены отдельно)
    user_ids = get_all_user_ids() # Замените на реальные ID пользователей

    for user_id in user_ids:
        if text:
            bot.send_message(user_id, text)
        if media:
            if "photo" in media:
                bot.send_photo(user_id, media["photo"])
            if "video" in media:
                bot.send_video(user_id, media["video"])

    bot.send_message(message.chat.id, "Рассылка завершена.")


@bot.message_handler(func=lambda message: message.text in ["отменить","cancel","назад","back","Главное меню","Main menu"])
def handle_cancel(message):
    chatid = message.chat.id

    # Удаляем данные о текущем шаге и процессе, если они есть
    if chatid in current_step:
        del current_step[chatid]
    if chatid in user_data:
        del user_data[chatid]        

    
    if user_language[chatid] == "en":
        markup = types.ReplyKeyboardMarkup()
        create_document_button = types.KeyboardButton("Create Document📃")
        create_document_button1 = types.KeyboardButton("View Profile🏦")
        create_document_button2 = types.KeyboardButton("Top up Balance💵")
        create_document_button3 = types.KeyboardButton("Rules")
        create_document_button4 = types.KeyboardButton("Channel📡")
        create_document_button5 = types.KeyboardButton("Support💬")
        create_document_button6 = types.KeyboardButton("FAQ❓")
        markup.add(create_document_button)
        markup.add(create_document_button1)
        markup.add(create_document_button2)
        markup.row(create_document_button3,create_document_button4)
        markup.row(create_document_button5,create_document_button6)
        if str(chatid) in get_all_admins_ids():
            markup.add( types.KeyboardButton("Рассылка"))
            markup.add( types.KeyboardButton("Добавить админов"))
            markup.add( types.KeyboardButton("Убрать админов"))
            markup.add( types.KeyboardButton("Пользователи"))
            markup.add( types.KeyboardButton("Изменить реферал всем"))
        markup.add( types.KeyboardButton("Invite friends📩"))
        chatid = message.chat.id
        username = message.from_user.username  # Получаем username пользователя
        name = message.from_user.full_name
        add_user(chatid,username, name,message)
        # Отправляем приветственное сообщение и показываем кнопку
        bot.send_message(message.chat.id, "Click the button below to get started.", reply_markup=markup)
    elif user_language[chatid] == "ru":
        markup = types.ReplyKeyboardMarkup()
        create_document_button = types.KeyboardButton("Создать документ📃")
        create_document_button1 = types.KeyboardButton("Посмотреть профиль🏦")
        create_document_button2 = types.KeyboardButton("Пополнить баланс💵")
        create_document_button3 = types.KeyboardButton("правила⚖️")
        create_document_button4 = types.KeyboardButton("канал📡")
        create_document_button5 = types.KeyboardButton("Поддержка💬")
        create_document_button6 = types.KeyboardButton("FAQ❓")
        markup.add(create_document_button)
        markup.add(create_document_button1)
        markup.add(create_document_button2)
        markup.row(create_document_button3,create_document_button4)
        markup.row(create_document_button5,create_document_button6)
        markup.add( types.KeyboardButton("Пригласить друзей📩"))
        if str(chatid) in get_all_admins_ids():
            markup.add( types.KeyboardButton("Рассылка"))
            markup.add( types.KeyboardButton("Добавить админов"))
            markup.add( types.KeyboardButton("Убрать админов"))
            markup.add( types.KeyboardButton("Пользователи"))
            markup.add( types.KeyboardButton("Изменить реферал всем"))

        chatid = message.chat.id
        username = message.from_user.username  # Получаем username пользователя
        name = message.from_user.full_name
        add_user(chatid,username, name,message)
        # Отправляем приветственное сообщение и показываем кнопку
        bot.send_message(message.chat.id, "Нажми на кнопку ниже, чтобы начать.", reply_markup=markup)
    
@bot.message_handler(func=lambda message: message.chat.id in current_step and current_step[message.chat.id] == "waiting_for_second_photo")
def handle_photo(message):
    chatid = message.chat.id
    markup = types.ReplyKeyboardMarkup(row_width=5)
    create_document_button = types.KeyboardButton("Photo")
    create_document_button1 = types.KeyboardButton("Scan")
    create_document_button2 = types.KeyboardButton("Print")
    markup.add(create_document_button,create_document_button1,create_document_button2)
    if not message.photo:
        if user_language[chatid]=="ru":
            bot.send_message(chatid, "Вы решили пропустить отправку второй фотографии. Спасибо. Теперь выберите тип файла для сохранения",reply_markup=markup)
        else:
            bot.send_message(chatid, "You decide to skip sending the second photo. Thank you. Now select the file type to save",reply_markup=markup)

        current_step[chatid] = "waiting_for_psp"


@bot.message_handler(func=lambda message: message.chat.id in current_step and not current_step[message.chat.id] == "waiting_for_payment"and not current_step[message.chat.id] == "waiting_for_first_photo"and not current_step[message.chat.id] == "waiting_for_second_photo" and not current_step[message.chat.id] == "waittingforbg"and not current_step[message.chat.id] == "waiting_for_psp")
def handle_answer(message):
    """Обрабатывает ответ пользователя."""
    chatid = message.chat.id
    step_index = current_step[chatid]["step_index"]
    field_index = current_step[chatid]["field_index"]
    steps = user_data[chatid]["steps"]
    
    # Сохраняем ответ
    field = steps[step_index]["fields"][field_index]
    if message.text!="пропустить" and message.text!="skip":
        user_data[chatid]["main_shablon"][field["input_name"]] = message.text
        current_step[chatid]["field_index"] += 1
    elif current_step[chatid]!="waiting_for_second_photo":
        if  user_data[chatid]["required"]==False:
            user_data[chatid]["main_shablon"][field["input_name"]] = ""
            current_step[chatid]["field_index"] += 1
        else:
            user_data[chatid]["main_shablon"][field["input_name"]] = field['input_placeholder']
            current_step[chatid]["field_index"] += 1
        

    ask_next_question(chatid)
def finalize_blank(chatid):
    if not user_cat[chatid] in ["Коммунальные услуги 🧾","Выписки из банка 🏦","Bank Statements 🏦","Utility Bills 🧾"]: 
        current_step[chatid] = "waiting_for_first_photo"
        if user_language[chatid] == "ru":
            bot.send_message(chatid, "Пожалуйста, отправьте фото для завершения.")
        else:
            bot.send_message(chatid, "Please submit a photo to complete.")
    else:
        
        markup = types.ReplyKeyboardMarkup(row_width=5)
        create_document_button = types.KeyboardButton("Photo")
        create_document_button1 = types.KeyboardButton("Scan")
        create_document_button2 = types.KeyboardButton("Print")
        markup.add(create_document_button,create_document_button1,create_document_button2)
        current_step[chatid] = "waiting_for_psp"
        if user_language[chatid]=="rus":
            bot.send_message(chatid, " Теперь выберите тип файла для сохранения",reply_markup=markup)
        else:
            bot.send_message(chatid, " Now select the file type to save",reply_markup=markup)

@bot.message_handler(func=lambda message: message.chat.id in current_step and current_step[message.chat.id] == "waiting_for_payment")
def handle_payment_response(message):
    chatid = message.chat.id
    if message.text.lower() == "да" or message.text.lower() == "yes":
        update_user_balance(chatid,-float(user_data[chatid]["price"]))
        if not user_cat[chatid] in ["Коммунальные услуги 🧾","Выписки из банка 🏦","Bank Statements 🏦","Utility Bills 🧾"]:
            try:
                generate(user_data[chatid],chatid)
            except:
                bot.send_message(chatid,"ошибка со стороны сервера")
        else:
            try:
                generatebonk(user_data[chatid],chatid)
            except:
                bot.send_message(chatid,"ошибка со стороны сервера")

                
    elif message.text.lower() == "нет" or message.text.lower() == "no":
        glavnoe_menu(chatid)

    else:
        if user_language[chatid]=="ru":
            bot.send_message(chatid, "Пожалуйста, ответьте 'Да' для подтверждения или 'Нет' для отмены.")
        if user_language[chatid]=="en":
            bot.send_message(chatid, "Please answer 'Yes' to confirm or 'No' to cancel.")

@bot.message_handler(func=lambda message: message.chat.id in current_step and current_step[message.chat.id] == "waiting_for_psp")
def handle_payment_response(message):
    chatid = message.chat.id
    if message.text.lower() == "photo":
        user_data[chatid]["main_shablon"]["BACKGROUND"] = "Photo"
    elif message.text.lower() == "scan":
        user_data[chatid]["main_shablon"]["BACKGROUND"] = "Scan"
    else: 
        user_data[chatid]["main_shablon"]["BACKGROUND"] = "Print"
    markup = types.ReplyKeyboardMarkup(row_width=5)
    for i in [1,5,9,13]:
        con = types.KeyboardButton(str(i))
        con1 = types.KeyboardButton(str(i+1))
        con2 = types.KeyboardButton(str(i+2))
        con3 = types.KeyboardButton(str(i+3))
        markup.row(con,con1,con2,con3)
    if not user_cat[chatid] in ["Коммунальные услуги 🧾","Выписки из банка 🏦","Bank Statements 🏦","Utility Bills 🧾"]: 
        if user_language[chatid]=="ru":
            bot.send_message(chatid, "Напишите номер фона (число от 1 до 16)",reply_markup=markup)
        else:
            bot.send_message(chatid, "Write the background number (a number from 1 to 16)",reply_markup=markup)
        current_step[chatid] = "waittingforbg"
    else:
        markup = types.ReplyKeyboardMarkup(row_width=5)
        current_step[chatid] = "waiting_for_payment"
        if user_language[chatid]=="ru":
            create_document_button = types.KeyboardButton("Да")
            create_document_button1 = types.KeyboardButton("Нет")
            markup.add(create_document_button,create_document_button1)
            price = float(user_data.get(chatid, {}).get("price", 0))
            current_step[chatid] = "waiting_for_payment"
            bot.send_message(chatid, f"Пожалуйста, оплатите {price} $. Подтвердите оплату, отправив 'Да', или отмените, отправив 'Нет'.",reply_markup=markup)

        else:
            create_document_button = types.KeyboardButton("Yes")
            create_document_button1 = types.KeyboardButton("No")
            markup.add(create_document_button,create_document_button1)
            current_step[chatid] = "waiting_for_payment"
            price = float(user_data.get(chatid, {}).get("price", 0))
            bot.send_message(chatid, f"Please pay {price} $. Confirm payment by sending 'Yes' or cancel by sending 'No'.",reply_markup=markup)

   
@bot.message_handler(func=lambda message: message.chat.id in current_step and current_step[message.chat.id] == "waittingforbg")
def handle_payment_response(message):
    chatid = message.chat.id
    user_data[chatid]["main_shablon"]["BACKGROUND_NUMBER"] = message.text
    price = float(user_data.get(chatid, {}).get("price", 0))
    markup = types.ReplyKeyboardMarkup(row_width=5)
    if user_language[chatid]=="ru":
        create_document_button = types.KeyboardButton("Да")
        create_document_button1 = types.KeyboardButton("Нет")
        markup.add(create_document_button,create_document_button1)
        current_step[chatid] = "waiting_for_payment"
        bot.send_message(chatid, f"Пожалуйста, оплатите {price} $. Подтвердите оплату, отправив 'Да', или отмените, отправив 'Нет'.",reply_markup=markup)

    else:
        create_document_button = types.KeyboardButton("Yes")
        create_document_button1 = types.KeyboardButton("No")
        markup.add(create_document_button,create_document_button1)
        current_step[chatid] = "waiting_for_payment"
        bot.send_message(chatid, f"Please pay {price} $. Confirm payment by sending 'Yes' or cancel by sending 'No'.",reply_markup=markup)

   
 
@bot.message_handler(func=lambda message: message.chat.id in current_step and current_step[message.chat.id] == "waiting_for_first_photo")
def handle_photo(message):
    chatid = message.chat.id

    if chatid in current_step and current_step[chatid] == "waiting_for_first_photo":
        if message.photo:
            # Сохраняем первую фотографию
            photo_file_id = message.photo[-1].file_id
            file_info = bot.get_file(photo_file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            file_name = str(chatid) + "_1.jpg"
            file_path = os.path.join('', file_name)
            markup = types.ReplyKeyboardMarkup(row_width=5)
            if user_language[chatid]=="ru":
                create_document_button = types.KeyboardButton("пропустить")
            else:
                create_document_button = types.KeyboardButton("skip")
            markup.add(create_document_button)
            with open(file_path, 'wb') as new_file:
                new_file.write(downloaded_file)
            if user_language[chatid]=="ru":
                bot.send_message(chatid, "Первая фотография успешно сохранена! Теперь отправьте фотографию подписи или пропустите этот шаг.",reply_markup=markup)
            else:
                bot.send_message(chatid, "The first photo was successfully saved! Now send a photo of the signature or skip this step.",reply_markup=markup)
        else:
            response = requests.get("https://api.verifblog.com/media/generators/previews/photo_for_passport_1.jpg",stream=True)
            file_name = str(chatid) + "_1.jpg"
            file_path = os.path.join('', file_name)
            markup = types.ReplyKeyboardMarkup(row_width=5)
            if user_language[chatid]=="ru":
                create_document_button = types.KeyboardButton("пропустить")
            else:
                create_document_button = types.KeyboardButton("skip")
            markup.add(create_document_button)
            with open(file_name, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            if user_language[chatid]=="ru":
                bot.send_message(chatid, "Первое Фото пропущено. Теперь отправьте фотографию подписи или пропустите этот шаг.",reply_markup=markup)
            else:
                bot.send_message(chatid, "The first photo was successfully Skipped! Now send a photo of the signature or skip this step.",reply_markup=markup)
        current_step[chatid] = "waiting_for_second_photo"

    elif chatid in current_step and current_step[chatid] == "waiting_for_second_photo":
        if message.photo:
            # Сохраняем вторую фотографию
            photo_file_id = message.photo[-1].file_id
            file_info = bot.get_file(photo_file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            file_name = str(chatid) + "_2.jpg"
            file_path = os.path.join('', file_name)

            with open(file_path, 'wb') as new_file:
                new_file.write(downloaded_file)
                markup = types.ReplyKeyboardMarkup(row_width=5)
                create_document_button = types.KeyboardButton("Photo")
                create_document_button1 = types.KeyboardButton("Scan")
                create_document_button2 = types.KeyboardButton("Print")
                markup.add(create_document_button,create_document_button1,create_document_button2)
            if user_language[chatid]=="ru":
                bot.send_message(chatid, "Вторая фотография успешно сохранена! Спасибо. Теперь выберите тип файла для сохранения",reply_markup=markup)
            else:
                bot.send_message(chatid, "The second photo was successfully saved! Thank you. Now select the file type to save",reply_markup=markup)
                
            current_step[chatid] = "waiting_for_psp"
        else:
            new_file.write(downloaded_file)
            markup = types.ReplyKeyboardMarkup(row_width=5)
            create_document_button = types.KeyboardButton("Photo")
            create_document_button1 = types.KeyboardButton("Scan")
            create_document_button2 = types.KeyboardButton("Print")
            markup.add(create_document_button,create_document_button1,create_document_button2)
            if user_language[chatid]=="ru":
                bot.send_message(chatid, "Вы решили пропустить отправку второй фотографии. Спасибо. Теперь выберите тип файла для сохранения",reply_markup=markup)
            else:
                bot.send_message(chatid, "You decide to skip sending the second photo. Thank you. Now select the file type to save",reply_markup=markup)

            current_step[chatid] = "waiting_for_psp"
        

        

    else:
        if user_language[chatid]=="ru":
            bot.send_message(chatid, "Я не жду от вас фото. Попробуйте снова.")
        else:
            bot.send_message(chatid, "I'm not expecting a photo from you. Try again.")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    chatid = message.chat.id

    if chatid in current_step and current_step[chatid] == "waiting_for_first_photo":
        if message.photo:
            # Сохраняем первую фотографию
            photo_file_id = message.photo[-1].file_id
            file_info = bot.get_file(photo_file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            file_name = str(chatid) + "_1.jpg"
            file_path = os.path.join('', file_name)
            markup = types.ReplyKeyboardMarkup(row_width=5)
            if user_language[chatid]=="ru":
                create_document_button = types.KeyboardButton("пропустить")
            else:
                create_document_button = types.KeyboardButton("skip")
            markup.add(create_document_button)
            with open(file_path, 'wb') as new_file:
                new_file.write(downloaded_file)
            if user_language[chatid]=="ru":
                bot.send_message(chatid, "Первая фотография успешно сохранена! Теперь отправьте фотографию подписи или пропустите этот шаг.",reply_markup=markup)
            else:
                bot.send_message(chatid, "The first photo was successfully saved! Now send a photo of the signature or skip this step.",reply_markup=markup)
        else:
            response = requests.get("https://api.verifblog.com/media/generators/previews/photo_for_passport_1.jpg",stream=True)
            file_name = str(chatid) + "_1.jpg"
            file_path = os.path.join('', file_name)
            markup = types.ReplyKeyboardMarkup(row_width=5)
            if user_language[chatid]=="ru":
                create_document_button = types.KeyboardButton("пропустить")
            else:
                create_document_button = types.KeyboardButton("skip")
            markup.add(create_document_button)
            with open(file_name, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            if user_language[chatid]=="ru":
                bot.send_message(chatid, "Первое Фото пропущено. Теперь отправьте фотографию подписи или пропустите этот шаг.",reply_markup=markup)
            else:
                bot.send_message(chatid, "The first photo was successfully Skipped! Now send a photo of the signature or skip this step.",reply_markup=markup)
        current_step[chatid] = "waiting_for_second_photo"

    elif chatid in current_step and current_step[chatid] == "waiting_for_second_photo":
        if message.photo:
            # Сохраняем вторую фотографию
            photo_file_id = message.photo[-1].file_id
            file_info = bot.get_file(photo_file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            file_name = str(chatid) + "_2.jpg"
            file_path = os.path.join('', file_name)

            with open(file_path, 'wb') as new_file:
                new_file.write(downloaded_file)
                markup = types.ReplyKeyboardMarkup(row_width=5)
                create_document_button = types.KeyboardButton("Photo")
                create_document_button1 = types.KeyboardButton("Scan")
                create_document_button2 = types.KeyboardButton("Print")
                markup.add(create_document_button,create_document_button1,create_document_button2)
            if user_language[chatid]=="ru":
                bot.send_message(chatid, "Вторая фотография успешно сохранена! Спасибо. Теперь выберите тип файла для сохранения",reply_markup=markup)
            else:
                bot.send_message(chatid, "The second photo was successfully saved! Thank you. Now select the file type to save",reply_markup=markup)
                
            current_step[chatid] = "waiting_for_psp"
        else:
            new_file.write(downloaded_file)
            markup = types.ReplyKeyboardMarkup(row_width=5)
            create_document_button = types.KeyboardButton("Photo")
            create_document_button1 = types.KeyboardButton("Scan")
            create_document_button2 = types.KeyboardButton("Print")
            markup.add(create_document_button,create_document_button1,create_document_button2)
            if user_language[chatid]=="ru":
                bot.send_message(chatid, "Вы решили пропустить отправку второй фотографии. Спасибо. Теперь выберите тип файла для сохранения",reply_markup=markup)
            else:
                bot.send_message(chatid, "You decide to skip sending the second photo. Thank you. Now select the file type to save",reply_markup=markup)

            current_step[chatid] = "waiting_for_psp"
        

        

    else:
        if user_language[chatid]=="ru":
            bot.send_message(chatid, "Я не жду от вас фото. Попробуйте снова.")
        else:
            bot.send_message(chatid, "I'm not expecting a photo from you. Try again.")



    

while True:
    try:
        bot.polling()
        

    except Exception as e:
        print(f"Ошибка: {e}. Перезапуск через 5 секунд...")
        time.sleep(5)  # Задержка перед перезапуском
    else:
        break  # Выйти из цикла, если ошибок нет
