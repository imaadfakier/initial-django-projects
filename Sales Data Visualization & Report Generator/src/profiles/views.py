from django.shortcuts import render
from .models import Profile
from .forms import ProfileForm

from django.contrib.auth.decorators import login_required

# Create your views here.
# def my_profile_view(request):
@login_required
def my_profile_view(request):
    # context = {}
    # return render(request, 'profiles/main.html', context)
    profile = Profile.objects.get(user=request.user)
    # form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
    # form = ProfileForm(request.POST or None, request.FILES or None)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
    confirm = False
    if form.is_valid():
        form.save()
        confirm = True
    context = {
        'profile':profile,
        'form':form,
        'confirm':confirm,
    }
    return render(request, 'profiles/main.html', context)