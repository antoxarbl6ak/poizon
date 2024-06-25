import asyncio
from aiogram import Dispatcher
from true_handlers import admin, router, bot, BotCommand, BotCommandScopeChat, BotCommandScopeDefault

dp = Dispatcher()


async def set_menu():
    user_commands = [BotCommand(command="/start", description="старт")]
    admin_commands = user_commands + [BotCommand(command="/admin", description="админ панель")]
    await bot.set_my_commands(commands=user_commands, scope=BotCommandScopeDefault())
    await bot.set_my_commands(commands=admin_commands, scope=BotCommandScopeChat(chat_id=admin))


async def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    dp.startup.register(set_menu)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
