from django.urls import path
from . import views

app_name = 'cms'
urlpatterns = [
    # schedule views
    path('schedule/new', views.schedule_new, name='schedule_new'),
    path('schedule/edit/<int:schedule_id>', views.schedule_edit, name='schedule_edit'),
    path('schedule/delete/<int:schedule_id>', views.schedule_delete, name='schedule_delete'),
    path('schedule/<str:company_id>', views.schedule_index, name='schedule_index'),

    # content views
    path('content/new', views.content_new, name='content_new'),
    path('content/edit/<int:content_id>', views.content_edit, name='content_edit'),
    path('content/delete/<int:content_id>', views.content_delete, name='content_delete'),
    path('content/<str:company_id>', views.content_index, name='content_index'),

    path('media', views.MediaCreateView.as_view(), name='media_index'),

    # json views
    path('schedule.json', views.schedule_json, name='schedule_json'),
    path('content.json', views.content_json, name='content_json'),
]