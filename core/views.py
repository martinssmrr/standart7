from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db import models
from .models import Lancamento, Diferencial, HeroSection, SobreSection, GaleriaImagem, Depoimento, LancamentosHero, LancamentosVideo


class HomeView(ListView):
    """View da página inicial - exibe diferenciais"""
    model = Diferencial
    template_name = 'core/home.html'
    context_object_name = 'diferenciais'
    
    def get_queryset(self):
        """Retorna apenas os diferenciais ativos"""
        return Diferencial.objects.filter(ativo=True)
    
    def get_context_data(self, **kwargs):
        """Adiciona Hero Section, Seção Sobre, CTA Investimento, Depoimentos e Vídeo ao contexto"""
        context = super().get_context_data(**kwargs)
        context['hero'] = HeroSection.objects.filter(ativo=True).first()
        context['sobre'] = SobreSection.objects.filter(ativo=True).first()
        context['depoimentos'] = Depoimento.objects.filter(ativo=True)
        context['home_video'] = LancamentosVideo.objects.filter(ativo=True).first()
        from .models import InvestmentCTASection
        context['cta_investimento'] = InvestmentCTASection.objects.filter(ativo=True).first()
        return context


class LancamentoDetailView(DetailView):
    """View de detalhes de um lançamento específico"""
    model = Lancamento
    template_name = 'lancamentos/lancamento_detail.html'
    context_object_name = 'lancamento'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        """Retorna apenas lançamentos ativos com imagens da galeria"""
        return Lancamento.objects.filter(ativo=True).prefetch_related('galeria_imagens')


class LancamentosListView(ListView):
    """View da página de lançamentos"""
    model = Lancamento
    # Usamos um template limpo novo para evitar problemas com o arquivo anterior corrompido
    template_name = 'core/lancamentos_clean.html'
    context_object_name = 'lancamentos'
    
    def get_queryset(self):
        """Retorna apenas lançamentos ativos com suas imagens da galeria"""
        return Lancamento.objects.filter(ativo=True).prefetch_related(
            models.Prefetch(
                'galeria_imagens',
                queryset=GaleriaImagem.objects.filter(destaque_home=True).order_by('ordem')
            )
        )
    
    def get_context_data(self, **kwargs):
        """Adiciona o hero ao contexto"""
        context = super().get_context_data(**kwargs)
        context['lancamentos_hero'] = LancamentosHero.objects.filter(ativo=True).first()
        return context
