from django.template.context_processors import static
from django.urls import path

from SageBankServiceDashboard import settings
from dashboard import views

app_name='dashboard'

urlpatterns = [
    path("",views.receivables_index,name='home'),
    #receivables
    path("by_date_form/", views.by_date_form, name='by_date_form'),
    path("by_field_form/", views.by_field_form, name='by_field_form'),
    path("receivables_transactions/search_results/",views.successful_transactions_results, name='s_t_results'),
    path("receivables_transactions/search_field_results/",views.successful_receivables_by_field, name='s_t_results_field'),
    path("receivables_transactions/search_field_results/xls/",views.successful_receivables_by_field_report, name='s_t_field_export'),
    path("receivables_transactions/",views.receivables_index,name='receivables_homepage'),
    path("successful/<int:page>/", views.recievables_successfull_trans, name='s_t'),
    path("successful_transactions_xls/all/", views.successful_transactions_report_to_excel, name='s_excel'),
    path("successful_transactions_xls/by_date/", views.successful_receivables_date_report, name='s_excel_by_date'),
    path("unsuccessful/<int:page>/", views.receivables_unsuccessfull_trans, name='u_t'),
    path("unsuccessful_transactions/search_field_results/",views.unsuccessful_receivables_by_field, name='u_t_results_field'),
    path("unsuccesful_transactions_xls/", views.unsuccessful_transactions_report_to_excel, name='u_excel'),
    path("unsuccessful_transactions_xls/by_date/", views.unsuccessful_receivables_date_report, name='u_excel_by_date'),
    path("unsuccessful_transactions/search_results/",views.unsuccessful_transactions_results, name='u_t_results'),
    path("unsuccessful_transactions/search_field_results/",views.unsuccessful_receivables_by_field_report, name='u_t_results_field_export'),
    path("unsuccessful_transactions/search_field_results/xls/",views.unsuccessful_receivables_by_field_report, name='u_t_field_export'),
    path("duplicates/<int:page>/", views.duplicates, name='d_t'),
    path("duplicate_transactions_xls", views.duplicate_transactions_report_to_excel, name='d_excel'),
    path("duplicate_transactions_xls/by_date/", views.duplicate_receivables_date_report, name='d_excel_by_date'),
    path("duplicate_transactions/search_results/",views.duplicate_transactions_results, name='d_t_results'),
    path("duplicate_transactions/search_field_results/",views.duplicate_receivables_by_field, name='d_t_results_field'),
    
    path("duplicate_transactions/search_field_results_xls/",views.duplicate_receivables_by_field_report, name='d_t_field_export')]
"""payables
    path("payables_transactions/",views.payables_index,name='payables_homepage'),
    path("payables_successful/<int:page>/", views.payables_successfull_trans, name='p_s_t'),
    path("payables_unsuccessful/<int:page>/", views.payables_unsuccessfull_trans, name='p_u_t'),
    path("payments_successful_transactions_xls", views.payables_successful_transactions_report_to_excel, name='p_s_excel'),
    path("payments_successful_transactions_xls/daily/", views.daily_report, name='p_excel_daily'),
    path("payments_successful_transactions_xls/weekly/", views.weekly_report, name='p_excel_weekly'),
    path("payments_successful_transactions_xls/monthly/", views.monthly_report, name='p_excel_monthly'),
    path("payments_successful_transactions_xls/yearly/", views.yearly_report, name='p_excel_yearly'),
    path("payments_unsuccessful_transactions_xls", views.payables_unsuccessful_transactions_report_to_excel, name='p_u_excel'),
    path("payments_unsuccessful_transactions_xls/daily/", views.daily_report_unsuccessful, name='p_u_excel_daily'),
    path("payments_unsuccessful_transactions_xls/weekly/", views.weekly_report_unsuccessful, name='p_u_excel_weekly'),
    path("payments_unsuccessful_transactions_xls/monthly/", views.monthly_report_unsuccessful, name='p_u_excel_monthly'),
    path("payments_unsuccessful_transactions_xls/yearly/", views.yearly_report_unsuccessful, name='p_u_excel_yearly')"""

    