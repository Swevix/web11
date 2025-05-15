from django.contrib import admin, messages
from django.contrib.admin import SimpleListFilter
from django.utils.html import mark_safe
from django.db.models import ExpressionWrapper, F, DecimalField

from .models import Car, Manufacturer, CarDetail, Tag


# Пользовательское вычисляемое поле: краткая информация (п.7)
@admin.display(description="Краткая информация")
def brief_info(obj):
    return f"Описание: {len(obj.description)} символов" if obj.description else "Нет описания"


# Пользовательское вычисляемое поле: цена с налогом (п.7)
@admin.display(description="Цена с налогом")
def price_with_tax(obj):
    if obj.price is not None:
        return f"${round(float(obj.price) * 1.2, 2)}"
    return "$0.00"


# Кастомный фильтр для статуса публикации (п.9)
class PublishedFilter(SimpleListFilter):
    title = "Статус публикации"
    parameter_name = "pub_status"

    def lookups(self, request, model_admin):
        return [
            ("published", "Опубликовано"),
            ("draft", "Черновик"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "published":
            return queryset.filter(is_published=Car.Status.PUBLISHED)
        elif self.value() == "draft":
            return queryset.filter(is_published=Car.Status.DRAFT)
        return queryset


# Дополнительный кастомный фильтр по диапазону цены (п.9)
class PriceRangeFilter(SimpleListFilter):
    title = "Диапазон цены"
    parameter_name = "price_range"

    def lookups(self, request, model_admin):
        return [
            ('low', 'Низкая цена (<20000)'),
            ('medium', 'Средняя цена (20000-50000)'),
            ('high', 'Высокая цена (>50000)'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'low':
            return queryset.filter(price__lt=20000)
        elif self.value() == 'medium':
            return queryset.filter(price__gte=20000, price__lte=50000)
        elif self.value() == 'high':
            return queryset.filter(price__gt=50000)
        return queryset


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    # Поля для формы добавления/редактирования
    fields = [
        'title', 'slug', 'description', 'price',
        'manufacturer', 'tags', 'image', 'image_preview'
    ]
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ['time_create', 'time_update', 'image_preview']

    # Список записей
    list_display = (
        'id', 'title', 'manufacturer', 'time_create',
        'is_published', brief_info, price_with_tax,
    )
    list_display_links = ('id', 'title')
    list_editable = ('is_published',)
    ordering = ['-time_create', 'title']
    list_per_page = 5
    search_fields = ['title', 'manufacturer__name']
    list_filter = [PublishedFilter, 'manufacturer', PriceRangeFilter]
    actions = ['set_published', 'set_draft']

    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Car.Status.PUBLISHED)
        self.message_user(request, f"Статус 'Опубликовано' обновлён для {count} записей.", messages.SUCCESS)

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Car.Status.DRAFT)
        self.message_user(request, f"{count} записей сняты с публикации.", messages.WARNING)

    @admin.display(description='Превью изображения')
    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' style='max-height:200px;' />")
        return "(нет изображения)"


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'country')


@admin.register(CarDetail)
class CarDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'car', 'engine', 'transmission', 'mileage')
    list_display_links = ('id', 'car')
    search_fields = ('car__title', 'engine', 'transmission')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
