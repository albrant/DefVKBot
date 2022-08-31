from django.test import TestCase

# from setupDjangoORM import VK_API_TOKEN
# import vk_api.vk_api
# import mock
from .models import Product, Section


class TestBotServer(TestCase):
    """Тестируем BotServer.

    def test_api_creation_error(self):
        self.assertRaises(
            ValueError,
            lambda: vk_api.VkApi(token=VK_API_TOKEN)
        )

    @mock.patch('vkontakte.api._API._get')
    def test_with_arguments(self, _get):
        _get.return_value = [{'last_name': u'Дуров'}]
        res = self.api.getProfiles(uids='1,2', fields='education')
        self.assertEqual(res, _get.return_value)
        _get.assert_called_once_with(
            'getProfiles',
            uids='1,2',
            fields='education'
        )

    @mock.patch('vkontakte.http.post')
    def test_urlencode_bug(self, post):
        post.return_value = 200, '{"response":123}'
        res = self.api.search(q=u'клен')
        self.assertEqual(res, 123)
    """
    pass


class TestModels(TestCase):
    """Тестируем работу моделей БД."""

    @classmethod
    def setUpClass(cls):
        """Создаём раздел и продукт в виртуальной БД"""
        super().setUpClass()
        # Создаём тестовую запись в БД
        # и сохраняем созданную запись в качестве переменной класса
        cls.section = Section.objects.create(
            name='Тестовый раздел',
            description='Тестовое описание'
        )
        cls.product = Product.objects.create(
            name='Тестовый продукт',
            description='тестовое описание',
            image='image',
            section=TestModels.section
        )

    def test_product_name(self):
        """Название продукта совпадает с ожидаемым."""
        product = TestModels.product
        product_name = product.name
        self.assertEqual(product_name, 'Тестовый продукт')

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        product = TestModels.product
        field_verboses = {
            'name': 'Название товара',
            'description': 'Описание товара',
            'section': 'Раздел товара',
            'image': 'Изображение товара',
            'price': 'Цена товара',
            'quantity': 'Количество на складе'
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    product._meta.get_field(field).verbose_name,
                    expected_value
                )

    def test_object_name_is_name_field(self):
        """__str__ product - это строчка с содержимым product.name"""
        product = TestModels.product
        expected_object_name = product.name
        self.assertEqual(expected_object_name, str(product))
