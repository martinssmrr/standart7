# 📋 Documentação Técnica - Standart 7

## Arquitetura do Sistema

### Estrutura MVT (Model-View-Template) do Django

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Browser   │─────▶│    URLs     │─────▶│    Views    │
│             │      │  routing    │      │  (logic)    │
└─────────────┘      └─────────────┘      └─────────────┘
      ▲                                           │
      │                                           ▼
      │                                    ┌─────────────┐
      │                                    │   Models    │
      │                                    │ (database)  │
      │                                    └─────────────┘
      │                                           │
      │                                           ▼
      │                                    ┌─────────────┐
      └────────────────────────────────────│  Templates  │
                                           │   (HTML)    │
                                           └─────────────┘
```

## Modelos de Dados

### Modelo Lancamento

```python
class Lancamento(models.Model):
    # Campos de texto
    titulo = CharField(max_length=200)                  # Obrigatório
    slug = SlugField(unique=True, blank=True)           # Auto-gerado
    descricao_curta = CharField(max_length=250)         # Obrigatório
    descricao_completa = TextField()                    # Obrigatório
    
    # Campos de escolha
    status = CharField(choices=STATUS_CHOICES)          # breve/obras/pronto
    
    # Localização
    cidade = CharField(max_length=100)                  # Obrigatório
    bairro = CharField(max_length=100)                  # Obrigatório
    
    # Mídia
    imagem_principal = ImageField(upload_to='lancamentos/')
    
    # Metadata
    data_criacao = DateTimeField(auto_now_add=True)     # Auto-preenchido
    ativo = BooleanField(default=True)                  # Controle de visibilidade
```

**Relacionamentos:**
- One-to-Many com `GaleriaImagem` (via ForeignKey reversa `galeria_imagens`)

### Modelo GaleriaImagem

```python
class GaleriaImagem(models.Model):
    lancamento = ForeignKey(Lancamento)                 # Relacionamento
    imagem = ImageField(upload_to='lancamentos/galeria/')
    legenda = CharField(max_length=200, blank=True)     # Opcional
    ordem = IntegerField(default=0)                     # Para ordenação
```

**Relacionamentos:**
- Many-to-One com `Lancamento`

## Views

### HomeView (ListView)

**Tipo**: Class-Based View (ListView)  
**URL**: `/`  
**Template**: `core/home.html`  
**Contexto**: `lancamentos` (lista de objetos Lancamento)

```python
def get_queryset(self):
    return Lancamento.objects.filter(ativo=True)
```

**Query SQL gerada:**
```sql
SELECT * FROM core_lancamento 
WHERE ativo = 1 
ORDER BY data_criacao DESC;
```

### LancamentoDetailView (DetailView)

**Tipo**: Class-Based View (DetailView)  
**URL**: `/lancamentos/<slug:slug>/`  
**Template**: `lancamentos/lancamento_detail.html`  
**Contexto**: `lancamento` (objeto único)

```python
def get_queryset(self):
    return Lancamento.objects.filter(ativo=True)
```

**Query SQL gerada:**
```sql
SELECT * FROM core_lancamento 
WHERE ativo = 1 AND slug = 'slug-do-lancamento';

SELECT * FROM core_galeriaimagem 
WHERE lancamento_id = ? 
ORDER BY ordem, id;
```

## URLs

### Configuração de Rotas

**standart7/urls.py** (URLs principais):
```python
urlpatterns = [
    path("admin/", admin.site.urls),          # Painel admin
    path("", include('core.urls')),           # Inclui URLs do core
]
```

**core/urls.py** (URLs da aplicação):
```python
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('lancamentos/<slug:slug>/', LancamentoDetailView.as_view(), name='lancamento_detail'),
]
```

### Exemplos de URLs Geradas

```
/                                    → HomeView
/lancamentos/residencial-chicago/    → LancamentoDetailView (slug='residencial-chicago')
/lancamentos/condominio-riviera/     → LancamentoDetailView (slug='condominio-riviera')
/admin/                              → Django Admin
/admin/core/lancamento/              → Lista de Lançamentos
/admin/core/lancamento/1/change/     → Editar Lançamento #1
/media/lancamentos/foto.jpg          → Arquivo de mídia
```

## Templates

### Hierarquia de Templates

```
base.html (estrutura principal)
├── core/home.html (página inicial)
└── lancamentos/lancamento_detail.html (detalhes)
```

### Template Tags Usadas

**URLs dinâmicas:**
```django
{% url 'core:home' %}
{% url 'core:lancamento_detail' lancamento.slug %}
```

**Arquivos estáticos:**
```django
{% load static %}
<img src="{% static 'img/logo.png' %}">
```

**Arquivos de mídia:**
```django
<img src="{{ lancamento.imagem_principal.url }}">
```

**Loops e condicionais:**
```django
{% for lancamento in lancamentos %}
    {% if lancamento.imagem_principal %}
        <img src="{{ lancamento.imagem_principal.url }}">
    {% else %}
        <div class="placeholder"></div>
    {% endif %}
{% endfor %}
```

**Display de choices:**
```django
{{ lancamento.get_status_display }}  {# Mostra "Em Obras" ao invés de "obras" #}
```

## Admin

### Customizações Implementadas

**LancamentoAdmin:**
- `list_display`: Colunas mostradas na listagem
- `list_filter`: Filtros laterais (status, cidade, ativo, data)
- `search_fields`: Campos incluídos na busca
- `prepopulated_fields`: Slug gerado automaticamente do título
- `list_editable`: Campos editáveis na listagem (ativo)
- `date_hierarchy`: Navegação por data
- `fieldsets`: Organização dos campos em seções
- `inlines`: Permite editar GaleriaImagem junto com Lancamento

**GaleriaImagemAdmin:**
- `list_display`: lancamento, legenda, ordem
- `list_filter`: Por lançamento
- `list_editable`: Ordem editável na listagem

## Banco de Dados

### Esquema (SQLite)

**Tabela: core_lancamento**
```sql
CREATE TABLE core_lancamento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo VARCHAR(200) NOT NULL,
    slug VARCHAR(200) UNIQUE NOT NULL,
    status VARCHAR(20) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    bairro VARCHAR(100) NOT NULL,
    descricao_curta VARCHAR(250) NOT NULL,
    descricao_completa TEXT NOT NULL,
    imagem_principal VARCHAR(100),
    data_criacao DATETIME NOT NULL,
    ativo BOOLEAN NOT NULL
);
```

**Tabela: core_galeriaimagem**
```sql
CREATE TABLE core_galeriaimagem (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lancamento_id INTEGER NOT NULL,
    imagem VARCHAR(100) NOT NULL,
    legenda VARCHAR(200),
    ordem INTEGER NOT NULL,
    FOREIGN KEY (lancamento_id) REFERENCES core_lancamento(id)
);
```

### Índices Criados Automaticamente

- Primary keys em ambas tabelas
- Unique index em `core_lancamento.slug`
- Foreign key index em `core_galeriaimagem.lancamento_id`

## Arquivos de Mídia

### Estrutura de Upload

```
media/
└── lancamentos/
    ├── foto1.jpg              # Imagens principais
    ├── foto2.jpg
    └── galeria/
        ├── foto1_gallery1.jpg # Imagens da galeria
        ├── foto1_gallery2.jpg
        └── ...
```

### Configuração (settings.py)

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### Servir em Desenvolvimento (urls.py)

```python
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

**⚠️ IMPORTANTE:** Em produção, use Nginx ou servidor web para servir mídia.

## Arquivos Estáticos

### Estrutura

```
static/
├── css/
│   └── custom.css (não usado, TailwindCSS via CDN)
└── img/
    └── (logos, ícones, etc.)
```

### Configuração (settings.py)

```python
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / 'static']
```

## TailwindCSS

### Classes Principais Usadas

**Layout:**
- `container mx-auto px-4`: Container centralizado
- `grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3`: Grid responsivo
- `flex items-center justify-between`: Flexbox

**Cores:**
- `bg-blue-600`: Fundo azul (primária)
- `text-gray-700`: Texto cinza
- `bg-gradient-to-r from-blue-600 to-blue-800`: Gradiente

**Espaçamento:**
- `py-16`: Padding vertical (4rem)
- `mb-8`: Margin bottom (2rem)
- `space-y-6`: Espaçamento vertical entre filhos

**Efeitos:**
- `hover:shadow-xl`: Sombra no hover
- `transition`: Transição suave
- `transform hover:-translate-y-2`: Mover para cima no hover

**Responsividade:**
- `md:`: Tablet (768px+)
- `lg:`: Desktop (1024px+)

## Fluxo de Dados

### Exemplo: Listar Lançamentos

1. **Usuário acessa** `/`
2. **Django** roteia para `HomeView`
3. **View** executa `get_queryset()`:
   ```python
   Lancamento.objects.filter(ativo=True)
   ```
4. **ORM Django** gera SQL:
   ```sql
   SELECT * FROM core_lancamento WHERE ativo = 1
   ```
5. **SQLite** retorna resultados
6. **View** passa `lancamentos` para template
7. **Template** renderiza HTML com loop:
   ```django
   {% for lancamento in lancamentos %}
       <div class="card">...</div>
   {% endfor %}
   ```
8. **Django** retorna HTML completo
9. **Navegador** renderiza página

## Segurança

### Proteções Ativas (Django padrão)

✅ **CSRF Protection**: Token em formulários  
✅ **SQL Injection**: ORM sanitiza queries  
✅ **XSS Protection**: Auto-escape em templates  
✅ **Clickjacking Protection**: X-Frame-Options header  
✅ **HTTPS**: Force SSL (para produção)

### Configurações de Segurança (settings.py)

```python
SECRET_KEY = "..." # Mudar em produção!
DEBUG = True       # False em produção!
ALLOWED_HOSTS = [] # Definir em produção!
```

## Performance

### Queries Otimizadas

**Problema N+1**: Ao listar lançamentos, cada imagem gera uma query.

**Solução**: Usar `select_related()` ou `prefetch_related()`:
```python
Lancamento.objects.filter(ativo=True).prefetch_related('galeria_imagens')
```

### Cache (não implementado)

Para implementar cache:
```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # Cache por 15 minutos
def home(request):
    ...
```

## Migrações

### Histórico de Migrações

```
core/migrations/
└── 0001_initial.py  # Cria Lancamento e GaleriaImagem
```

### Comandos

```bash
# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Ver SQL de uma migração
python manage.py sqlmigrate core 0001

# Reverter migração
python manage.py migrate core zero
```

## Testes (não implementados)

### Exemplo de teste a implementar:

```python
# core/tests.py
from django.test import TestCase
from .models import Lancamento

class LancamentoTestCase(TestCase):
    def test_slug_generation(self):
        lancamento = Lancamento.objects.create(
            titulo="Residencial Teste",
            status="breve",
            cidade="São Paulo",
            bairro="Centro",
            descricao_curta="Teste",
            descricao_completa="Teste completo"
        )
        self.assertEqual(lancamento.slug, "residencial-teste")
```

## Deploy (Produção)

### Checklist para Deploy

- [ ] Alterar `SECRET_KEY`
- [ ] `DEBUG = False`
- [ ] Configurar `ALLOWED_HOSTS`
- [ ] Usar PostgreSQL/MySQL
- [ ] Configurar servidor WSGI (Gunicorn)
- [ ] Configurar Nginx para servir static/media
- [ ] Configurar HTTPS (Let's Encrypt)
- [ ] Configurar backup do banco
- [ ] Configurar logs
- [ ] Executar `collectstatic`

### Exemplo de Deploy com Gunicorn

```bash
pip install gunicorn
gunicorn standart7.wsgi:application --bind 0.0.0.0:8000
```

## Extensões Futuras

### Sugestões de Melhorias

1. **Sistema de Busca**: Buscar por cidade, bairro, status
2. **Filtros na Home**: Filtrar lançamentos por critérios
3. **Mapa Interativo**: Mostrar localização no Google Maps
4. **Formulário Funcional**: Enviar emails de contato
5. **Newsletter**: Sistema de cadastro de interessados
6. **Blog**: Notícias imobiliárias
7. **Comparador**: Comparar até 3 lançamentos
8. **Calculadora**: Simulador de financiamento
9. **Tours Virtuais**: Integração com Matterport
10. **API REST**: Expor dados via API (Django REST Framework)

### Tecnologias Complementares

- **Celery**: Tarefas assíncronas (envio de emails)
- **Redis**: Cache e filas
- **Elasticsearch**: Busca avançada
- **Django REST Framework**: API REST
- **Webpack**: Build de assets frontend
- **Docker**: Containerização
- **CI/CD**: GitHub Actions, GitLab CI

## Referências

- [Django Documentation](https://docs.djangoproject.com/)
- [TailwindCSS Documentation](https://tailwindcss.com/docs)
- [Pillow Documentation](https://pillow.readthedocs.io/)
- [Django Admin Cookbook](https://books.agiliq.com/projects/django-admin-cookbook/)

---

**Versão**: 1.0.0  
**Data**: 29 de outubro de 2025  
**Python**: 3.13.2  
**Django**: 5.2.7
