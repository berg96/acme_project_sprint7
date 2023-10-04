from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import BirthdayForm, CongratulationForm
from .models import Birthday, Congratulation
from .utils import calculate_birthday_countdown


DATEDIFF = '(strftime("%j","birthday") - strftime("%j","now") + 365) % 365'


class BirthdayListView(ListView):
    model = Birthday
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.extra(select={'datediff': DATEDIFF}).order_by('datediff')


class BirthdayCreateView(LoginRequiredMixin, CreateView):
    model = Birthday
    form_class = BirthdayForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BirthdayUpdateView(LoginRequiredMixin, UpdateView):
    model = Birthday
    form_class = BirthdayForm

    def dispatch(self, request, *args, **kwargs):
        # Получаем объект по первичному ключу и автору или вызываем 404 ошибку.
        get_object_or_404(Birthday, pk=kwargs['pk'], author=request.user)
        # Если объект был найден, то вызываем родительский метод,
        # чтобы работа CBV продолжилась.
        return super().dispatch(request, *args, **kwargs)


class BirthdayDeleteView(LoginRequiredMixin, DeleteView):
    model = Birthday
    success_url = reverse_lazy('birthday:list')

    def dispatch(self, request, *args, **kwargs):
        # Получаем объект по первичному ключу и автору или вызываем 404 ошибку.
        get_object_or_404(Birthday, pk=kwargs['pk'], author=request.user)
        # Если объект был найден, то вызываем родительский метод,
        # чтобы работа CBV продолжилась.
        return super().dispatch(request, *args, **kwargs)


class BirthdayDetailView(DetailView):
    model = Birthday

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['birthday_countdown'] = calculate_birthday_countdown(
            self.object.birthday
        )
        # Записываем в переменную form пустой объект формы.
        context['form'] = CongratulationForm()
        # Запрашиваем все поздравления для выбранного дня рождения.
        context['congratulations'] = (
            # Дополнительно подгружаем авторов комментариев,
            # чтобы избежать множества запросов к БД.
            self.object.congratulations.select_related('author')
        )
        return context


class CongratulationCreateView(LoginRequiredMixin, CreateView):
    model = Congratulation
    form_class = CongratulationForm
    birthday = None

    def dispatch(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        self.birthday = get_object_or_404(Birthday, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.author = self.request.user
        form.instance.birthday = self.birthday
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse('birthday:detail', kwargs={'pk': self.birthday.pk})
