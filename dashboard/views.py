import io
from io import BytesIO, StringIO
import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render
from dashboard.models import *
from .forms import *
from django.db.models import Count
from django.core.paginator import Paginator
from datetime import *
from dateutil.relativedelta import relativedelta

global conn, b
b = io.BytesIO()
conn = ("mysql://saservice:mJ%40PcJ%21pNVs2%2AAW@localhost/sageservice")

def homepage(request):
    return render(request, "dashboard/index.html")
#RECEIVABLES
def receivables_index(request):

    sucessfull_trans = ProcessedTransactions.objects.filter(status=1).count()
    unsucesfull_trans = ProcessedTransactions.objects.filter(status=0).count()
    duplicates = ProcessedTransactions.objects.filter(status=-1).count()
    
    context = {
        's_t': sucessfull_trans,
        'u_t': unsucesfull_trans,
        'd_t': duplicates,
        
    }

    return render(request, "dashboard/index.html", context)

def set_fields(reference_no, amt, customer_no):
    global amount, cust_no, ref_no
    amount = amt
    cust_no = customer_no
    ref_no = reference_no
    return amount, cust_no, ref_no

def by_date_form(request):
    return render (request, "dashboard/date_search.html")

def by_field_form(request):
    return render (request, "dashboard/search.html")

def set_dates(st_date, en_date):
    global s_date, e_date
    s_date = st_date
    e_date = en_date

def recievables_successfull_trans(request,page):
    distinct = ProcessedTransactions.objects.values('transid').annotate(name_count=Count('transid')
).filter(name_count=1)
    sucessfull_trans = ProcessedTransactions.objects.filter(status=1,transid__in=[item['transid'] for item in distinct]).order_by('-entrydate')
    p = Paginator(sucessfull_trans,10)
    item = p.get_page(page)
    nums = "a" * item.paginator.num_pages
    return render(request, "dashboard/transactions.html", { 's_t':item, 'nums':nums, })

def successful_transactions_results(request):
        distinct = ProcessedTransactions.objects.values('transid').annotate(name_count=Count('transid')
).filter(name_count=1)

        trans_list = ProcessedTransactions.objects.filter(status=1, transid__in=[item['transid'] for item in distinct]).order_by('-entrydate')
        if 'date_init' and 'date_fin' in request.GET:
            start_date = request.GET['date_init']
            end_date = request.GET['date_fin']
            set_dates(start_date, end_date)
            raw_trans = trans_list.filter(entrydate__range=[start_date, end_date]).all()
            
            return render (request, "dashboard/transaction_results.html", {'s_t':raw_trans,'s_date':start_date,'e_date':end_date})

def successful_receivables_date_report(request):
    start_date= s_date + " 00:00:00"
    end_date = e_date + " 00:00:00"
    print(start_date, end_date)
    v = f"SELECT `processed_transactions`.`id`, `processed_transactions`.`processed`, `processed_transactions`.`customer_no`, `processed_transactions`.`amount`, `processed_transactions`.`name`, `processed_transactions`.`transId`, `processed_transactions`.`transDate`, `processed_transactions`.`entryDate` FROM `processed_transactions` WHERE (`processed_transactions`.`status` = 1 AND `processed_transactions`.`entryDate` BETWEEN '{start_date}' AND '{end_date}' )"
    df = pd.read_sql_query(v, conn)
    writer = pd.ExcelWriter(b, engine='openpyxl')
    df.to_excel(writer, sheet_name='Transactions')
    writer.save()
    response = HttpResponse(b.getvalue(), content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Report1.xls"'
    return response

def unsuccessful_receivables_date_report(request):
    start_date= s_date + " 00:00:00"
    end_date = e_date + " 00:00:00"
    print(start_date, end_date)
    v = f"SELECT `processed_transactions`.`id`, `processed_transactions`.`processed`, `processed_transactions`.`customer_no`, `processed_transactions`.`amount`, `processed_transactions`.`name`, `processed_transactions`.`transId`, `processed_transactions`.`transDate`, `processed_transactions`.`entryDate` FROM `processed_transactions` WHERE (`processed_transactions`.`status` = 0 AND `processed_transactions`.`entryDate` BETWEEN '{start_date}' AND '{end_date}' )"
    df = pd.read_sql_query(v, conn)
    writer = pd.ExcelWriter(b, engine='openpyxl')
    df.to_excel(writer, sheet_name='Transactions')
    writer.save()
    response = HttpResponse(b.getvalue(), content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Report1.xls"'
    return response

def successful_receivables_by_field(request):
    
    trans_list = ProcessedTransactions.objects.filter(status=1).order_by('-entrydate')
    if 'ref_no' in request.GET:
        ref_no = request.GET['ref_no']
        if ref_no:
            trans_list = trans_list.filter(transid__icontains=ref_no)
    

    if 'cust_no' in request.GET:
        cust_no = request.GET['cust_no']
        if cust_no:
            
            trans_list = trans_list.filter(customer_no__iexact = cust_no)
    
    if 'amount' in request.GET:
        amount = request.GET['amount']
        if amount:
            trans_list = trans_list.filter(amount__iexact = amount)
    if amount == '':
        amnt = '-'
    else:
        amnt = amount
    if ref_no == '':
        refer_no= '-'
    else:
        refer_no = ref_no
    if cust_no == '':
        custm_no = '-' 
    else:
        custm_no = cust_no

    print(set_fields(refer_no, amnt, custm_no))
    

    return render (request, "dashboard/transaction_results_by_field.html", {'s_t':trans_list,'ref_no':ref_no,'cust_no':cust_no,'amount':amount})



def successful_receivables_by_field_report(request):
    if cust_no != '-' and amount != '-' and ref_no != '-': 
    
        v = f"SELECT `processed_transactions`.`id`, `processed_transactions`.`processed`, `processed_transactions`.`customer_no`, `processed_transactions`.`amount`, `processed_transactions`.`name`, `processed_transactions`.`transId`, `processed_transactions`.`transDate`, `processed_transactions`.`entryDate` FROM `processed_transactions` WHERE (`processed_transactions`.`amount` = '{amount}' AND `processed_transactions`.`customer_no` = '{cust_no}' AND `processed_transactions`.`status` = 1 AND `processed_transactions`.`transId` = '{ref_no}')"
    elif cust_no != '-' and amount  != '-':
        
        v = f"SELECT `processed_transactions`.`id`, `processed_transactions`.`processed`, `processed_transactions`.`customer_no`, `processed_transactions`.`amount`, `processed_transactions`.`name`, `processed_transactions`.`transId`, `processed_transactions`.`transDate`, `processed_transactions`.`entryDate` FROM `processed_transactions` WHERE (`processed_transactions`.`amount` = '{amount}' AND `processed_transactions`.`customer_no` = '{cust_no}' AND `processed_transactions`.`status` = 1)"

    elif ref_no != '-'and amount != '-':
        
        v =f"SELECT `processed_transactions`.`id`, `processed_transactions`.`processed`, `processed_transactions`.`customer_no`, `processed_transactions`.`amount`, `processed_transactions`.`name`, `processed_transactions`.`transId`, `processed_transactions`.`transDate`, `processed_transactions`.`entryDate` FROM `processed_transactions` WHERE (`processed_transactions`.`amount` = '{amount}' AND `processed_transactions`.`status` = 1 AND `processed_transactions`.`transId` = '{ref_no}')"
 
    elif ref_no != '-' and cust_no != '-':
        
        v = f"SELECT `processed_transactions`.`id`, `processed_transactions`.`processed`, `processed_transactions`.`customer_no`, `processed_transactions`.`amount`, `processed_transactions`.`name`, `processed_transactions`.`transId`, `processed_transactions`.`transDate`, `processed_transactions`.`entryDate` FROM `processed_transactions` WHERE (`processed_transactions`.`customer_no` = '{cust_no}' AND `processed_transactions`.`status` = 1 AND `processed_transactions`.`transId` = '{ref_no}')"
                                                          
    elif cust_no != '-':
        
        v = f"SELECT `processed_transactions`.`id`, `processed_transactions`.`processed`, `processed_transactions`.`customer_no`, `processed_transactions`.`amount`, `processed_transactions`.`name`, `processed_transactions`.`transId`, `processed_transactions`.`transDate`, `processed_transactions`.`entryDate` FROM `processed_transactions` WHERE (`processed_transactions`.`customer_no` = '{cust_no}' AND `processed_transactions`.`status` = 1 )"
 
    elif amount != '-':
    
        v = f"SELECT `processed_transactions`.`id`, `processed_transactions`.`processed`, `processed_transactions`.`customer_no`, `processed_transactions`.`amount`, `processed_transactions`.`name`, `processed_transactions`.`transId`, `processed_transactions`.`transDate`, `processed_transactions`.`entryDate` FROM `processed_transactions` WHERE (`processed_transactions`.`amount` = '{amount}' AND `processed_transactions`.`status` = 1 )"
 
    elif ref_no != '-':
    
        v = f"SELECT `processed_transactions`.`id`, `processed_transactions`.`processed`, `processed_transactions`.`customer_no`, `processed_transactions`.`amount`, `processed_transactions`.`name`, `processed_transactions`.`transId`, `processed_transactions`.`transDate`, `processed_transactions`.`entryDate` FROM `processed_transactions` WHERE (`processed_transactions`.`transid` = '{ref_no}' AND `processed_transactions`.`status` = 1 )"
    df = pd.read_sql_query(v, conn)
    print(df)
    writer = pd.ExcelWriter(b, engine='openpyxl')
    df.to_excel(writer, sheet_name='Transactions')
    writer.save()
    response = HttpResponse(b.getvalue(), content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Report1.xls"'
    return response
def successful_transactions_report_to_excel(request):
    v = str(ProcessedTransactions.objects.filter(status=1).values('id', 'processed', 'customer_no', 'amount', 'name',
                                                             'transid', 'transdate', 'entrydate').query)
    df = pd.read_sql_query(v, conn)
    print(df)
    writer = pd.ExcelWriter(b, engine='openpyxl')
    df.to_excel(writer, sheet_name='Transactions')
    writer.save()
    response = HttpResponse(b.getvalue(), content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Report1.xls"'
    return response

def receivables_unsuccessfull_trans(request,page):
    unsucessfull_trans = ProcessedTransactions.objects.filter(status=0).order_by('-entrydate')
    p = Paginator(unsucessfull_trans, 10)
    item = p.get_page(page)
    nums = "a" * item.paginator.num_pages
    return render(request, "dashboard/unsuccessful_transactions.html", {'u_t':item, 'nums':nums})

def unsuccessful_transactions_results(request):
        trans_list = ProcessedTransactions.objects.filter(status=0).order_by('-entrydate')
        if 'date_init' and 'date_fin' in request.GET:
            start_date = request.GET['date_init']
            end_date = request.GET['date_fin']
            set_dates(start_date, end_date)
            raw_trans = trans_list.filter(entrydate__range=[start_date, end_date]).all()
            
            return render (request, "dashboard/unsuccessful_transaction_results.html", {'u_t':raw_trans,'s_date':start_date,'e_date':end_date})
def unsuccessful_receivables_by_field(request):
    
    trans_list = ProcessedTransactions.objects.filter(status=0).order_by('-entrydate')
    if 'ref_no' in request.GET:
        ref_no = request.GET['ref_no']
        if ref_no:
            trans_list = trans_list.filter(transid__icontains=ref_no)
    

    if 'cust_no' in request.GET:
        cust_no = request.GET['cust_no']
        if cust_no:
            
            trans_list = trans_list.filter(customer_no__iexact = cust_no)
    
    if 'amount' in request.GET:
        amount = request.GET['amount']
        if amount:
            trans_list = trans_list.filter(amount__iexact = amount)
    if amount == '':
        amnt = '-'
    else:
        amnt = amount
    if ref_no == '':
        refer_no= '-'
    else:
        refer_no = ref_no
    if cust_no == '':
        custm_no = '-' 
    else:
        custm_no = cust_no

    print(set_fields(refer_no, amnt, custm_no))
    
    
    return render (request, "dashboard/unsuccessful_transaction_results_by_field.html", {'u_t':trans_list,'ref_no':ref_no,'cust_no':cust_no,'amount':amount})

def unsuccessful_receivables_by_field_report(request):
    if cust_no != '-' and amount != '-' and ref_no != '-': 
    
        v = f"SELECT `processed_transactions`.`id`, `processed_transactions`.`processed`, `processed_transactions`.`customer_no`, `processed_transactions`.`amount`, `processed_transactions`.`name`, `processed_transactions`.`transId`, `processed_transactions`.`transDate`, `processed_transactions`.`entryDate` FROM `processed_transactions` WHERE (`processed_transactions`.`amount` = '{amount}' AND `processed_transactions`.`customer_no` = '{cust_no}' AND `processed_transactions`.`status` = 0 AND `processed_transactions`.`transId` = '{ref_no}')"
    elif cust_no != '-' and amount  != '-':
        
        v = f"SELECT `processed_transactions`.`id`, `processed_transactions`.`processed`, `processed_transactions`.`customer_no`, `processed_transactions`.`amount`, `processed_transactions`.`name`, `processed_transactions`.`transId`, `processed_transactions`.`transDate`, `processed_transactions`.`entryDate` FROM `processed_transactions` WHERE (`processed_transactions`.`amount` = '{amount}' AND `processed_transactions`.`customer_no` = '{cust_no}' AND `processed_transactions`.`status` = 0)"

    elif ref_no != '-'and amount != '-':
        
        v =f"SELECT `processed_transactions`.`id`, `processed_transactions`.`processed`, `processed_transactions`.`customer_no`, `processed_transactions`.`amount`, `processed_transactions`.`name`, `processed_transactions`.`transId`, `processed_transactions`.`transDate`, `processed_transactions`.`entryDate` FROM `processed_transactions` WHERE (`processed_transactions`.`amount` = '{amount}' AND `processed_transactions`.`status` = 0 AND `processed_transactions`.`transId` = '{ref_no}')"
 
    elif ref_no != '-' and cust_no != '-':
        
        v = f"SELECT `processed_transactions`.`id`, `processed_transactions`.`processed`, `processed_transactions`.`customer_no`, `processed_transactions`.`amount`, `processed_transactions`.`name`, `processed_transactions`.`transId`, `processed_transactions`.`transDate`, `processed_transactions`.`entryDate` FROM `processed_transactions` WHERE (`processed_transactions`.`customer_no` = '{cust_no}' AND `processed_transactions`.`status` = 0 AND `processed_transactions`.`transId` = '{ref_no}')"
                                                          
    elif cust_no != '-':
        
        v = f"SELECT `processed_transactions`.`id`, `processed_transactions`.`processed`, `processed_transactions`.`customer_no`, `processed_transactions`.`amount`, `processed_transactions`.`name`, `processed_transactions`.`transId`, `processed_transactions`.`transDate`, `processed_transactions`.`entryDate` FROM `processed_transactions` WHERE (`processed_transactions`.`customer_no` = '{cust_no}' AND `processed_transactions`.`status` = 0 )"
 
    elif amount != '-':
    
        v = f"SELECT `processed_transactions`.`id`, `processed_transactions`.`processed`, `processed_transactions`.`customer_no`, `processed_transactions`.`amount`, `processed_transactions`.`name`, `processed_transactions`.`transId`, `processed_transactions`.`transDate`, `processed_transactions`.`entryDate` FROM `processed_transactions` WHERE (`processed_transactions`.`amount` = '{amount}' AND `processed_transactions`.`status` = 0 )"
 
    elif ref_no != '-':
        
        v = f"SELECT `processed_transactions`.`id`, `processed_transactions`.`processed`, `processed_transactions`.`customer_no`, `processed_transactions`.`amount`, `processed_transactions`.`name`, `processed_transactions`.`transId`, `processed_transactions`.`transDate`, `processed_transactions`.`entryDate` FROM `processed_transactions` WHERE (`processed_transactions`.`transid` = '{ref_no}' AND `processed_transactions`.`status` = 0 )"
    df = pd.read_sql_query(v, conn)
    writer = pd.ExcelWriter(b, engine='openpyxl')
    df.to_excel(writer, sheet_name='Transactions')
    writer.save()
    response = HttpResponse(b.getvalue(), content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Report1.xls"'
    return response

def unsuccessful_transactions_report_to_excel(request):
    v = ProcessedTransactions.objects.filter(status=0).values('id', 'processed', 'customer_no', 'amount', 'name',
                                                                  'transid', 'transdate', 'entrydate').query
    df = pd.read_sql_query(v, conn)
    print(df)
    writer = pd.ExcelWriter(b, engine='openpyxl')
    df.to_excel(writer, sheet_name='Transactions')
    writer.save()
    response = HttpResponse(b.getvalue(), content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Report1.xls"'
    return response

def duplicates(request,page):
    duplicates = ProcessedTransactions.objects.filter(status=-1).order_by('-entrydate')
    p = Paginator(duplicates, 10)
    form = DateForm()
    item = p.get_page(page)
    nums = "a" * item.paginator.num_pages
    return render(request, "dashboard/duplicate_transactions.html", {'d_t':item, 'nums':nums, 'form': form})

def duplicate_transactions_results(request):
        trans_list = ProcessedTransactions.objects.filter(status=-1).order_by('-entrydate')
        if 'date_init' and 'date_fin' in request.GET:
            start_date = request.GET['date_init']
            end_date = request.GET['date_fin']
            set_dates(start_date, end_date)
            raw_trans = trans_list.filter(entrydate__range=[start_date, end_date]).all()
            
            return render (request, "dashboard/duplicate_transaction_results.html", {'d_t':raw_trans,'s_date':start_date,'e_date':end_date})

def duplicate_receivables_by_field(request):
    
    trans_list = ProcessedTransactions.objects.filter(status=-1).order_by('-entrydate')
    if 'ref_no' in request.GET:
        ref_no = request.GET['ref_no']
        if ref_no:
            trans_list = trans_list.filter(transid__icontains=ref_no)
    if 'cust_no' in request.GET:
        cust_no = request.GET['cust_no']
        if cust_no: 
            trans_list = trans_list.filter(customer_no__iexact = cust_no)
    if 'amount' in request.GET:
        amount = request.GET['amount']
        if amount:
            trans_list = trans_list.filter(amount__iexact = amount)
    if amount == '':
        amnt = '-'
    else:
        amnt = amount
    if ref_no == '':
        refer_no= '-'
    else:
        refer_no = ref_no
    if cust_no == '':
        custm_no = '-' 
    else:
        custm_no = cust_no

    set_fields(refer_no, amnt, custm_no)
    
    return render (request, "dashboard/duplicate_transaction_results_by_field.html", {'d_t':trans_list,'ref_no':ref_no,'cust_no':cust_no,'amount':amount})



# DUPLICATE TRANSACTIONS
def duplicate_transactions_report_to_excel(request):
    v = ProcessedTransactions.objects.filter(status=-1).values('id', 'processed', 'customer_no', 'amount', 'name',
                                                                  'transid', 'transdate', 'entrydate').query
    df = pd.read_sql_query(v, conn)
    print(df)
    writer = pd.ExcelWriter(b, engine='openpyxl')
    df.to_excel(writer, sheet_name='Transactions')
    writer.save()
    response = HttpResponse(b.getvalue(), content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Report1.xls"'
    return response
def duplicate_receivables_date_report(request):
    start_date= s_date + " 00:00:00"
    end_date = e_date + " 00:00:00"
    print(start_date, end_date)
    v = f"SELECT `processed_transactions`.`id`, `processed_transactions`.`processed`, `processed_transactions`.`customer_no`, `processed_transactions`.`amount`, `processed_transactions`.`name`, `processed_transactions`.`transId`, `processed_transactions`.`transDate`, `processed_transactions`.`entryDate` FROM `processed_transactions` WHERE (`processed_transactions`.`status` = 0 AND `processed_transactions`.`entryDate` BETWEEN '{start_date}' AND '{end_date}' )"
    df = pd.read_sql_query(v, conn)
    writer = pd.ExcelWriter(b, engine='openpyxl')
    df.to_excel(writer, sheet_name='Transactions')
    writer.save()
    response = HttpResponse(b.getvalue(), content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Report1.xls"'
    return response

def duplicate_receivables_by_field_report(request):
    if cust_no != '-' and amount != '-' and ref_no != '-': 
    
        v = f"SELECT `processed_transactions`.`id`, `processed_transactions`.`processed`, `processed_transactions`.`customer_no`, `processed_transactions`.`amount`, `processed_transactions`.`name`, `processed_transactions`.`transId`, `processed_transactions`.`transDate`, `processed_transactions`.`entryDate` FROM `processed_transactions` WHERE (`processed_transactions`.`amount` = '{amount}' AND `processed_transactions`.`customer_no` = '{cust_no}' AND `processed_transactions`.`status` = -1 AND `processed_transactions`.`transId` = '{ref_no}')"
    elif cust_no != '-' and amount  != '-':
        
        v = f"SELECT `processed_transactions`.`id`, `processed_transactions`.`processed`, `processed_transactions`.`customer_no`, `processed_transactions`.`amount`, `processed_transactions`.`name`, `processed_transactions`.`transId`, `processed_transactions`.`transDate`, `processed_transactions`.`entryDate` FROM `processed_transactions` WHERE (`processed_transactions`.`amount` = '{amount}' AND `processed_transactions`.`customer_no` = '{cust_no}' AND `processed_transactions`.`status` = -1)"

    elif ref_no != '-'and amount != '-':
        
        v =f"SELECT `processed_transactions`.`id`, `processed_transactions`.`processed`, `processed_transactions`.`customer_no`, `processed_transactions`.`amount`, `processed_transactions`.`name`, `processed_transactions`.`transId`, `processed_transactions`.`transDate`, `processed_transactions`.`entryDate` FROM `processed_transactions` WHERE (`processed_transactions`.`amount` = '{amount}' AND `processed_transactions`.`status` = -1 AND `processed_transactions`.`transId` = '{ref_no}')"
 
    elif ref_no != '-' and cust_no != '-':
        
        v = f"SELECT `processed_transactions`.`id`, `processed_transactions`.`processed`, `processed_transactions`.`customer_no`, `processed_transactions`.`amount`, `processed_transactions`.`name`, `processed_transactions`.`transId`, `processed_transactions`.`transDate`, `processed_transactions`.`entryDate` FROM `processed_transactions` WHERE (`processed_transactions`.`customer_no` = '{cust_no}' AND `processed_transactions`.`status` = -1 AND `processed_transactions`.`transId` = '{ref_no}')"
                                                          
    elif cust_no != '-':
        
        v = f"SELECT `processed_transactions`.`id`, `processed_transactions`.`processed`, `processed_transactions`.`customer_no`, `processed_transactions`.`amount`, `processed_transactions`.`name`, `processed_transactions`.`transId`, `processed_transactions`.`transDate`, `processed_transactions`.`entryDate` FROM `processed_transactions` WHERE (`processed_transactions`.`customer_no` = '{cust_no}' AND `processed_transactions`.`status` = -1 )"
 
    elif amount != '-':
    
        v = f"SELECT `processed_transactions`.`id`, `processed_transactions`.`processed`, `processed_transactions`.`customer_no`, `processed_transactions`.`amount`, `processed_transactions`.`name`, `processed_transactions`.`transId`, `processed_transactions`.`transDate`, `processed_transactions`.`entryDate` FROM `processed_transactions` WHERE (`processed_transactions`.`amount` = '{amount}' AND `processed_transactions`.`status` = -1 )"
 
    elif ref_no != '-':
        
        v = f"SELECT `processed_transactions`.`id`, `processed_transactions`.`processed`, `processed_transactions`.`customer_no`, `processed_transactions`.`amount`, `processed_transactions`.`name`, `processed_transactions`.`transId`, `processed_transactions`.`transDate`, `processed_transactions`.`entryDate` FROM `processed_transactions` WHERE (`processed_transactions`.`transid` = '{ref_no}' AND `processed_transactions`.`status` = -1 )"
    df = pd.read_sql_query(v, conn)
    writer = pd.ExcelWriter(b, engine='openpyxl')
    df.to_excel(writer, sheet_name='Transactions')
    writer.save()
    response = HttpResponse(b.getvalue(), content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Report1.xls"'
    return response
#PAYABLES   
"""def payables_index(request):

    sucessfull_trans = PaymentTransaction.objects.filter(status="SUCCESS").count()
    unsucesfull_trans = PaymentTransaction.objects.filter(status="FAIL").count()
    

    context = {
        'p_s_t': sucessfull_trans,
        'p_u_t': unsucesfull_trans,
    
    }

    return render(request, "dashboard/index.html", context)

# PAYABLES TRANSACTIONS DISPLAY

def payables_successfull_trans(request,page):
    sucessfull_trans = PaymentTransaction.objects.filter(status="SUCCESS").order_by('-timestamp')
    p = Paginator(sucessfull_trans,10)
    item = p.get_page(page)
    nums = "a" * item.paginator.num_pages
    return render(request, "dashboard/transactions.html", { 'p_s_t':item, 'nums':nums})


def payables_unsuccessfull_trans(request,page):
    unsucessfull_trans = PaymentTransaction.objects.filter(status="FAIL").order_by('-timestamp')
    p = Paginator(unsucessfull_trans, 10)
    item = p.get_page(page)
    nums = "a" * item.paginator.num_pages
    return render(request, "dashboard/unsuccessful_transactions.html", {'p_u_t':item, 'nums':nums})

# PAYABLES REPORTS
#SUCCESSFUL TRANSACTIONS
def payables_successful_transactions_report_to_excel(request):
    v = str(PaymentTransaction.objects.filter(status="SUCCESS").values('id', 'destacc', 'service', 'amount', 'remarks',
                                                                  'referenceno', 'transactiontype', 'timestamp').query)
    df = pd.read_sql_query(v, conn)
    print(df)
    writer = pd.ExcelWriter(b, engine='openpyxl')
    df.to_excel(writer, sheet_name='Transactions')
    writer.save()
    response = HttpResponse(b.getvalue(), content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Report1.xls"'
    return response
def daily_report(request):
    start_date= datetime.now()
    end_date = datetime.now() - timedelta(days=1)
    v = f"SELECT `payment_transaction`.`id`, `payment_transaction`.`destacc`, `payment_transaction`.`service`, `payment_transaction`.`amount`, `payment_transaction`.`remarks`, `payment_transaction`.`referenceNo`, `payment_transaction`.`transactionType`, `payment_transaction`.`timestamp` FROM `payment_transaction` WHERE (`payment_transaction`.`status` = 'SUCCESS' AND `payment_transaction`.`timestamp` BETWEEN '{end_date}' AND '{start_date}')"
    df = pd.read_sql_query(v, conn)

    writer = pd.ExcelWriter(b, engine='openpyxl')
    df.to_excel(writer, sheet_name='Transactions')
    writer.save()
    response = HttpResponse(b.getvalue(), content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Report1.xls"'
    return response
def weekly_report(request):
    start_date= datetime.now()
    end_date = datetime.now() - timedelta(days=7)
    v = f"SELECT `payment_transaction`.`id`, `payment_transaction`.`destacc`, `payment_transaction`.`service`, `payment_transaction`.`amount`, `payment_transaction`.`remarks`, `payment_transaction`.`referenceNo`, `payment_transaction`.`transactionType`, `payment_transaction`.`timestamp` FROM `payment_transaction` WHERE (`payment_transaction`.`status` = 'SUCCESS' AND `payment_transaction`.`timestamp` BETWEEN '{end_date}' AND '{start_date}')"
   
    df = pd.read_sql_query(v, conn)
 
    writer = pd.ExcelWriter(b, engine='openpyxl')
    df.to_excel(writer, sheet_name='Transactions')
    writer.save()
    response = HttpResponse(b.getvalue(), content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Report1.xls"'
    return response
def monthly_report(request):
    start_date= datetime.now()
    end_date = datetime.now() - relativedelta(months=1)
    v = f"SELECT `payment_transaction`.`id`, `payment_transaction`.`destacc`, `payment_transaction`.`service`, `payment_transaction`.`amount`, `payment_transaction`.`remarks`, `payment_transaction`.`referenceNo`, `payment_transaction`.`transactionType`, `payment_transaction`.`timestamp` FROM `payment_transaction` WHERE (`payment_transaction`.`status` = 'SUCCESS' AND `payment_transaction`.`timestamp` BETWEEN '{end_date}' AND '{start_date}')"
   
    df = pd.read_sql_query(v, conn)

    writer = pd.ExcelWriter(b, engine='openpyxl')
    df.to_excel(writer, sheet_name='Transactions')
    writer.save()
    response = HttpResponse(b.getvalue(), content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Report1.xls"'
    return response
def yearly_report(request):
    start_date= datetime.now()
    end_date = datetime.now() - relativedelta(years=1)
    v = f"SELECT `payment_transaction`.`id`, `payment_transaction`.`destacc`, `payment_transaction`.`service`, `payment_transaction`.`amount`, `payment_transaction`.`remarks`, `payment_transaction`.`referenceNo`, `payment_transaction`.`transactionType`, `payment_transaction`.`timestamp` FROM `payment_transaction` WHERE (`payment_transaction`.`status` = 'SUCCESS' AND `payment_transaction`.`timestamp` BETWEEN '{end_date}' AND '{start_date}')"
   
    df = pd.read_sql_query(v, conn)

    writer = pd.ExcelWriter(b, engine='openpyxl')
    df.to_excel(writer, sheet_name='Transactions')
    writer.save()
    response = HttpResponse(b.getvalue(), content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Report1.xls"'
    return response
#UNSUCCESSFUL TRANSACTIONS
def payables_unsuccessful_transactions_report_to_excel(request):
    v = str(PaymentTransaction.objects.filter(status="FAIL").values('id', 'destacc', 'service', 'amount', 'remarks',
                                                                  'referenceno', 'transactiontype', 'timestamp').query)
    df = pd.read_sql_query(v, conn)
    print(df)
    writer = pd.ExcelWriter(b, engine='openpyxl')
    df.to_excel(writer, sheet_name='Transactions')
    writer.save()
    response = HttpResponse(b.getvalue(), content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Report1.xls"'
    return response

def daily_report_unsuccessful(request):
    start_date= datetime.now()
    end_date = datetime.now() - timedelta(days=1)
    v = f"SELECT `payment_transaction`.`id`, `payment_transaction`.`destacc`, `payment_transaction`.`service`, `payment_transaction`.`amount`, `payment_transaction`.`remarks`, `payment_transaction`.`referenceNo`, `payment_transaction`.`transactionType`, `payment_transaction`.`timestamp` FROM `payment_transaction` WHERE (`payment_transaction`.`status` = 'FAIL' AND `payment_transaction`.`timestamp` BETWEEN '{end_date}' AND '{start_date}')"
    df = pd.read_sql_query(v, conn)

    writer = pd.ExcelWriter(b, engine='openpyxl')
    df.to_excel(writer, sheet_name='Transactions')
    writer.save()
    response = HttpResponse(b.getvalue(), content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Report1.xls"'
    return response
def weekly_report_unsuccessful(request):
    start_date= datetime.now()
    end_date = datetime.now() - timedelta(days=7)
    v = f"SELECT `payment_transaction`.`id`, `payment_transaction`.`destacc`, `payment_transaction`.`service`, `payment_transaction`.`amount`, `payment_transaction`.`remarks`, `payment_transaction`.`referenceNo`, `payment_transaction`.`transactionType`, `payment_transaction`.`timestamp` FROM `payment_transaction` WHERE (`payment_transaction`.`status` = 'FAIL' AND `payment_transaction`.`timestamp` BETWEEN '{end_date}' AND '{start_date}')"
    
    df = pd.read_sql_query(v, conn)

    writer = pd.ExcelWriter(b, engine='openpyxl')
    df.to_excel(writer, sheet_name='Transactions')
    writer.save()
    response = HttpResponse(b.getvalue(), content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Report1.xls"'
    return response
def monthly_report_unsuccessful(request):
    start_date= datetime.now()
    end_date = datetime.now() - relativedelta(months=1)
    v = f"SELECT `payment_transaction`.`id`, `payment_transaction`.`destacc`, `payment_transaction`.`service`, `payment_transaction`.`amount`, `payment_transaction`.`remarks`, `payment_transaction`.`referenceNo`, `payment_transaction`.`transactionType`, `payment_transaction`.`timestamp` FROM `payment_transaction` WHERE (`payment_transaction`.`status` = 'FAIL' AND `payment_transaction`.`timestamp` BETWEEN '{end_date}' AND '{start_date}')"
    
    df = pd.read_sql_query(v, conn)

    writer = pd.ExcelWriter(b, engine='openpyxl')
    df.to_excel(writer, sheet_name='Transactions')
    writer.save()
    response = HttpResponse(b.getvalue(), content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Report1.xls"'
    return response
def yearly_report_unsuccessful(request):
    start_date= datetime.now()
    end_date = datetime.now() - relativedelta(years=1)
    v = f"SELECT `payment_transaction`.`id`, `payment_transaction`.`destacc`, `payment_transaction`.`service`, `payment_transaction`.`amount`, `payment_transaction`.`remarks`, `payment_transaction`.`referenceNo`, `payment_transaction`.`transactionType`, `payment_transaction`.`timestamp` FROM `payment_transaction` WHERE (`payment_transaction`.`status` = 'FAIL' AND `payment_transaction`.`timestamp` BETWEEN '{end_date}' AND '{start_date}')"
    
    df = pd.read_sql_query(v, conn)

    writer = pd.ExcelWriter(b, engine='openpyxl')
    df.to_excel(writer, sheet_name='Transactions')
    writer.save()
    response = HttpResponse(b.getvalue(), content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Report1.xls"'
    return response"""

