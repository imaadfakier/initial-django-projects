from django.shortcuts import render
from .models import Todo

# Create your views here.
def index(request):
    all_to_do_items = Todo.objects.all().order_by('added_date')
    # all_to_do_items = Todo.objects.all().order_by('-added_date')
    context = {'all_to_do_items': all_to_do_items}
    return render(request, 'to_do_list/index.html', context)
