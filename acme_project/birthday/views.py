from django.shortcuts import render

from .forms import BirthdayForm


def birthday(request):
    if request.GET:
        form = BirthdayForm(request.GET)
        if form.is_valid():
            pass
    else:
        form = BirthdayForm()
    context = {'form': form}
    return render(request, 'birthday/birthday.html', context)
