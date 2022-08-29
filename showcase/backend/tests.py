from django.test import TestCase
from setupDjangoORM import VK_API_TOKEN, ID_PUBLIC
from bot_server import BotServer


class TestBotServer(TestCase):
    """Тестируем BotServer."""

    @classmethod
    def setUpClass(cls):
        """Вызывается однажды перед запуском всех тестов класса."""
        cls.server = BotServer(
            VK_API_TOKEN,
            ID_PUBLIC,
            "test_server"
        )

    def test_something(self):
        act = 1
        self.assertEqual(act, 1, 'Метод act не работает')
