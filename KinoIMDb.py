import requests
from bs4 import BeautifulSoup as bs
from telebot import TeleBot
#   Передача API в бот
bot = TeleBot('5148516163:AAGLVl5ljJZgtZy4XPRe6cXOXs6UO9Z-wRE')
#   Получение кода страницы и обработка для получения ссылки на другую страницу
def get_href(m):
    req = requests.get(f'https://www.imdb.com/find?q={m}')
    soup = bs(req.text, features='html.parser')
    href = soup.find('td', class_='result_text').a.get('href')
    return href
#   Получение кода страницы и обработка кода с целью извлечения имени и рейтинга фильма
def get_nr(m):
    req2 = requests.get(f'https://imdb.com{get_href(m)}?ref_=fn_al_tt_1')
    soup1 = bs(req2.text, features='html.parser')
    name = soup1.find('h1', class_='sc-b73cd867-0 eKrKux').text
    raiting = soup1.find('span', class_='sc-7ab21ed2-1 jGRxWM').text
    return name, raiting
#   Обработчик команды start
@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, 'Введите название фильма, а я вам скажу его рейтинг')
#   Обработчик текстовых комманд
@bot.message_handler(content_types=['text'])
def textm(m):
    mes = m.text
    get_href(mes)
    bot.send_message(m.chat.id, f'Фильм: {get_nr(mes)[0]}\nРейтинг: {get_nr(mes)[1]}')
#   Запуск бота
bot.polling(none_stop=True, interval=0)
