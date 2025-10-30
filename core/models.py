from django.db import models
from django.utils.text import slugify


class Lancamento(models.Model):
    """Modelo para representar um empreendimento imobiliário"""
    
    STATUS_CHOICES = [
        ('breve', 'Breve Lançamento'),
        ('obras', 'Em Obras'),
        ('pronto', 'Pronto para Morar'),
    ]
    
    titulo = models.CharField('Título', max_length=200)
    slug = models.SlugField('Slug', unique=True, max_length=200, blank=True)
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='breve')
    cidade = models.CharField('Cidade', max_length=100)
    bairro = models.CharField('Bairro', max_length=100)
    descricao_curta = models.CharField('Descrição Curta', max_length=250, 
                                       help_text='Chamada rápida exibida nos cards da home')
    descricao_completa = models.TextField('Descrição Completa',
                                          help_text='Texto detalhado para a página de detalhes')
    imagem_principal = models.ImageField('Imagem Principal', upload_to='lancamentos/', 
                                         help_text='Banner ou foto de capa')
    data_criacao = models.DateTimeField('Data de Criação', auto_now_add=True)
    ativo = models.BooleanField('Ativo', default=True, 
                                help_text='Define se o lançamento aparece no site')
    
    class Meta:
        verbose_name = 'Lançamento'
        verbose_name_plural = 'Lançamentos'
        ordering = ['-data_criacao']
    
    def __str__(self):
        return self.titulo
    
    def save(self, *args, **kwargs):
        """Gera o slug automaticamente a partir do título se não existir"""
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)


class GaleriaImagem(models.Model):
    """Modelo para galeria de imagens de um lançamento"""
    
    lancamento = models.ForeignKey(Lancamento, on_delete=models.CASCADE, 
                                   related_name='galeria_imagens',
                                   verbose_name='Lançamento')
    imagem = models.ImageField('Imagem', upload_to='lancamentos/galeria/')
    legenda = models.CharField('Legenda', max_length=200, blank=True)
    ordem = models.IntegerField('Ordem', default=0,
                                help_text='Define a ordem de exibição das imagens')
    
    class Meta:
        verbose_name = 'Imagem da Galeria'
        verbose_name_plural = 'Imagens da Galeria'
        ordering = ['ordem', 'id']
    
    def __str__(self):
        return f'{self.lancamento.titulo} - Imagem {self.id}'


class Diferencial(models.Model):
    """Modelo para diferenciais da Standart 7"""
    
    titulo = models.CharField('Título', max_length=200)
    descricao = models.TextField('Descrição',
                                 help_text='Texto explicativo do diferencial')
    imagem = models.ImageField('Imagem', upload_to='diferenciais/',
                               help_text='Imagem ilustrativa do diferencial')
    ordem = models.IntegerField('Ordem', default=0,
                                help_text='Define a ordem de exibição')
    ativo = models.BooleanField('Ativo', default=True,
                                help_text='Define se o diferencial aparece no site')
    
    class Meta:
        verbose_name = 'Diferencial'
        verbose_name_plural = 'Diferenciais'
        ordering = ['ordem', 'id']
    
    def __str__(self):
        return self.titulo


class HeroSection(models.Model):
    """Modelo para gerenciar o conteúdo da Hero Section"""
    
    titulo = models.CharField('Título Principal', max_length=200,
                             default='Investimento Inteligente em Imóveis')
    subtitulo = models.CharField('Subtítulo', max_length=300,
                                default='Transforme seu capital em patrimônio com segurança e rentabilidade')
    texto_botao = models.CharField('Texto do Botão', max_length=100,
                                  default='Consultoria Especializada')
    imagem_fundo = models.ImageField('Imagem de Fundo', upload_to='hero/',
                                     help_text='Imagem de fundo da seção principal (recomendado: 1920x1080px)')
    ativo = models.BooleanField('Ativo', default=True,
                               help_text='Apenas uma Hero Section pode estar ativa por vez')
    data_atualizacao = models.DateTimeField('Última Atualização', auto_now=True)
    
    class Meta:
        verbose_name = 'Hero Section'
        verbose_name_plural = 'Hero Sections'
        ordering = ['-ativo', '-data_atualizacao']
    
    def __str__(self):
        return f'Hero Section - {self.titulo[:50]}'
    
    def save(self, *args, **kwargs):
        """Garante que apenas uma Hero Section esteja ativa"""
        if self.ativo:
            HeroSection.objects.filter(ativo=True).exclude(id=self.id).update(ativo=False)
        super().save(*args, **kwargs)


class SobreSection(models.Model):
    """Modelo para gerenciar o conteúdo da Seção Sobre (Nossa História)"""
    
    titulo = models.CharField('Título da Seção', max_length=200,
                             default='Nossa História')
    
    # Camila
    nome_fundadora = models.CharField('Nome da Fundadora', max_length=100,
                                     default='Camilla Daianne')
    texto_fundadora = models.TextField('Texto sobre a Fundadora',
                                      help_text='Parágrafo sobre Camilla Daianne')
    foto_fundadora = models.ImageField('Foto da Fundadora', upload_to='sobre/',
                                       help_text='Foto de Camilla (recomendado: 500x500px)')
    
    # Marlon
    nome_fundador = models.CharField('Nome do Fundador', max_length=100,
                                    default='Marlon Deivison')
    texto_fundador = models.TextField('Texto sobre o Fundador',
                                     help_text='Parágrafo sobre Marlon Deivison')
    foto_fundador = models.ImageField('Foto do Fundador', upload_to='sobre/',
                                      help_text='Foto de Marlon (recomendado: 500x500px)')
    
    ativo = models.BooleanField('Ativo', default=True,
                               help_text='Apenas uma Seção Sobre pode estar ativa por vez')
    data_atualizacao = models.DateTimeField('Última Atualização', auto_now=True)
    
    class Meta:
        verbose_name = 'Seção Sobre (Nossa História)'
        verbose_name_plural = 'Seções Sobre (Nossa História)'
        ordering = ['-ativo', '-data_atualizacao']
    
    def __str__(self):
        return f'Seção Sobre - {self.titulo}'
    
    def save(self, *args, **kwargs):
        """Garante que apenas uma Seção Sobre esteja ativa"""
        if self.ativo:
            SobreSection.objects.filter(ativo=True).exclude(id=self.id).update(ativo=False)
        super().save(*args, **kwargs)
