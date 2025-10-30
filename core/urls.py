from django.urls import path
from .views import HomeView, LancamentoDetailView, DiferenciaisView

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('lancamentos/<slug:slug>/', LancamentoDetailView.as_view(), name='lancamento_detail'),
    path('diferenciais/', DiferenciaisView.as_view(), name='diferenciais'),
]
