from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)

from .forms import BirthdayForm
from .models import Birthday
from .utils import calculate_birthday_countdown


DATEDIFF = '(strftime("%j","birthday") - strftime("%j","now") + 365) % 365'


class BirthdayMixin:
    model = Birthday
    success_url = reverse_lazy('birthday:list')


class BirthdayListView(ListView):
    model = Birthday
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.extra(select={'datediff': DATEDIFF}).order_by('datediff')


class BirthdayCreateView(BirthdayMixin, CreateView):
    form_class = BirthdayForm


class BirthdayUpdateView(BirthdayMixin, UpdateView):
    form_class = BirthdayForm


class BirthdayDeleteView(BirthdayMixin, DeleteView):
    pass


class BirthdayDetailView(DetailView):
    model = Birthday

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['birthday_countdown'] = calculate_birthday_countdown(
            self.object.birthday
        )
        return context
