# импортируем настройки Django ORM, чтобы можно было работать
# с базой данных без Django
import SetupDjangoORM
# Импортируем созданный нами класс Server
from bot_server import BotServer
# Получаем из config.py наш нузные переменные
from config import vk_api_token, id_public


server1 = BotServer(vk_api_token, id_public, "server1")
print('Запуск сервера бота')
server1.start()
