import asyncio
import logging
import openai
import os

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from logic import check_sub
from buttons import start_keyboard

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
router = Router()
bot = Bot(TOKEN)
openai.api_key = os.getenv('OPENAI_API_KEY')


@router.message(Command(commands=["start"]))
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, {message.from_user.full_name}! Бот Чиби предоставит доступ к ChatGPT. Но "
                         f"перед этим подпишитесь на канал\n@xdev_v", reply_markup=start_keyboard.as_markup())


@router.message()
async def msg_gpt(message: types.Message) -> None:
    isSubscribe = await check_sub(message, bot)

    if not isSubscribe:
        await message.answer('Вы не подписаны на канал 😔\n@xdev_v', reply_markup=start_keyboard.as_markup())
    else:
        await message.answer('Ем печеньки, готовлю ответ 🍪')
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": message.text}
            ]
        )
        print(isSubscribe)
        await message.answer(completion.choices[0].message.content)


@router.callback_query(lambda c: c.data.startswith('check_subscribe'))
async def check_s(callback: CallbackQuery):
    isSubscribe = await check_sub(callback.message, bot)
    if not isSubscribe:
        await callback.message.answer('Ты не подписался на канал 😔\n@xdev_v', reply_markup=start_keyboard.as_markup())
    else:
        await callback.message.answer('Отправь сообщение, чтобы начать переписку')


async def main() -> None:
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())