from django.db import models
from django.utils.text import slugify

# Modelo para gerenciar a seção CTA de investimento (após os imports)
class InvestmentCTASection(models.Model):
    """Modelo para gerenciar a seção CTA de investimento"""
    titulo = models.CharField('Título Principal', max_length=200, default='Sua próxima grande oportunidade')
    subtitulo = models.TextField('Subtítulo', default='Está pronto para transformar seu capital em um investimento imobiliário inteligente e altamente lucrativo? Nossa equipe está pronta para apresentar as melhores estratégias e oportunidades, baseadas em nossa profunda análise de mercado.')
    imagem_fundo = models.ImageField('Imagem de Fundo', upload_to='cta_investimento/', help_text='Imagem de fundo da seção (recomendado: 1920x800px)')
    texto_botao = models.CharField('Texto do Botão', max_length=100, default='Receber Análise Completa de Investimentos')
    link_botao = models.URLField('Link do Botão', default='https://api.whatsapp.com/send?phone=5577999106220&text=Ol%C3%A1!%20Gostaria%20de%20receber%20a%20An%C3%A1lise%20Completa%20de%20Investimentos.')
    ativo = models.BooleanField('Ativo', default=True, help_text='Apenas uma CTA pode estar ativa por vez')
    data_atualizacao = models.DateTimeField('Última Atualização', auto_now=True)

    class Meta:
        verbose_name = 'Chamada para Investimento (Home)'
        verbose_name_plural = 'Chamadas para Investimento (Home)'
        ordering = ['-ativo', '-data_atualizacao']

    def __str__(self):
        return f'CTA Investimento - {self.titulo[:50]}'

    def save(self, *args, **kwargs):
        if self.ativo:
            InvestmentCTASection.objects.filter(ativo=True).exclude(id=self.id).update(ativo=False)
        super().save(*args, **kwargs)

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
        verbose_name = 'Empreendimento / Lançamento'
        verbose_name_plural = 'Empreendimentos / Lançamentos'
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
    destaque_home = models.BooleanField('Exibir na página inicial?', default=False,
                                     help_text='Marque para exibir esta imagem na página inicial')
    
    class Meta:
        verbose_name = 'Imagem do Empreendimento'
        verbose_name_plural = 'Imagens dos Empreendimentos'
        ordering = ['ordem', 'id']
    
    def __str__(self):
        return f'{self.lancamento.titulo} - Imagem {self.id}'
        
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.destaque_home:
            # Conta quantas imagens já estão destacadas para este lançamento
            destacadas = GaleriaImagem.objects.filter(
                lancamento=self.lancamento,
                destaque_home=True
            ).exclude(id=self.id).count()
            
            if destacadas >= 3:
                raise ValidationError({
                    'destaque_home': 'Apenas 3 imagens podem ser selecionadas para exibição na página inicial.'
                })


class Diferencial(models.Model):
    """Modelo para diferenciais da Standart 7"""
    
    titulo = models.CharField('Título', max_length=200)
    descricao = models.TextField('Descrição',
                                 help_text='Texto explicativo do diferencial')
    imagem = models.ImageField('Imagem', upload_to='diferenciais/',
                               help_text='Imagem ilustrativa do diferencial')
    ordem = models.IntegerField('Ordem', default=0,
                                help_text='Define a ordem de exibição')
    texto_botao = models.CharField('Texto do Botão', max_length=100, blank=True, default='', help_text='Texto exibido no botão do diferencial')
    link_botao = models.URLField('Link do Botão', blank=True, default='', help_text='URL para onde o botão irá redirecionar')
    ativo = models.BooleanField('Ativo', default=True,
                                help_text='Define se o diferencial aparece no site')
    
    class Meta:
        verbose_name = 'Diferencial da Empresa'
        verbose_name_plural = 'Diferenciais da Empresa'
        ordering = ['ordem', 'id']
    
    def __str__(self):
        return self.titulo


class HeroSection(models.Model):
    """Modelo para gerenciar o conteúdo da Hero Section"""
    
    titulo = models.CharField('Título Principal', max_length=200,
                             default='Investimento Inteligente em Imóveis')
    texto_destaque = models.CharField('Texto de Destaque', max_length=100, blank=True,
                                     help_text='Texto em destaque entre o título e subtítulo (ex: "DE SUCESSO")')
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
        verbose_name = 'Banner Principal (Home)'
        verbose_name_plural = 'Banners Principais (Home)'
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
        verbose_name = 'Nossa História (Home)'
        verbose_name_plural = 'Nossa História (Home)'
        ordering = ['-ativo', '-data_atualizacao']
    
    def __str__(self):
        return f'Seção Sobre - {self.titulo}'
    
    def save(self, *args, **kwargs):
        """Garante que apenas uma Seção Sobre esteja ativa"""
        if self.ativo:
            SobreSection.objects.filter(ativo=True).exclude(id=self.id).update(ativo=False)
        super().save(*args, **kwargs)


class Depoimento(models.Model):
    """Modelo para depoimentos de clientes"""
    
    nome = models.CharField('Nome do Cliente', max_length=200)
    foto = models.ImageField('Foto do Cliente', upload_to='depoimentos/',
                            help_text='Foto do cliente (recomendado: 300x300px)')
    conteudo = models.TextField('Depoimento',
                                help_text='Texto do depoimento do cliente')
    ordem = models.IntegerField('Ordem', default=0,
                               help_text='Define a ordem de exibição dos depoimentos')
    ativo = models.BooleanField('Ativo', default=True,
                                help_text='Define se o depoimento aparece no site')
    data_criacao = models.DateTimeField('Data de Criação', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Depoimento de Cliente'
        verbose_name_plural = 'Depoimentos de Clientes'
        ordering = ['ordem', '-data_criacao']
    
    def __str__(self):
        return f'Depoimento - {self.nome}'


class LancamentosHero(models.Model):
    """Modelo para gerenciar o background hero da página de lançamentos"""
    
    titulo = models.CharField('Título', max_length=200, default='Nossos Empreendimentos')
    subtitulo = models.CharField('Subtítulo', max_length=300, 
                                default='Conheça os lançamentos e oportunidades disponíveis')
    imagem_fundo = models.ImageField('Imagem de Fundo', upload_to='hero/',
                                     help_text='Imagem de fundo da seção hero (recomendado: 1920x1080px)')
    opacidade = models.IntegerField('Opacidade do Overlay Branco (%)', default=60,
                                   help_text='Opacidade da camada BRANCA sobre a imagem (0=transparente, 100=branco total)')
    ativo = models.BooleanField('Ativo', default=True,
                                help_text='Apenas um hero pode estar ativo por vez')
    data_criacao = models.DateTimeField('Data de Criação', auto_now_add=True)
    data_atualizacao = models.DateTimeField('Última Atualização', auto_now=True)
    
    class Meta:
        verbose_name = 'Banner da Página Lançamentos'
        verbose_name_plural = 'Banners da Página Lançamentos'
        ordering = ['-ativo', '-data_atualizacao']
    
    def __str__(self):
        return f'{self.titulo} - {"Ativo" if self.ativo else "Inativo"}'
    
    def save(self, *args, **kwargs):
        """Garante que apenas um hero esteja ativo por vez"""
        if self.ativo:
            LancamentosHero.objects.filter(ativo=True).exclude(id=self.id).update(ativo=False)
        super().save(*args, **kwargs)
    
    def clean(self):
        """Validação personalizada"""
        from django.core.exceptions import ValidationError
        if self.opacidade < 0 or self.opacidade > 100:
            raise ValidationError({'opacidade': 'A opacidade deve estar entre 0 e 100.'})


class LancamentosVideo(models.Model):
    """Modelo para gerenciar o vídeo da página HOME"""
    
    titulo = models.CharField('Título da Seção', max_length=200, blank=True,
                             default='Conheça Nossos Empreendimentos')
    video_arquivo = models.FileField('Arquivo de Vídeo', upload_to='videos/', blank=True, null=True,
                                    help_text='Formatos suportados: MP4, WebM, OGG, MOV')
    texto_botao = models.CharField('Texto do Botão WhatsApp', max_length=100,
                                  default='Falar com Especialista')
    link_whatsapp = models.URLField('Link do WhatsApp',
                                   default='https://wa.me/5577999106220?text=Ol%C3%A1%2C%20gostaria%20de%20saber%20mais%20sobre%20os%20lan%C3%A7amentos.',
                                   help_text='Link do WhatsApp com mensagem pré-definida')
    ativo = models.BooleanField('Ativo', default=True,
                                help_text='Apenas um vídeo pode estar ativo por vez')
    autoplay = models.BooleanField('Reprodução Automática', default=True,
                                   help_text='Iniciar vídeo automaticamente quando entrar na página')
    data_criacao = models.DateTimeField('Data de Criação', auto_now_add=True)
    data_atualizacao = models.DateTimeField('Última Atualização', auto_now=True)
    
    class Meta:
        verbose_name = 'Vídeo da Página Home'
        verbose_name_plural = 'Vídeos da Página Home'
        ordering = ['-ativo', '-data_atualizacao']
    
    def __str__(self):
        return f'{self.titulo} - {"Ativo" if self.ativo else "Inativo"}'
    
    def save(self, *args, **kwargs):
        """Garante que apenas um vídeo esteja ativo por vez"""
        if self.ativo:
            LancamentosVideo.objects.filter(ativo=True).exclude(id=self.id).update(ativo=False)
        super().save(*args, **kwargs)
