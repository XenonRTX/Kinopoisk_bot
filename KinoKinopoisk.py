import requests
from bs4 import BeautifulSoup as bs
from telebot import TeleBot
#   Передача API в бот
bot = TeleBot('5028709860:AAHPyoHKAbC-Vjei7fPPVxfen1RLDEfbuds')
#---------------- Парсерная часть ----------------
#   Функция получения кода страницы + обработка страницы
def parser(m):
    req = requests.get(f'https://www.kinopoisk.ru/index.php?kp_query={m}')
    soup = bs(req.text, features="html.parser")
    return soup
#   Функция получения необходимых элементов с имеющегося кода страницы
def get_nr(m):
    name = parser(m).find('p', class_='name').text
    raiting = parser(m).find('div', class_='rating').text
    return name, raiting
#---------------- Конец парсерной части ----------
#   Обработчик команды /start для Телеграмм-бота
@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, 'Введи название фильма, а я скажу его рейтинг')
#   Обработчик текстовых сообщений получаемых ботом
@bot.message_handler(content_types=['text'])
def text(m):
    #   Обработчик исключений для предотвращения возникновения ошибок, прерывающих работу программы
    try:
        #   Получение аргумента для функции из сообщения пользователя
        mes = m.text
        #   Передача аргумента в функцию и точка старта работы "парсерной части сайта"
        parser(mes)
        bot.send_message(m.chat.id, f'Фильм: {get_nr(mes)[0]}\nРейтинг фильма: {get_nr(mes)[1]}')
    except:
        bot.send_message(m.chat.id, 'Фильм не найден, введите другое название')
#       Запуск бота
bot.polling(interval=0)
