from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Lancamento, Diferencial, HeroSection, SobreSection


class HomeView(ListView):
    """View da página inicial - lista todos os lançamentos ativos"""
    model = Lancamento
    template_name = 'core/home.html'
    context_object_name = 'lancamentos'
    
    def get_queryset(self):
        """Retorna apenas os lançamentos ativos com suas imagens da galeria"""
        return Lancamento.objects.filter(ativo=True).prefetch_related('galeria_imagens')
    
    def get_context_data(self, **kwargs):
        """Adiciona Hero Section e Seção Sobre ao contexto"""
        context = super().get_context_data(**kwargs)
        context['hero'] = HeroSection.objects.filter(ativo=True).first()
        context['sobre'] = SobreSection.objects.filter(ativo=True).first()
        return context


class LancamentoDetailView(DetailView):
    """View de detalhes de um lançamento específico"""
    model = Lancamento
    template_name = 'lancamentos/lancamento_detail.html'
    context_object_name = 'lancamento'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        """Retorna apenas lançamentos ativos"""
        return Lancamento.objects.filter(ativo=True)


class DiferenciaisView(ListView):
    """View da página de diferenciais"""
    model = Diferencial
    template_name = 'core/diferenciais.html'
    context_object_name = 'diferenciais'
    
    def get_queryset(self):
        """Retorna apenas diferenciais ativos ordenados"""
        return Diferencial.objects.filter(ativo=True)
