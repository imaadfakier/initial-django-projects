from django.shortcuts import render
from django.utils import timezone
from .models import Todo
from django.http import HttpResponseRedirect

def add_to_do_list_item(request):
    # print(request)
    # print(request.POST)
    # print(request.POST.get('content'))

    content = request.POST['content']
    # print(content)
    added_date = timezone.now()
    # print(added_date)

    to_do_list_item = Todo.objects.create(text=content, added_date=added_date)
    # print(to_do_list_item)
    # print(to_do_list_item.id)
    total_to_do_list_objects = Todo.objects.all().count()
    # print(total_to_do_list_objects)

    # return render(request, 'to_do_list/index.html')
    return HttpResponseRedirect('/to_do_list')

def delete_to_do_list_item(request, to_do_list_item_id):
    # print(to_do_list_item_id)
    Todo.objects.get(id=to_do_list_item_id).delete()
    return HttpResponseRedirect('/to_do_list')
