# from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from profiles.models import Profile
from django.http import JsonResponse
from .utils import get_report_image
from .models import Report
from .forms import ReportForm
from django.views.generic import ListView, DetailView
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

# M - model
# V - view                ... frameworks such as Flask, Django etc.
# T - template

# vs

# M - model
# V - view                ... frameworks such as ?
# C - controller

@login_required
def create_report_view(request):
    form = ReportForm(request.POST or None)
    if request.is_ajax():
        # name = request.POST.get('name')
        image = request.POST.get('image')

        img = get_report_image(image)

        # remarks = request.POST.get('remarks')
        author = Profile.objects.get(user=request.user)

        # Report.objects.create(name=name, image=img, remarks=remarks, author=author)
        if form.is_valid:
            # form.save()
            instance = form.save(commit=False)
            instance.image = img
            instance.author = author
            instance.save()

        return JsonResponse({'msg':'send'})
    return JsonResponse({})

# class ReportListView(ListView):
class ReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name = 'reports/main.html'

# class ReportDetailView(DetailView):
class ReportDetailView(LoginRequiredMixin, DetailView):
    model = Report
    template_name = 'reports/detail.html'

# def render_pdf_view(request):
# def render_pdf_view(request, pk):
@login_required
def render_pdf_view(request, pk):
    # template_path = 'user_printer.html'
    template_path = 'reports/pdf.html'

    # obj = Report.object.get(id=pk)
    # obj = Report.object.get(pk=pk)
    obj = get_object_or_404(Report, pk=pk)

    # context = {'myvar': 'this is your template context'}
    # context = {'hello': 'hello world from pdf'}
    context = {'obj': obj}

    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # if download:
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # if display in browser:
    response['Content-Disposition'] = 'filename="report.pdf"'


    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)


    # create a pdf
    # pisa_status = pisa.CreatePDF(
    #    html, dest=response, link_callback=link_callback
    # )
    pisa_status = pisa.CreatePDF(
       html, dest=response
    )

    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response