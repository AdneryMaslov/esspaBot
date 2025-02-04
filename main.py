from flask import Flask, render_template
from flask import request
from flask import Response
import requests
import json
from bs4 import BeautifulSoup as BS
import random
import os

TOKEN = "6631871232:AAFqp5DD7n1vTw6agij3UUR_XAFy7US6D2c"
TOKEN_YANDEX = "cd6b7193-b438-4b24-9d25-15f8a2a86c17"
app = Flask(__name__, template_folder='../public_html')

colors = {
    'красный': 'зеленый',
    'красный': 'зелёный'
}


def dress_up_photo_maker(chat_id, weather):
    temp = ''
    if weather > 10:
        temp = 'warm'
    else:
        temp = 'cold'
    global_path = f'/home/s/semyon2b/botesspa/public_html/{chat_id}/{temp}/up'
    all_path = os.listdir(global_path)
    file = random.choice(all_path)
    file = f'{chat_id}/{temp}/up/{file}'
    return file


def dress_down_photo_maker(chat_id, weather):
    temp = ''
    if weather > 10:
        temp = 'warm'
    else:
        temp = 'cold'
    global_path = f'/home/s/semyon2b/botesspa/public_html/{chat_id}/{temp}/down'
    all_path = os.listdir(global_path)
    file = random.choice(all_path)
    file = f'{chat_id}/{temp}/down/{file}'
    return file


def tel_send_photos(chat_id, url_photo):
    url = f'https://api.telegram.org/bot{TOKEN}/sendPhoto'
    photo = url_photo
    payload = {
        'chat_id': chat_id,
        'photo': f"https://botesspa.ru/{url_photo}",
        'caption': "BotEsspa"
    }
    r = requests.post(url, json=payload)
    return r


def get_location(chat_id):
    global_path = f'/home/s/semyon2b/botesspa/public_html/{chat_id}'
    all_path = os.listdir(global_path)
    for i in all_path:
        if 'latitude' in i:
            return eval(i)
    return 0, 0


def tel_parse_message(msg):
    chat_id = msg['message']['chat']['id']
    if 'photo' in msg['message']:
        file_id = msg['message']['photo'][2]['file_id']
        txt = 0
        location = 0
    elif 'text' in msg['message']:
        txt = msg['message']['text']
        file_id = 0
        location = 0
    else:
        location = msg['message']['location']
        file_id = 0
        txt = 0
    return chat_id, txt, file_id, location


def tel_send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    r = requests.post(url, json=payload)
    return r


def tel_inlineurl_start(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': "Здравствуйте, давайте познакомимся!👋 \n Меня зовут Your Designer Bot, и со мной у вас больше не будет возникать вопросов, что бы надеть сегодня. Я буду вашим личным ассистентом по подбору одежды, исходя только из вашего гардероба.💁‍♀️ \n Все, что вам будет нужно сделать, это только прислать мне фотографии вашей одежды, выбрать город и время отправки сообщения, а дальше всю работу сделаю я! \n При составлении вашего наряда на сегодня я буду учитывать погоду в вашем городе, и, конечно, грамотно сочетать цвета для самого удачного образа.💗 \n Давайте начнем!",
        'reply_markup': {
            "keyboard":
                [[{"text": "Подробнее обо мне🙌"}],
                 [{"request_location": True, "text": "Поделиться геопозицией📍"}]]}}
    r = requests.post(url, json=payload)
    return r


def tel_inlineurl_look(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': "Теперь я готов принять фотографии вашей одежды, присылайте по одной фотографии.️",
        'reply_markup': {
            "keyboard":
                [[{"text": "Я отправил все фотографии."}],
                 [{"text": "В главное меню📱"}]]}}
    r = requests.post(url, json=payload)
    return r


def tel_inlineurl_final_look(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': "Отлично! Теперь я готов прислать вам ваш идеальный образ по погоде на сегодня☺️️",
        'reply_markup': {
            "keyboard":
                [[{"text": "Отправь готовый образ👕"}],
                 [{"text": "В главное меню📱"}]]}}
    r = requests.post(url, json=payload)
    return r


def tel_inlineurl_back_to_menu(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': "Вы вернулись в главное меню️",
        'reply_markup': {
            "keyboard":
                [[{"text": "Подробнее обо мне🙌"}],
                 [{"request_location": True, "text": "Поделиться геопозицией📍"}]]}}
    r = requests.post(url, json=payload)
    return r


def tel_send_button(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

    payload = {
        'chat_id': chat_id,
        'text': "Пожалуйста, выберите время, в которое вы бы хотели получать готовый образ:",
        'reply_markup': {
            "keyboard": [[{'text': '6:00'}, {'text': '7:00'}],
                         [{'text': '8:00'}, {'text': '9:00'}],
                         [{'text': '10:00'}, {'text': '11:00'}], [{'text': '12:00'}]]}}
    r = requests.post(url, json=payload)
    return r


def tel_send_inlinebutton(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

    payload = {
        'chat_id': chat_id,
        'text': "What is this?",
        'reply_markup': {
            "inline_keyboard": [[
                {
                    "text": "A",
                    "callback_data": "ic_A"
                },
                {
                    "text": "B",
                    "callback_data": "ic_B"
                }]
            ]
        }
    }
    r = requests.post(url, json=payload)
    return r


def tel_upload_file(file_id):
    url = f'https://api.telegram.org/bot{TOKEN}/getFile?file_id={file_id}'
    a = requests.post(url)
    json_resp = json.loads(a.content)
    file_pathh = json_resp['result']['file_path']

    url_1 = f'https://api.telegram.org/file/bot{TOKEN}/{file_pathh}'
    b = requests.get(url_1)
    file_content = b.content
    with open(f'/home/s/semyon2b/botesspa/public_html/{file_pathh}', "wb") as f:
        f.write(file_content)
        return f'https://botesspa.ru/{file_pathh}'


def search_image_by_url(image_url):
    url = "https://yandex.com/images/search"
    payload = {
        'source': 'collections',
        'rpt': 'imageview',
        'url': image_url
    }
    response = requests.get(url, params=payload)
    html = BS(response.content, 'html.parser')
    for el in html.select('.CbirSection > .Tags > .Tags-Wrapper > .Button2 > .Button2-Text'):
        return el.text


def yandex_weather(location):
    latitude = location['latitude']
    longitude = location['longitude']
    url_yandex = f'https://api.weather.yandex.ru/v2/informers/?lat={latitude}&lon={longitude}&[lang=ru_RU]'
    resp = requests.get(url_yandex, headers={'X-Yandex-API-Key': "cd6b7193-b438-4b24-9d25-15f8a2a86c17"}, verify=False)
    html = resp.json()
    return html.get('fact').get('feels_like')


def make_user(chat_id, location):
    if not os.path.isdir(f"/home/s/semyon2b/botesspa/public_html/{chat_id}/{location}"):
        os.makedirs(f"/home/s/semyon2b/botesspa/public_html/{chat_id}/{location}")
        os.makedirs(f'/home/s/semyon2b/botesspa/public_html/{chat_id}/warm/up')
        os.makedirs(f'/home/s/semyon2b/botesspa/public_html/{chat_id}/warm/down')
        os.makedirs(f'/home/s/semyon2b/botesspa/public_html/{chat_id}/cold/up')
        os.makedirs(f'/home/s/semyon2b/botesspa/public_html/{chat_id}/cold/down')


@app.route('/python-bot/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        try:
            chat_id, txt, file_id, location = tel_parse_message(msg)
            if txt != 0:
                if txt == '/start':
                    tel_inlineurl_start(chat_id)
                    tel_send_message(chat_id,
                                     'Пожалуйста, для начала поделитесь со мной вашей геопозицией, чтобы я мог узнать погоду в вашем городе😉')
                elif txt == 'Загрузить фотографии одежды👚':
                    tel_send_message(chat_id,
                                     'Мы готовы принять фотографии вашей одежды, присылайте по одной фотографии')
                    tel_inlineurl_look(chat_id)
                elif txt == "В главное меню📱":
                    tel_inlineurl_back_to_menu(chat_id)
                elif txt == "Я отправил все фотографии.":
                    tel_inlineurl_final_look(chat_id)
                elif txt == 'Отправь готовый образ👕':
                    location = get_location(chat_id)
                    weather = yandex_weather(location)
                    url_photo_up = dress_up_photo_maker(chat_id, weather)
                    url_photo_down = dress_down_photo_maker(chat_id, weather)
                    tel_send_photos(chat_id, url_photo_up)
                    tel_send_photos(chat_id, url_photo_down)
                else:
                    tel_send_message(chat_id, 'Я вас не понимаю :(')
            elif file_id != 0:
                url_to_photo = tel_upload_file(file_id)
                on_photo = search_image_by_url(url_to_photo)
                tel_send_message(chat_id, on_photo)
            else:
                make_user(chat_id, location)
                weather = yandex_weather(location)
                tel_send_message(chat_id, f"Погода в вашем городе сейчас ощущается как {weather}°C☀️")
                tel_inlineurl_look(chat_id)
        except:
            print("from index-->")
        return Response('ok', status=200)
    else:
        return '<h1>Это страница-webhook для бота на Python, размещенного на хостинге Beget.</h1>'


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template('home.html')


if __name__ == '__main__':
    app.run(threaded=True)