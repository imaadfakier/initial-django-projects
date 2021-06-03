from django.urls import path
from . import views
# from .forms import add_to_do_list_item
from . import forms

urlpatterns = [
    path('', views.index, name='index'),
    # path('add_todo/', add_to_do_list_item, name='add_to_do_list_item')
    path('add_todo/', forms.add_to_do_list_item, name='add_to_do_list_item'),
    path('delete_todo/<int:to_do_list_item_id>/', forms.delete_to_do_list_item, name='delete_to_do_list_item'),
]
