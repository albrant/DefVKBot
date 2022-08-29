import math
from random import randint
from typing import Any

import vk_api.vk_api
from vk_api import VkUpload
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
from vk_api.keyboard import VkKeyboard

from backend.models import Product, Section
from setupDjangoORM import KEYBOARD_ROWS, MEDIA_ROOT


class BotServer:
    """Класс для реализации функционала бота для группы VK.
    Главный метод - start для запуска сервера.
    """
    def __init__(self, api_token, group_id, server_name: str = "Server"):
        # Даем серверу имя
        self.server_name = server_name
        # Для Long Poll
        self.vk = vk_api.VkApi(token=api_token)
        # Для использования Long Poll API
        self.long_poll = VkBotLongPoll(self.vk, group_id)
        # Для вызова методов vk_api
        self.vk_api = self.vk.get_api()

    def send_message(self, user_id: int, message: str,
                     keyboard=None, attachment=None) -> None:
        """Функция отправки сообщения через метод method.
        Можно добавить сообщению картинку и клавиатуру (кнопки)."""
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
                error_message = f'{username}, нет такого продукта или раздела'

                if message_text.lower() in ('start', 'начать',
                                            'витрина', 'разделы'):
                    self.send_message(
                        from_id,
                        message='Выберите раздел кондитерской',
                        keyboard=self.get_sections_keyboard())

                else:
                    # пробуем найти продукты в указанном разделе
                    products_keyboard = self.get_products_keyboard(
                        message_text
                    )
                    if products_keyboard is not None:
                        self.send_message(
                            peer_id,
                            f'Выберите продукт из раздела {message_text}',
                            keyboard=products_keyboard
                        )
                    else:
                        # пробуем найти информацию о выбранном продукте
                        product = self.get_product(message_text)
                        if product:
                            message = (product.name.capitalize() + '\n' +
                                       product.description + '\n' +
                                       f'Стоимость: {product.price} рублей')
                            upload = VkUpload(self.vk)
                            photo = upload.photo_messages(
                                MEDIA_ROOT + product.image.url
                            )
                            owner_id = photo[0]['owner_id']
                            photo_id = photo[0]['id']
                            access_key = photo[0]['access_key']
                            image = f'photo{owner_id}_{photo_id}_{access_key}'
                        else:
                            message = error_message
                            image = None
                        self.send_message(peer_id, message, attachment=image)

    def get_user_name(self, user_id: int) -> str:
        """Функция получения имени пользователя по его user_id"""
        return self.vk_api.users.get(user_id=user_id)[0]['first_name']

    def get_product(self, product_name: str) -> Any:
        """Функция получения продукта из БД по его имени (названию)"""
        product = Product.objects.filter(name=product_name)
        return product[0] if product else None

    def get_sections_keyboard(self) -> Any:
        """Функция формирования клавиатуры из списка разделов кондитерской."""
        keyboard = VkKeyboard()
        sections = Section.objects.all()  # считываем секции из БД через ORM
        # т.к. в ВК не может быть больше 10 рядов кнопок,
        # то нужно посчитать, по сколько кнопок будет в ряду
        columns = math.ceil(len(sections) / KEYBOARD_ROWS)
        if columns == 0:
            columns = 1
        i = 0
        # формируем клавиши в клавиатуре
        for section in sections:
            i += 1
            if i % columns == 0 and i > 1:
                keyboard.add_line()
            keyboard.add_button(str(section))
        return keyboard.get_keyboard()

    def get_products_keyboard(self, section: str) -> Any:
        """Функция формирования клавиатуры из списка продуктов."""
        keyboard = VkKeyboard()
        products = Product.objects.filter(section__name=section)
        columns = math.ceil(len(products) / KEYBOARD_ROWS)
        if columns == 0:
            columns = 1
        i = 0
        for product in products:
            i += 1
            if i % columns == 0 and i > 1:
                keyboard.add_line()
            keyboard.add_button(str(product))
        if i > 0:
            keyboard.add_line()
            keyboard.add_button('разделы')
        # вернём либо None (если по данному разделу ничего нет),
        # либо список продуктов данного раздела
        return keyboard.get_keyboard() if i > 0 else None
