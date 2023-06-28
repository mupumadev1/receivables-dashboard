from django.template.context_processors import static
from django.urls import path

from SageBankServiceDashboard import settings
from dashboard import views

app_name='dashboard'

urlpatterns = [
    #receivables

    path("dashboard/search/",views.search_results, name='s_t_results'),
    path("download", views.generate_report, name='excel-report'),
    path("dashboard/", views.recievables_successfull_trans, name='s_t')
]
