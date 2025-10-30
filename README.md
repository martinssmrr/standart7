# Standart 7 - Landing Page Imobiliária

Sistema de landing page para imobiliária desenvolvido com Django e TailwindCSS.

## 🚀 Tecnologias Utilizadas

- **Backend**: Python 3.13 com Django 5.2.7
- **Frontend**: HTML5 com TailwindCSS via CDN
- **Banco de Dados**: SQLite (padrão do Django)
- **Upload de Imagens**: Pillow

## 📋 Funcionalidades

- ✅ Gestão completa de lançamentos imobiliários via painel admin
- ✅ Página inicial (home) com listagem de empreendimentos
- ✅ Página de detalhes de cada lançamento
- ✅ Galeria de imagens para cada empreendimento
- ✅ Sistema de status (Breve Lançamento, Em Obras, Pronto para Morar)
- ✅ Formulário de contato
- ✅ Design responsivo com TailwindCSS
- ✅ URLs amigáveis (slug)

## 🏗️ Estrutura do Projeto

```
Standart 7/
├── core/                      # Aplicação principal
│   ├── migrations/           # Migrações do banco de dados
│   ├── admin.py             # Configuração do painel admin
│   ├── models.py            # Modelos (Lancamento e GaleriaImagem)
│   ├── views.py             # Views (HomeView e LancamentoDetailView)
│   └── urls.py              # URLs da aplicação
├── standart7/                # Configurações do projeto
│   ├── settings.py          # Configurações gerais
│   ├── urls.py              # URLs principais
│   └── wsgi.py
├── templates/                # Templates HTML
│   ├── base.html            # Template base
│   ├── core/
│   │   └── home.html        # Página inicial
│   └── lancamentos/
│       └── lancamento_detail.html  # Página de detalhes
├── static/                   # Arquivos estáticos
│   ├── css/
│   └── img/
├── media/                    # Upload de imagens
│   └── lancamentos/         # Imagens dos lançamentos
└── manage.py                # Script de gerenciamento Django
```

## 🔧 Instalação e Configuração

### Pré-requisitos

- Python 3.13 ou superior
- pip (gerenciador de pacotes Python)

### Passo a Passo

1. **Ambiente Virtual (já configurado)**
   O projeto já possui um ambiente virtual em `.venv/`

2. **Dependências (já instaladas)**
   - Django 5.2.7
   - Pillow (para upload de imagens)

3. **Banco de Dados (já configurado)**
   As migrações já foram aplicadas e o banco `db.sqlite3` está pronto.

4. **Superusuário (já criado)**
   - **Usuário**: `admin`
   - **Senha**: `admin123`
   - **E-mail**: `admin@standart7.com`

## 🎮 Como Usar

### Iniciar o Servidor

```powershell
cd "c:\Users\teste\OneDrive\Desktop\Standart 7"
& "C:/Users/teste/OneDrive/Desktop/Standart 7/.venv/Scripts/python.exe" manage.py runserver
```

O servidor estará disponível em: **http://127.0.0.1:8000/**

### Acessar o Painel Administrativo

1. Acesse: **http://127.0.0.1:8000/admin/**
2. Faça login com:
   - Usuário: `admin`
   - Senha: `admin123`

### Adicionar um Lançamento

1. No painel admin, clique em **Lançamentos**
2. Clique em **Adicionar Lançamento**
3. Preencha os campos:
   - **Título**: Nome do empreendimento
   - **Slug**: Será preenchido automaticamente
   - **Status**: Escolha entre Breve Lançamento, Em Obras ou Pronto para Morar
   - **Cidade**: Cidade do imóvel
   - **Bairro**: Bairro do imóvel
   - **Descrição Curta**: Texto para o card na home (máx. 250 caracteres)
   - **Descrição Completa**: Texto detalhado para a página de detalhes
   - **Imagem Principal**: Upload da foto de capa
   - **Ativo**: Marque para o lançamento aparecer no site
4. Na seção **Imagens da Galeria**, adicione fotos adicionais com legendas
5. Clique em **Salvar**

### Ver o Site

- **Página Inicial**: http://127.0.0.1:8000/
- **Detalhes de um lançamento**: http://127.0.0.1:8000/lancamentos/[slug]/

## 📊 Modelos do Banco de Dados

### Lancamento
- `titulo`: CharField - Nome do empreendimento
- `slug`: SlugField - URL amigável (gerado automaticamente)
- `status`: CharField - Status do empreendimento (breve/obras/pronto)
- `cidade`: CharField - Cidade
- `bairro`: CharField - Bairro
- `descricao_curta`: CharField - Descrição resumida
- `descricao_completa`: TextField - Descrição detalhada
- `imagem_principal`: ImageField - Foto de capa
- `data_criacao`: DateTimeField - Data de criação (automático)
- `ativo`: BooleanField - Define se aparece no site

### GaleriaImagem
- `lancamento`: ForeignKey - Relacionamento com Lancamento
- `imagem`: ImageField - Foto da galeria
- `legenda`: CharField - Descrição da foto
- `ordem`: IntegerField - Ordem de exibição

## 🎨 Personalização

### Alterar Cores
O TailwindCSS está sendo carregado via CDN. Para personalizar cores:
- Azul principal: classes `bg-blue-600`, `text-blue-600`, etc.
- Cinza: classes `bg-gray-*`, `text-gray-*`

### Adicionar Seções
Edite os templates em `templates/`:
- `base.html` - Layout geral (header e footer)
- `core/home.html` - Página inicial
- `lancamentos/lancamento_detail.html` - Página de detalhes

## 🔒 Segurança

**IMPORTANTE**: Para produção, você deve:
1. Alterar `SECRET_KEY` em `settings.py`
2. Definir `DEBUG = False`
3. Configurar `ALLOWED_HOSTS`
4. Usar um servidor WSGI (Gunicorn, uWSGI)
5. Configurar banco de dados PostgreSQL ou MySQL
6. Servir arquivos estáticos com Nginx ou Whitenoise
7. Alterar as credenciais do superusuário

## 📝 URLs Disponíveis

- `/` - Página inicial com listagem de lançamentos
- `/lancamentos/<slug>/` - Detalhes de um lançamento específico
- `/admin/` - Painel administrativo Django

## 🛠️ Comandos Úteis

```powershell
# Criar novas migrações após alterar models.py
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar novo superusuário
python manage.py createsuperuser

# Coletar arquivos estáticos (para produção)
python manage.py collectstatic
```

## 📦 Estrutura dos Templates

Os templates usam herança do Django:
- `base.html` define a estrutura HTML base
- `home.html` e `lancamento_detail.html` estendem `base.html`
- Usa blocks: `{% block content %}`, `{% block title %}`, etc.

## 🌟 Recursos do Painel Admin

- ✅ List display com colunas personalizadas
- ✅ Filtros por status, cidade e data
- ✅ Busca por título, cidade e bairro
- ✅ Slug preenchido automaticamente
- ✅ Edição inline da galeria de imagens
- ✅ Ativar/desativar lançamentos diretamente na lista
- ✅ Hierarquia por data de criação

## 💡 Dicas

1. **Imagens**: Use fotos de alta qualidade (mín. 1920x1080)
2. **Descrição Curta**: Seja objetivo e atrativo (ideal: 150-200 caracteres)
3. **Descrição Completa**: Detalhe comodidades, metragem, diferenciais
4. **Galeria**: Adicione 5-10 fotos mostrando diferentes ângulos
5. **Status**: Mantenha atualizado para transparência com clientes

## 📞 Suporte

Para dúvidas sobre o Django:
- Documentação oficial: https://docs.djangoproject.com/
- TailwindCSS: https://tailwindcss.com/docs

---

**Desenvolvido com ❤️ usando Django e TailwindCSS**
