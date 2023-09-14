import configparser
from aiogram import types, executor, Dispatcher, Bot
from bs4 import BeautifulSoup
import requests
import logging

class Lis_Bot:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.initialize_logging()
        bot_token = self.config['Telegram']['bot_token']
        self.bot = Bot(bot_token)
        self.dp = Dispatcher(self.bot)

    def initialize_logging(self):
        logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def run(self):
        @self.dp.message_handler(commands=['start'])
        async def start(message: types.Message):
            await self.bot.send_message(message.chat.id,
                """Բարև, ես քո <b>Telegram Bot</b> եմ,կոգնեմ գտնես տուն ՀՀ֊ում <b> <a href="//https://www.list.am/"> list.am </a></b> կայքում։ """,
                parse_mode="html", disable_web_page_preview=0)

        @self.dp.message_handler(content_types=['text'])
        async def parser(message: types.Message):
            url = "https://www.list.am/category?q=" + message.text
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
            }
            response = requests.get(url, headers=headers)

            soup = BeautifulSoup(response.text, "html.parser")
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                dl_elements = soup.find_all('div', class_='dl')
                for dl in dl_elements:
                    a_tags = dl.find_all('a')
                    for a in a_tags:
                        url = "www.list.am" + a.get("href")
                        await self.bot.send_message(message.chat.id, url, parse_mode="html")
                        self.logger.info(f"Sent message: {url}")

        self.logger.info("Bot started")
        executor.start_polling(self.dp)

if __name__ == '__main__':
    bot = Lis_Bot()
    bot.run()
