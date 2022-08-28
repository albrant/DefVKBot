from django.db import models


class Section(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Раздел витрины'
    )
    description = models.CharField(
        max_length=100,
        verbose_name='Описание раздела витрины'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'

    def __str__(self) -> str:
        return f'{self.name}'


class Product(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название товара'
    )
    description = models.TextField(
        max_length=500,
        verbose_name='Описание товара'
    )
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        verbose_name='Раздел товара',
        related_name='products'
    )
    image = models.ImageField(
        upload_to='products/images/',
        verbose_name='Изображение товара'
    )
    price = models.FloatField(
        default=0,
        verbose_name='Цена товара'
    )
    quantity = models.IntegerField(
        default=0,
        verbose_name='Количество на складе'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self) -> str:
        return f'{self.name}'
