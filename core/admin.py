from django.contrib import admin
from .models import InvestmentCTASection, Lancamento, GaleriaImagem, Diferencial, HeroSection, SobreSection, Depoimento, LancamentosHero, LancamentosVideo


# Configuração do Admin Site - Nomes amigáveis
admin.site.site_header = 'Administração Standart 7'
admin.site.site_title = 'Standart 7'
admin.site.index_title = 'Painel de Gerenciamento do Site'

@admin.register(InvestmentCTASection)
class InvestmentCTASectionAdmin(admin.ModelAdmin):
    """Admin para a seção CTA de investimento"""
    list_display = ['titulo', 'ativo', 'data_atualizacao']
    list_filter = ['ativo', 'data_atualizacao']
    search_fields = ['titulo', 'subtitulo']

    fieldsets = (
        ('Textos da Chamada', {
            'fields': ('titulo', 'subtitulo', 'texto_botao', 'link_botao'),
            'description': 'Textos e botão da seção de chamada para investimento'
        }),
        ('Imagem de Fundo', {
            'fields': ('imagem_fundo',),
            'description': 'Imagem de fundo da seção (recomendado: 1920x800px)'
        }),
        ('Status', {
            'fields': ('ativo',),
            'description': 'Apenas uma seção pode estar ativa por vez'
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['data_atualizacao']
        return []
    
    class Meta:
        verbose_name = 'Chamada para Investimento (Home)'
        verbose_name_plural = 'Chamadas para Investimento (Home)'
from django.contrib import admin
from .models import Lancamento, GaleriaImagem, Diferencial, HeroSection, SobreSection, Depoimento, LancamentosHero


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
        ('Botão', {
            'fields': ('texto_botao', 'link_botao')
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


@admin.register(Depoimento)
class DepoimentoAdmin(admin.ModelAdmin):
    """Configuração do painel de administração para Depoimentos"""
    
    list_display = ['nome', 'ordem', 'ativo', 'data_criacao']
    list_filter = ['ativo', 'data_criacao']
    search_fields = ['nome', 'conteudo']
    list_editable = ['ordem', 'ativo']
    date_hierarchy = 'data_criacao'
    
    fieldsets = (
        ('Informações do Cliente', {
            'fields': ('nome', 'foto'),
            'description': 'Nome e foto do cliente'
        }),
        ('Depoimento', {
            'fields': ('conteudo',),
            'description': 'Texto do depoimento'
        }),
        ('Configurações', {
            'fields': ('ordem', 'ativo'),
            'description': 'Ordem de exibição e status'
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Define campos somente leitura"""
        if obj:
            return ['data_criacao']
        return []


@admin.register(LancamentosHero)
class LancamentosHeroAdmin(admin.ModelAdmin):
    """Admin para o Hero da página de lançamentos"""
    list_display = ['titulo', 'opacidade', 'ativo', 'data_atualizacao']
    list_filter = ['ativo', 'data_atualizacao']
    search_fields = ['titulo', 'subtitulo']
    list_editable = ['ativo']
    
    fieldsets = (
        ('Textos', {
            'fields': ('titulo', 'subtitulo'),
            'description': 'Título e subtítulo exibidos no hero'
        }),
        ('Imagem de Fundo', {
            'fields': ('imagem_fundo',),
            'description': 'Imagem de fundo do hero (recomendado: 1920x1080px para tela cheia)'
        }),
        ('Configurações Visuais', {
            'fields': ('opacidade',),
            'description': 'Opacidade do overlay BRANCO sobre a imagem (0=transparente/imagem visível, 100=branco total)'
        }),
        ('Status', {
            'fields': ('ativo',),
            'description': 'Apenas um hero pode estar ativo por vez'
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Define campos somente leitura"""
        if obj:
            return ['data_criacao', 'data_atualizacao']
        return []


@admin.register(LancamentosVideo)
class LancamentosVideoAdmin(admin.ModelAdmin):
    """Admin para o Vídeo da página HOME"""
    list_display = ['titulo', 'ativo', 'autoplay', 'data_atualizacao']
    list_filter = ['ativo', 'autoplay', 'data_atualizacao']
    search_fields = ['titulo']
    list_editable = ['ativo', 'autoplay']
    
    fieldsets = (
        ('Conteúdo do Vídeo', {
            'fields': ('titulo', 'video_arquivo', 'autoplay'),
            'description': 'Faça upload do arquivo de vídeo (MP4, MOV, WebM, OGG)'
        }),
        ('Botão WhatsApp', {
            'fields': ('texto_botao', 'link_whatsapp'),
            'description': 'Botão de contato exibido abaixo do vídeo'
        }),
        ('Status', {
            'fields': ('ativo',),
            'description': 'Apenas um vídeo pode estar ativo por vez'
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Define campos somente leitura"""
        if obj:
            return ['data_criacao', 'data_atualizacao']
        return []
