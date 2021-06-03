import uuid, base64
from customers.models import Customer
from profiles.models import Profile
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns

def generate_code():
    # code = str(uuid.uuid4()).replace('-', '')[:12]
    # print(code) => # d7fee3f6-7df6-4f5f-982b-baea54597edc
    # print(code_mod) => # d7fee3f67df6
    code = str(uuid.uuid4()).replace('-', '').upper()[:12]
    return code

def get_sales_rep_from_id(val):
    # pass
    sales_rep = Profile.objects.get(id=val)
    # return sales_rep
    return sales_rep.user.username

def get_customer_from_id(val):
    # pass
    customer = Customer.objects.get(id=val)
    return customer

def get_graph():
    # pass
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

# def get_chart(chart_type, data, **kwargs):
def get_chart(chart_type, data, results_by, **kwargs):
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(10, 4))
    key = get_key(results_by)
    d = data.groupby(key, as_index=False)['total_price'].agg('sum')
    if chart_type == '#1':
        # print('bar chart')
        # plt.bar(data['transaction_id'], data['price'])
        # sns.barplot(x='transaction_id', y='price', data=data)
        sns.barplot(x=key, y='total_price', data=d)
        # plt.bar(d[key], d['total_price'])
    elif chart_type == '#2':
        # print('pie chart')
        # labels = kwargs.get('labels')
        # plt.pie(data=data, x='price', labels=labels)
        plt.pie(data=d, x='total_price', labels=d[key].values)
    elif chart_type == '#3':
        # print('line chart')
        # plt.plot(data['transaction_id'], data['price'])
        # plt.plot(data['transaction_id'], data['price'], color='green', marker='o')
        # plt.plot(data['transaction_id'], data['price'], color='green', marker='o', linestyle='dashed')
        plt.plot(d[key], d['total_price'], color='green', marker='o', linestyle='dashed')
    else:
        print('oops ... failed to identify the chart type')
    plt.tight_layout()
    chart = get_graph()
    return chart

def get_key(res_by):
    if res_by == '#1':
        key = 'transaction_id'
    elif res_by == '#2':
        key = 'created_on'
    return key