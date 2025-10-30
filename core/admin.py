from django.contrib import admin
from .models import Lancamento, GaleriaImagem, Diferencial, HeroSection, SobreSection


class GaleriaImagemInline(admin.TabularInline):
    """Permite adicionar imagens da galeria diretamente na página do lançamento"""
    model = GaleriaImagem
    extra = 3
    fields = ['imagem', 'legenda', 'ordem']


@admin.register(Lancamento)
class LancamentoAdmin(admin.ModelAdmin):
    """Configuração do painel de administração para Lançamentos"""
    
    list_display = ['titulo', 'status', 'cidade', 'bairro', 'ativo', 'data_criacao']
    list_filter = ['status', 'cidade', 'ativo', 'data_criacao']
    search_fields = ['titulo', 'cidade', 'bairro', 'descricao_curta', 'descricao_completa']
    prepopulated_fields = {'slug': ('titulo',)}
    list_editable = ['ativo']
    date_hierarchy = 'data_criacao'
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'slug', 'status', 'ativo')
        }),
        ('Localização', {
            'fields': ('cidade', 'bairro')
        }),
        ('Descrições', {
            'fields': ('descricao_curta', 'descricao_completa')
        }),
        ('Imagem Principal', {
            'fields': ('imagem_principal',)
        }),
    )
    
    inlines = [GaleriaImagemInline]
    
    def get_readonly_fields(self, request, obj=None):
        """Define campos somente leitura após a criação"""
        if obj:  # Editando um objeto existente
            return ['data_criacao']
        return []


@admin.register(GaleriaImagem)
class GaleriaImagemAdmin(admin.ModelAdmin):
    """Configuração do painel de administração para Imagens da Galeria"""
    
    list_display = ['lancamento', 'legenda', 'ordem']
    list_filter = ['lancamento']
    search_fields = ['lancamento__titulo', 'legenda']
    list_editable = ['ordem']


@admin.register(Diferencial)
class DiferencialAdmin(admin.ModelAdmin):
    """Configuração do painel de administração para Diferenciais"""
    
    list_display = ['titulo', 'ordem', 'ativo']
    list_filter = ['ativo']
    search_fields = ['titulo', 'descricao']
    list_editable = ['ordem', 'ativo']
    
    fieldsets = (
        ('Informações', {
            'fields': ('titulo', 'descricao', 'ativo')
        }),
        ('Imagem', {
            'fields': ('imagem',)
        }),
        ('Ordenação', {
            'fields': ('ordem',)
        }),
    )


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    """Configuração do painel de administração para Hero Section"""
    
    list_display = ['titulo', 'ativo', 'data_atualizacao']
    list_filter = ['ativo', 'data_atualizacao']
    search_fields = ['titulo', 'subtitulo']
    
    fieldsets = (
        ('Textos', {
            'fields': ('titulo', 'subtitulo', 'texto_botao'),
            'description': 'Textos exibidos na seção principal do site'
        }),
        ('Imagem', {
            'fields': ('imagem_fundo',),
            'description': 'Imagem de fundo da Hero Section (recomendado: 1920x1080px)'
        }),
        ('Configurações', {
            'fields': ('ativo',),
            'description': 'Apenas uma Hero Section pode estar ativa por vez'
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Define campos somente leitura"""
        if obj:
            return ['data_atualizacao']
        return []


@admin.register(SobreSection)
class SobreSectionAdmin(admin.ModelAdmin):
    """Configuração do painel de administração para Seção Sobre"""
    
    list_display = ['titulo', 'nome_fundadora', 'nome_fundador', 'ativo', 'data_atualizacao']
    list_filter = ['ativo', 'data_atualizacao']
    search_fields = ['titulo', 'nome_fundadora', 'nome_fundador', 'texto_fundadora', 'texto_fundador']
    
    fieldsets = (
        ('Título da Seção', {
            'fields': ('titulo',),
            'description': 'Título principal da seção "Nossa História"'
        }),
        ('Fundadora - Camilla', {
            'fields': ('nome_fundadora', 'texto_fundadora', 'foto_fundadora'),
            'description': 'Informações sobre a fundadora'
        }),
        ('Fundador - Marlon', {
            'fields': ('nome_fundador', 'texto_fundador', 'foto_fundador'),
            'description': 'Informações sobre o fundador'
        }),
        ('Configurações', {
            'fields': ('ativo',),
            'description': 'Apenas uma Seção Sobre pode estar ativa por vez'
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Define campos somente leitura"""
        if obj:
            return ['data_atualizacao']
        return []
