from aiogram import Bot
from aiogram.types import Message


async def check_sub(message: Message, bot: Bot) -> bool:
    channel_id = '@xdev_v'
    user_id = message.from_user.id

    try:
        chat_member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
        if chat_member.status == 'creator' or 'member':
            return True
        else:
            return False
    except Exception as e:
        await message.answer(f'Произошла ошибка: {str(e)}')