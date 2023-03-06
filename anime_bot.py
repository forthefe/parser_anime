from aiogram import types, executor, Dispatcher, Bot
from bs4 import BeautifulSoup
import requests
import asyncio
from keyboards import main_search
from dotenv import dotenv_values


config = dotenv_values('.env')
bot = Bot(config['tokens'])
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.message):
    await message.answer(f'привет, {message.from_user.full_name} я бот по поиску аниме')
    await asyncio.sleep(3)
    await message.answer('нажми на кнопку поиск и я найду тебе аниме ', reply_markup=main_search)


@dp.message_handler(text='Поиск 🔥🔎')
async def start(message: types.message):
    url = "https://yummyanime.tv/movies"
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    page_count = int(soup.find('div', class_='pagination__inner').find_all('a')[-1].text.strip())
    for i in range(1, page_count + 1):
        print(f'[INFO] Обработка {i} страницы')
        url = f'https://yummyanime.tv/movies/page/{i}/'
        req = requests.get(url)
        soup = BeautifulSoup(req.text, 'html.parser')

        menu = soup.select('.section > .section__content > .movie-item')
        for item in menu:
            title = item.select('.movie-item > .movie-item__inner > .movie-item__link > .movie-item__title')[
                0].text.strip()
            year = item.select('.movie-item__meta')[0].text.replace('(', '').replace(')', '')
            rating = item.select('.movie-item__rating')[0].text.strip()
            link_img = item.select('.movie-item__link > .movie-item__img > img')
            for i in link_img:
                start = 'https://yummyanime.tv'
                links = start + i['src']
            link_all = item.select('.movie-item__link')
            for i in link_all:
                all = 'https://yummyanime.tv'
                link_all = all + i['href']
            await asyncio.sleep(3)
            await bot.send_photo(message.chat.id, links,
            caption="<b>" + 'Название: '+ title.strip() + "</b>\n<i>" + 'Год випуска: ' + year.strip() + '\nРейтинг: ' + rating.strip() + f"</i>\n<a href='{link_all}'>Ссылка на сайт</a>",
            parse_mode='html')


executor.start_polling(dp)