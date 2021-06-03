from django.urls import path
# from .views import create_report_view
# from .views import (
#     create_report_view,render,
#     ReportListView,
#     ReportDetailView
# )
from .views import (
    create_report_view,
    ReportListView,
    ReportDetailView,
    render_pdf_view
)

app_name = 'reports'

urlpatterns = [
    # path('save/', create_report_view, name='create-report'),
    path('home', ReportListView.as_view(), name='main'),
    path('<pk>', ReportDetailView.as_view(), name='detail'),
    path('save/', create_report_view, name='create-report'),
    # path('pdf/', render_pdf_view, name='pdf'),
    path('<pk>/pdf/', render_pdf_view, name='pdf'),
]