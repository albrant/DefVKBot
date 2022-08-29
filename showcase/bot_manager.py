import setupDjangoORM
from bot_server import BotServer

# создаём и запускаем сервер бота
if __name__ == '__main__':
    server1 = BotServer(
        setupDjangoORM.VK_API_TOKEN,
        setupDjangoORM.ID_PUBLIC,
        "server1"
    )
    print('Запуск сервера бота')
    server1.start()
