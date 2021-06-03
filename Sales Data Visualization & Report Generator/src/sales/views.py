import csv

import pandas as pd
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
# from django.views.generic import DetailView, ListView
from django.views.generic import DetailView, ListView, TemplateView
from reports.forms import ReportForm

from .forms import SalesSearchForm
from .models import CSV, Position, Sale
from .utils import get_chart, get_customer_from_id, get_sales_rep_from_id

from django.utils.dateparse import parse_date
from products.models import Product
from customers.models import Customer
from profiles.models import Profile

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
# def home_view(request):
@login_required
def home_view(request):
    sales_df = None
    positions_df = None
    merged_df = None
    df = None
    chart = None
    no_data = None

    # hello = 'Hello World from the home view'
    # # return render(request, 'sales/main.html', {})
    # # return render(request, 'sales/main.html', {'h':hello})
    # return render(request, 'sales/home.html', {'hello':hello})
    
    # form = SalesSearchForm(request.POST or None)
    # # hello = 'Hello World from the home view'
    # context = {
    #     # 'hello':hello,
    #     'form':form,
    # }
    # # return render(request, 'sales/home.html', {'hello':hello})
    # return render(request, 'sales/home.html', context)

    search_form = SalesSearchForm(request.POST or None)
    report_form = ReportForm()

    if request.method == 'POST':
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')
        # print(date_from, date_to, chart_type)
        results_by = request.POST.get('results_by')

    # qs = Sale.objects.all()
    # print(qs)
    # qs = Sale.objects.get(id=1)
    # print(qs)
        # qs = Sale.objects.filter(created_on=date_from)
        # print(qs)
        # qs = Sale.objects.filter(created_on__date=date_from)
        # qs = Sale.objects.filter(created_on__date__lte=date_to, created_on__date__gte=date_from)
        sale_qs = Sale.objects.filter(created_on__date__lte=date_to, created_on__date__gte=date_from)
        # if len(qs) > 0:
        if len(sale_qs) > 0:
        # obj = Sale.objects.get(id=1)
        # print(qs)
        # print(qs.values())
        # print(qs.values_list())
        # print('######################')
        # df1 = pd.DataFrame(qs.values())
        # print(df1)
        # print('######################')
        # df2 = pd.DataFrame(qs.values_list())
        # print(df2)
            # df1 = pd.DataFrame(qs.values())
            # sales_df = pd.DataFrame(qs.values())
            # sales_df = pd.DataFrame(qs.values())
            sales_df = pd.DataFrame(sale_qs.values())
            # print(sales_df['customer_id'])
            sales_df['customer_id'] = sales_df['customer_id'].apply(get_customer_from_id)
            # print(sales_df['sales_rep_id'])
            sales_df['sales_rep_id'] = sales_df['sales_rep_id'].apply(get_sales_rep_from_id)
            # sales_df = sales_df.rename({'customer_id':'customer', 'sales_rep_id':'sales_rep'}, axis=1)
            # sales_df.rename({'customer_id':'customer', 'sales_rep_id':'sales_rep'}, axis=1, inplace=True)
            sales_df.rename({'customer_id':'customer', 'sales_rep_id':'sales_rep', 'id':'sales_id'}, axis=1, inplace=True)
            # sales_df['sales_id'] = sales_df['id']
            # sales_df['created_on'] = sales_df['created_on'].apply(lambda x: x.strftime('%y-%m-%d'))
            sales_df['created_on'] = sales_df['created_on'].apply(lambda x: x.strftime('%Y-%m-%d'))
            # sales_df = sales_df.to_html()
            # print(df1)
            # print(sales_df)
            positions_data = []
            for sale in sale_qs:
                for pos in sale.get_positions():
                    # obj = {
                    #     'position_id': pos.id,
                    #     'product': pos.product.name,
                    #     'quantity':pos.quantity,
                    #     'price':pos.price,
                    # }
                    obj = {
                        'position_id': pos.id,
                        'product': pos.product.name,
                        'quantity':pos.quantity,
                        'price':pos.price,
                        'sales_id': pos.get_sales_id(),
                    }
                    positions_data.append(obj)
            positions_df = pd.DataFrame(positions_data)
            # print('positions df')
            # print(positions_df)
            merged_df = pd.merge(sales_df, positions_df, on='sales_id')
            # sales_df = sales_df.to_html()
            # positions_df = positions_df.to_html()
            # merged_df = merged_df.to_html()

            df = merged_df.groupby('transaction_id', as_index=False)['price'].agg('sum')
            
            # sales_df = sales_df.to_html()
            # positions_df = positions_df.to_html()
            # merged_df = merged_df.to_html()
            # df = df.to_html()

            # sales_df = sales_df.to_html()
            # positions_df = positions_df.to_html()
            # merged_df = merged_df.to_html()

            # chart = get_chart(chart_type, df)
            # chart = get_chart(chart_type, df, labels=df['transaction_id'].values)
            chart = get_chart(chart_type, sales_df, results_by)
            print('Chart', chart)

            sales_df = sales_df.to_html()
            positions_df = positions_df.to_html()
            merged_df = merged_df.to_html()
            df = df.to_html()
        else:
            # print('No data!')
            # no_data = 'No data available in this date range'
            no_data = 'No data is available in this date range'
    # context = {
    #     'form':form,
    #     'sales_df':sales_df,
    # }
    # context = {
    #     'form':form,
    #     'sales_df':sales_df,
    #     'positions_df':positions_df,
    # }
    # context = {
    #     'form':form,
    #     'sales_df':sales_df,
    #     'positions_df':positions_df,
    #     'merged_df':merged_df,
    # }
    # context = {
    #     'form':form,
    #     'sales_df':sales_df,
    #     'positions_df':positions_df,
    #     'merged_df':merged_df,
    #     'df':df
    # }
    # context = {
    #     'form':form,
    #     'sales_df':sales_df,
    #     'positions_df':positions_df,
    #     'merged_df':merged_df,
    #     'df':df,
    #     'chart':chart
    # }
    # context = {
    #     'search_form':search_form,
    #     'report_form':report_form,
    #     'sales_df':sales_df,
    #     'positions_df':positions_df,
    #     'merged_df':merged_df,
    #     'df':df,
    #     'chart':chart
    # }
    context = {
        'search_form':search_form,
        'report_form':report_form,
        'sales_df':sales_df,
        'positions_df':positions_df,
        'merged_df':merged_df,
        'df':df,
        'chart':chart,
        'no_data':no_data
    }
    return render(request, 'sales/home.html', context)

# class SalesListView(ListView):
class SalesListView(LoginRequiredMixin, ListView):
    model = Sale
    template_name = 'sales/main.html'
    # context_object_name = 'qs'

# class SaleDetailView(DetailView):
class SaleDetailView(LoginRequiredMixin, DetailView):
    model = Sale
    template_name = 'sales/detail.html'

# alternative function-based views or the two class-based views (i.e. generic views) above

# def sale_list_view(request):
#     query_set = Sale.objects.all()
#     return render(request, 'sales/main.html', {'object_list':query_set})

# def sale_detail_view(request, pk):
#     obj = Sale.objects.get(pk=pk)
#     # or
#     # obj = get_object_or_404(Sale, pk=pk)
#     return render(request, 'sales/detail.html', {'object_list':obj})

# # or

# def sale_detail_view(request, **kwargs):
#     pk = kwargs.get('pk')
#     obj = Sale.objects.get(pk=pk)
#     return render(request, 'sales/detail.html', {'object':obj})

'''
in the urlpatterns:
path('sales/', sales_list_view, name='list'),
path('sales/<pk>/', sales_detail_view, name='detail'),
'''

# class UploadTemplateView(TemplateView):
class UploadTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'sales/from_file.html'

# def csv_upload_view(request):
#     return HttpResponse()
# def csv_upload_view(request):
@login_required
def csv_upload_view(request):
    print('File is being uploaded ...')

    if request.method == 'POST':
        csv_file_name = request.FILES.get('file').name
        csv_file = request.FILES.get('file')
        # obj = CSV.objects.create(filename=csv_file)
        obj, created = CSV.objects.get_or_create(filename=csv_file_name)

        # # with open(obj.filename.path, 'r') as f:
        # #     reader = csv.reader(f)
        # #     for row in reader:
        # #         print(row, type(row))
        # with open(obj.filename.path, 'r') as f:
        #     reader = csv.reader(f)
        #     reader.__next__()
        #     for row in reader:
        #         # print(row, type(row))
        #         # data = ''.join(row)
        #         # print(data, type(data))
        #         # data = data.split(';')
        #         # data = data.split(',')
        #         # print(data, type(data))
        #         # data.pop()
        #         # print(data, type(data))
        #         # print('')
                
        #         # transaction_id = data[1]
        #         # product = data[2]
        #         # quantity = int(data[3])
        #         # customer = data[4]
        #         # date = parse_date(data[5])
        #         transaction_id = row[1]
        #         product = row[2]
        #         quantity = int(row[3])
        #         customer = row[4]
        #         date = parse_date(row[5])

        #         # Step 1:
        #         try:
        #             # product_obj = Product.objects.get(name=product)
        #             product_obj = Product.objects.get(name__iexact=product)
        #         except Product.DoesNotExist:
        #             product_obj = None
        #         # print(product_obj)
                
        #         # Step 2:
        #         if product_obj is not None:
        #             # customer_obj, _ = Customer.objects.get_or_create(name=customer)
        #             # customer_obj, new_customer = Customer.objects.get_or_create(name=customer)
        #             customer_obj, _ = Customer.objects.get_or_create(name=customer)
                    
        #             # Step 3:
        #             sales_rep_obj = Profile.objects.get(user=request.user)
        #             position_obj = Position.objects.create(product=product_obj, quantity=quantity, created_on=date)
                    
        #             sale_obj, _ = Sale.objects.get_or_create(transaction_id=transaction_id, customer=customer_obj, sales_rep=sales_rep_obj, created_on=date)
        #             sale_obj.positions.add(position_obj)
        #             sale_obj.save()

        if created:
            obj.csv_file = csv_file
            obj.save()

            with open(obj.csv_file.path, 'r') as f:
                reader = csv.reader(f)
                reader.__next__()
                for row in reader:
                    transaction_id = row[1]
                    product = row[2]
                    quantity = int(row[3])
                    customer = row[4]
                    date = parse_date(row[5])

                    # Step 1:
                    try:
                        product_obj = Product.objects.get(name__iexact=product)
                    except Product.DoesNotExist:
                        product_obj = None
                    
                    # Step 2:
                    if product_obj is not None:
                        customer_obj, _ = Customer.objects.get_or_create(name=customer)
                        
                        # Step 3:
                        sales_rep_obj = Profile.objects.get(user=request.user)
                        position_obj = Position.objects.create(product=product_obj, quantity=quantity, created_on=date)
                        
                        sale_obj, _ = Sale.objects.get_or_create(transaction_id=transaction_id, customer=customer_obj, sales_rep=sales_rep_obj, created_on=date)
                        sale_obj.positions.add(position_obj)
                        sale_obj.save()
                
                # Step 4
                return JsonResponse({'ex':False})
        else:
            return JsonResponse({'ex':True})

    return HttpResponse()
