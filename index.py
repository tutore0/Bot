from aiogram import Bot ,Dispatcher ,types ,executor
import logging
from pytube import YouTube
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

bot = Bot(token='6097058363:AAEDzaO_d9IB3ezgznbW8D1uOGj3kdrERCI')
storage = MemoryStorage()
dp = Dispatcher(bot , storage=MemoryStorage())

@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer(f'Здравствуйте {message.from_user.full_name}!\nВведите команду /help - чтобы узнать возможности бота')

@dp.message_handler(commands='help')
async def help(message: types.Message):
    await message.answer(f'Команды:\n/start\n/help - информация о боту\n/audio - конвертировать видео с ютуба  в аудио формате mp3')

class Download(StatesGroup):
   download = State()

def download_video(url, type='audio'):
   yt = YouTube(url)
   if type == 'audio':
      yt.streams.filter(only_audio=True).first().download('audio', f'{yt.title}.mp3')
      return f'{yt.title}.mp3'

@dp.message_handler(commands='audio')
async def start(message: types.Message):
    await message.answer(f'Отправьте ссылку на видео в ютубе и я вам отправлю его в mp3 формате')
    await Download.download.set()

@dp.message_handler(state= Download.download)
async def download(message: types.Message, state:FSMContext):
   title = download_video(message.text)
   audio = open(f'audio/{title}', 'rb')
   await message.answer('Все скачалось')
   try:
      await bot.send_audio(message.chat.id, audio)
   except:
      await message.answer('Произашло ошибка попробуйте еще раз')
   await state.finish()

if __name__ == '__main__':
   executor.start_polling(dp)