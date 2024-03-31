from aiogram import types


bot_commands = (
    # ('ozon', '(артикул)'),
    ('help', 'краткая информация о боте'),
    ('stats', 'pic count'),
    ('pics', 'go recognition')
)


commands_for_bot = []
for cmd in bot_commands:
    commands_for_bot.append(
        types.BotCommand(command=cmd[0], description=cmd[1])
    )
