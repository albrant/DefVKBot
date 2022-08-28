from django.contrib import admin
from .models import Product, Section
from django.utils.safestring import mark_safe


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'section', 'price', 'quantity')
    empty_value_display = '-пусто-'
    readonly_fields = ('preview',)
    list_filter = ('section',)
    fields = ('name', 'description', 'section',
              'image', 'price', 'quantity', 'preview')

    def preview(self, obj):
        """функция, действующая как вычислимое поле записи:
        Отображает в админке картинку из поля image.
        По масштабу картинка уменьшится до 200 пикселей в высоту.
        """
        return mark_safe(
            f'<img src="{obj.image.url}" style="max-height: 200px;">'
        )
    preview.short_description = mark_safe('<b>Картинка</b>')


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    empty_value_display = '-пусто-'
