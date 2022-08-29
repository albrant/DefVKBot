import unittest
import setupDjangoORM
from bot_server import BotServer


class TestBotServer(unittest.TestCase):
    """Тестируем BotServer."""

    @classmethod
    def setUpClass(cls):
        """Вызывается однажды перед запуском всех тестов класса."""
        cls.server = BotServer(
            setupDjangoORM.VK_API_TOKEN,
            setupDjangoORM.ID_PUBLIC,
            "test_server"
        )

    def test_something(self):
        act = 1
        self.assertEqual(act, 1, 'Метод act не работает')


if __name__ == "__main__":
    unittest.main()
