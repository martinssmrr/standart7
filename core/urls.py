from django.urls import path
from .views import HomeView, LancamentoDetailView, LancamentosListView

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('lancamento/<slug:slug>/', LancamentoDetailView.as_view(), name='lancamento_detail'),
    path('lancamentos/', LancamentosListView.as_view(), name='lancamentos'),
]
