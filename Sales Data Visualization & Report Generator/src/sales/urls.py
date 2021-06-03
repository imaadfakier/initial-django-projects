from django.urls import path
# from .views import home_view
# from .views import (
#     home_view,
#     SalesListView,
#     SaleDetailView,
# )
# from .views import (
#     home_view,
#     SalesListView,
#     SaleDetailView,
#     UploadTemplateView,
# )
from .views import (
    home_view,
    SalesListView,
    SaleDetailView,
    UploadTemplateView,
    csv_upload_view
)

app_name = 'sales'

urlpatterns = [
    path('home/', home_view, name='home'),
    # path('list/', SalesListView.as_view(), name='list'),
    path('sales_list/', SalesListView.as_view(), name='list'),
    path('sales_list/<pk>/', SaleDetailView.as_view(), name='detail'),
    path('from_file/', UploadTemplateView.as_view(), name='from-file'),
    path('from_file/upload/', csv_upload_view, name='upload'),
]
