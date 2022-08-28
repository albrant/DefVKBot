import vk_api.vk_api
from vk_api import VkUpload
from vk_api.keyboard import VkKeyboard
from random import randint
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from config import my_vk_id
from backend.models import Section, Product


class BotServer:

    def __init__(self, api_token, group_id, server_name: str = "Empty"):
        # Даем серверу имя
        self.server_name = server_name
        # Для Long Poll
        self.vk = vk_api.VkApi(token=api_token)
        # Для использования Long Poll API
        self.long_poll = VkBotLongPoll(self.vk, group_id)
        # Для вызова методов vk_api
        self.vk_api = self.vk.get_api()

    def send_message(self, user_id, message, keyboard=None, attachment=None):
        """Функция отправки сообщения через метод method.
        Можно добавить клавиатуру к сообщению"""
        post = {
            'user_id': user_id,
            'message': message,
            'random_id': randint(10, 2048),
        }
        if attachment is not None:
            post['attachment'] = attachment
        if keyboard is not None:
            post['keyboard'] = keyboard
        self.vk.method('messages.send', post)

    def test(self):
        # Посылаем сообщение пользователю с указанным ID
        keyboard = VkKeyboard()
        keyboard.add_button('Тестовая кнопка')
        self.send_message(
            my_vk_id,
            "Привет-привет! Проверка связи",
            keyboard=keyboard,
            attachment='photo135336811_457243834')

    def start(self):
        """Функция основной работы бота. Слушаем эфир, реагируем"""
        for event in self.long_poll.listen():
            # Пришло новое сообщение
            if event.type == VkBotEventType.MESSAGE_NEW:
                message = event.object['message']
                from_id = message['from_id']
                peer_id = message['peer_id']
                message_text = message['text']
                username = self.get_user_name(from_id)
                error_message = f'{username}, нет такой команды (продукта или раздела)!'
                if message_text.lower() in ('start', 'начать',
                                            'витрина', 'разделы'):
                    self.send_message(
                        from_id,
                        message='Выберите раздел кондитерской',
                        keyboard=self.get_sections_keyboard())
                elif message_text.lower() in ('test', 'тест',
                                              'проверка', 'проверка связи'):
                    # вызов для проверки работоспособности отправки сообщений,
                    # содержащих картинку и клавиатуру из одной кнопки
                    self.test()
                else:
                    # пробуем найти продукты
                    products_keyboard = self.get_products_keyboard(message_text)
                    if products_keyboard is not None:
                        self.send_message(
                            peer_id,
                            f'Выбери продукт из раздела {message_text}',
                            keyboard=products_keyboard
                        )
                    else:
                        product = self.get_product(message_text)
                        if product:
                            message = (product.name + '\n' +
                                       product.description + '\n' +
                                       f'{product.price} рублей')
                            upload = VkUpload(self.vk)
                            photo = upload.photo_messages('/media/'+product.image)
                            owner_id = photo[0]['owner_id']
                            photo_id = photo[0]['id']
                            access_key = photo[0]['access_key']
                            image = f'photo{owner_id}_{photo_id}_{access_key}'
                        else:
                            message = error_message
                            image = None
                        self.send_message(peer_id, message, attachment=image)

    def get_user_name(self, user_id):
        """Функция получения имени пользователя"""
        return self.vk_api.users.get(user_id=user_id)[0]['first_name']

    def get_product(self, product_name):
        """Функция получения продукта из БД"""
        product = Product.objects.filter(name=product_name)
        return product[0] if product else None

    def get_sections_keyboard(self):
        """Функция формирования клавиатуры из списка разделов кондитерской"""
        keyboard = VkKeyboard()
        sections = Section.objects.all()
        i = 0
        for section in sections:
            keyboard.add_button(str(section))
            i += 1
            if i % 2 == 0:
                keyboard.add_line()
        return keyboard.get_keyboard()

    def get_products_keyboard(self, section):
        """Функция формирования клавиатуры из списка продуктов"""
        keyboard = VkKeyboard()
        products = Product.objects.filter(section__name=section)
        i = 0
        for product in products:
            keyboard.add_button(str(product))
            i += 1
            if i % 2 == 0:
                keyboard.add_line()
        if i > 0:
            keyboard.add_button('разделы')
        # вернём либо None (если по данному разделу ничего нет),
        # либо список продуктов данного раздела
        return keyboard.get_keyboard() if i > 0 else None
