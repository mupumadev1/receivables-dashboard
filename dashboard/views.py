import datetime
import io
from io import BytesIO, StringIO
from itertools import groupby
from operator import attrgetter

import pandas as pd
from django.db.models.functions import TruncDate
from django.http import HttpResponse
from django.shortcuts import render
from dashboard.models import *
from .forms import *
from django.db.models import Count, Q
from django.core.paginator import Paginator

from dateutil.relativedelta import relativedelta

global conn, b
b = io.BytesIO()
conn = ("mysql://saservice:mJ%40PcJ%21pNVs2%2AAW@localhost/sageservice")

# RECEIVABLES


def recievables_successfull_trans(request):
    distinct = ProcessedTransactions.objects.values('transid').annotate(name_count=Count('transid')
                                                                        ).filter(name_count=1)
    sucessfull_trans = ProcessedTransactions.objects.filter(status=1, transid__in=[item['transid'] for item in
                                                                                   distinct]).order_by('-entrydate')
    p = Paginator(sucessfull_trans, 10)
    page_number = request.GET.get('page')
    item = p.get_page(page_number)
    all_data = sucessfull_trans.filter(entrydate__year=2023)
    grouped_data = groupby(all_data, key=attrgetter('entrydate.month'))
    monthly_data = {month: 0 for month in range(1, 13)}
    for month, data in grouped_data:
        monthly_data[month] = len(list(data))
    monthly_data = [{'month': datetime.date(1900, month, 1).strftime('%B'), 'data': count} for month, count in
                    monthly_data.items()]
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=7)

    date_range = [end_date - datetime.timedelta(days=x) for x in range(7)]
    processed_deposits = ProcessedTransactions.objects.filter(entrydate__date__range=(start_date, end_date))
    processed_deposits = processed_deposits.annotate(trans_date=TruncDate('entrydate')).values('trans_date').annotate(
        count=Count('trans_date'))
    date_dict = {deposit['trans_date'].strftime('%Y-%m-%d'): deposit['count'] for deposit in processed_deposits}
    date_list = [date.strftime('%Y-%m-%d') for date in date_range]
    count_list = [date_dict.get(date.strftime('%Y-%m-%d'), 0) for date in date_range]
    context = {'s_t': item,
               'date_list': date_list,
               'count_list': count_list,
               'data_by_month': monthly_data,
               }

    return render(request, "dashboard/transactions.html", context)


def search_results(request):
    search_params = request.GET.get('search_params')
    field_option = request.GET.get('filter_options')
    field_mapping = {
        'customer_no': 'customer_no',
        'amount': 'amount__icontains',
        'transaction_id': 'transid',
        'transaction_date':'transdate',
        'entry_date': 'entrydate'
    }
    if field_option in field_mapping and search_params:
        transactions = ProcessedTransactions.objects.filter(**{field_mapping[field_option]: search_params}).all()
        print(transactions)
        paginator = Paginator(transactions, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            's_t': page_obj,
        }
        return render(request, 'dashboard/transactions.html', context)


def format_date(date_str):
    date_obj = datetime.strptime(date_str, '%d-%m-%Y')
    formatted_date = date_obj.strftime('%Y-%m-%d')
    return formatted_date


def generate_report(request):
    column_names = ['Customer Name', 'Customer Number', 'Remarks', 'Amount', 'Transaction ID', 'Transaction Date',
                    'Entry Date']
    search_params = request.GET.get('search_params')
    field_option = request.GET.get('filter_options')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    field_mapping = {
        'customer_no': 'customer_no',
        'amount': 'amount',
        'transid': 'transaction_id',
        'transdate': 'transaction_date',
        'entrydate': 'entry_date'
    }

    if field_option in field_mapping and search_params:
        transactions = ProcessedTransactions.objects.filter(**{field_mapping[field_option]: search_params},
                                                            transdate__range=[start_date, end_date]).order_by(
            '-entrydate').values('customername', 'customer_no', 'name', 'amount', 'transid', 'transdate',
                                 'entrydate').all()
        df = pd.DataFrame(list(transactions))
        if transactions.exists():
            df['entrydate'] = df['entrydate'].dt.strftime('%Y-%m-%d %H:%M:%S')

            output = BytesIO()
            writer = pd.ExcelWriter(output, engine='openpyxl')

            df.to_excel(writer, sheet_name='Sheet1', index=False, startrow=1)  # Start data from row 2

            # Write title and column names separately
            worksheet = writer.sheets['Sheet1']
            worksheet.cell(row=1, column=1, value=f'Transactions Between {start_date} and {end_date}')  # Write title
            for col_num, col_name in enumerate(column_names, start=1):
                worksheet.cell(row=2, column=col_num, value=col_name)  # Write column names

            writer.save()
            output.seek(0)

            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=report.xlsx'
            response.write(output.getvalue())
            return response
        else:
            output = BytesIO()
            writer = pd.ExcelWriter(output, engine='openpyxl')

            df.to_excel(writer, sheet_name='Sheet1', index=False, startrow=1)  # Start data from row 2

            # Write title and column names separately
            worksheet = writer.sheets['Sheet1']
            worksheet.cell(row=1, column=1, value=f'Transactions Between {start_date} and {end_date}')  # Write title
            for col_num, col_name in enumerate(column_names, start=1):
                worksheet.cell(row=2, column=col_num, value=col_name)  # Write column names

            writer.save()
            output.seek(0)

            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=report.xlsx'
            response.write(output.getvalue())
            return response
    else:
        data = ProcessedTransactions.objects.filter(entrydate__range=(start_date, end_date)).order_by(
            '-entrydate').values('customername', 'customer_no', 'name', 'amount', 'transid', 'transdate',
                                 'entrydate').all()

        df = pd.DataFrame(list(data))
        if data.exists():
            print('true')
            df['entrydate'] = df['entrydate'].dt.strftime('%Y-%m-%d %H:%M:%S')

            output = BytesIO()
            writer = pd.ExcelWriter(output, engine='openpyxl')

            df.to_excel(writer, sheet_name='Sheet1', index=False, startrow=1)  # Start data from row 2

            # Write title and column names separately
            worksheet = writer.sheets['Sheet1']
            worksheet.cell(row=1, column=1, value=f'Transactions Between {start_date} and {end_date}')  # Write title
            for col_num, col_name in enumerate(column_names, start=1):
                worksheet.cell(row=2, column=col_num, value=col_name)  # Write column names

            writer.save()
            output.seek(0)

            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=report.xlsx'
            response.write(output.getvalue())
            return response
        else:
            output = BytesIO()
            writer = pd.ExcelWriter(output, engine='openpyxl')
            df.to_excel(writer, sheet_name='Sheet1', index=False, startrow=1)  # Start data from row 2
            # Write title and column names separately
            worksheet = writer.sheets['Sheet1']
            worksheet.cell(row=1, column=1, value=f'Transactions Between {start_date} and {end_date}')  # Write title
            for col_num, col_name in enumerate(column_names, start=1):
                worksheet.cell(row=2, column=col_num, value=col_name)  # Write column names

            writer.save()
            output.seek(0)

            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=report.xlsx'
            response.write(output.getvalue())
            return response


