from django.shortcuts import render

from .forms import BirthdayForm


def birthday(request):
    form = BirthdayForm(request.GET or None)
    if form.is_valid():
        pass
    context = {'form': form}
    return render(request, 'birthday/birthday.html', context)
