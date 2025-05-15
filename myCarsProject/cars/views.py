from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView, ListView, DetailView,
    FormView, CreateView, UpdateView, DeleteView
)
from .models import Car, Tag
from .forms import CarForm, CarModelForm, UploadForm
from .utils import DataMixin


class HomeView(DataMixin, ListView):
    model = Car
    template_name = 'cars/index.html'
    context_object_name = 'cars'
    paginate_by = 5
    queryset = Car.published.all()
    title = 'Главная'




class AboutView(DataMixin, TemplateView):
    template_name = 'cars/about.html'
    title = 'О сайте'


class CarDetailView(DataMixin, DetailView):
    model = Car
    template_name = 'cars/car_detail.html'
    context_object_name = 'car'
    slug_field = 'slug'
    slug_url_kwarg = 'car_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Заголовок страницы — название автомобиля
        context['title'] = context['car'].title
        return context


class AddCarCustomView(DataMixin, FormView):
    form_class = CarForm
    template_name = 'cars/add_car_custom.html'
    success_url = reverse_lazy('cars:home')
    title = 'Добавить (Form)'

    def form_valid(self, form):
        cd = form.cleaned_data
        car = Car.objects.create(
            title=cd['title'],
            slug=cd['title'].lower().replace(' ', '-'),
            description=cd['description'],
            price=cd['price'],
            is_published=Car.Status.DRAFT
        )
        image = cd.get('image')
        if image:
            car.image = image
            car.save()
        return super().form_valid(form)


class CarCreateView(DataMixin, CreateView):
    model = Car
    form_class = CarModelForm
    template_name = 'cars/add_car_model.html'
    success_url = reverse_lazy('cars:home')
    title = 'Добавить (ModelForm)'


class CarUpdateView(DataMixin, UpdateView):
    model = Car
    form_class = CarModelForm
    template_name = 'cars/add_car_model.html'
    success_url = reverse_lazy('cars:home')
    slug_field = 'slug'
    slug_url_kwarg = 'car_slug'
    title = 'Редактировать автомобиль'


class CarDeleteView(DataMixin, DeleteView):
    model = Car
    template_name = 'cars/car_confirm_delete.html'
    success_url = reverse_lazy('cars:home')
    slug_field = 'slug'
    slug_url_kwarg = 'car_slug'
    title = 'Удалить автомобиль'


class UploadFileView(DataMixin, FormView):
    form_class = UploadForm
    template_name = 'cars/upload.html'
    success_url = reverse_lazy('cars:upload_file')
    title = 'Загрузка файла'

    def form_valid(self, form):
        # Сохраняем файл внутри формы (метод реализовать в UploadForm)
        form.save_file()
        return super().form_valid(form)
