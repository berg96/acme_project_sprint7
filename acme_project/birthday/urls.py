from django.urls import path

from . import views

app_name = 'birthday'

urlpatterns = [
    path('', views.BirthdayCreateView.as_view(), name='create'),
    path('list/', views.birthday_list, name='list'),
    path('<int:pk>/edit/', views.BirthdayUpdateView.as_view(), name='edit'),
    path(
        '<int:pk>/delete/', views.BirthdayDeleteView.as_view(), name='delete'
    ),
]
