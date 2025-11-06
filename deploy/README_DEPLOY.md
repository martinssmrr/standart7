# Guia de Deploy - Standart 7
## Deploy na VPS Hostinger

### Informações do Projeto
- **Domínio**: http://oportunidadenaplanta.com.br
- **Framework**: Django 5.2.7
- **Servidor Web**: Nginx
- **Servidor de Aplicação**: Gunicorn
- **Gerenciador de Processos**: Supervisor

---

## Pré-requisitos no Servidor

1. **Acesso SSH à VPS Hostinger**
2. **Python 3.8+** instalado
3. **Permissões de root/sudo**

---

## Passo a Passo do Deploy

### 1. Fazer Upload do Projeto

Use FTP, SFTP ou Git para fazer upload dos arquivos para o servidor:

```bash
# Opção 1: Via Git (recomendado)
cd /var/www
git clone https://github.com/seu-usuario/standart7.git
cd standart7

# Opção 2: Via rsync (do seu computador local)
rsync -avz --exclude='*.pyc' --exclude='__pycache__' \
  /caminho/local/standart7/ usuario@seu-servidor:/var/www/standart7/
```

### 2. Configurar o Arquivo .env

Edite o arquivo `.env` no servidor:

```bash
cd /var/www/standart7
nano .env
```

Certifique-se de que as seguintes configurações estão corretas:

```env
SECRET_KEY=k)9r#ga!a1oqv0js0u2751l#)167!4=ob*@yv%_a8qls2u^_=)
DEBUG=False
ALLOWED_HOSTS=oportunidadenaplanta.com.br,www.oportunidadenaplanta.com.br

# Database - SQLite (para começar)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# Security Settings
CSRF_TRUSTED_ORIGINS=http://oportunidadenaplanta.com.br,https://oportunidadenaplanta.com.br,http://www.oportunidadenaplanta.com.br,https://www.oportunidadenaplanta.com.br
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False

# Static and Media Files
STATIC_ROOT=/var/www/standart7/static
MEDIA_ROOT=/var/www/standart7/media
```

### 3. Executar o Script de Deploy

```bash
cd /var/www/standart7
chmod +x deploy/deploy.sh
sudo ./deploy/deploy.sh
```

### 4. Criar Superusuário

```bash
cd /var/www/standart7
source venv/bin/activate
python manage.py createsuperuser
```

### 5. Transferir Banco de Dados e Mídia (se existir)

Se você já tem dados em desenvolvimento:

```bash
# No seu computador local, copiar o banco de dados
scp db.sqlite3 usuario@seu-servidor:/var/www/standart7/

# Copiar arquivos de mídia
scp -r media/* usuario@seu-servidor:/var/www/standart7/media/

# No servidor, ajustar permissões
sudo chown -R www-data:www-data /var/www/standart7/db.sqlite3
sudo chown -R www-data:www-data /var/www/standart7/media
```

### 6. Configurar SSL/HTTPS (Recomendado)

```bash
# Instalar Certbot
sudo apt-get install certbot python3-certbot-nginx

# Obter certificado SSL
sudo certbot --nginx -d oportunidadenaplanta.com.br -d www.oportunidadenaplanta.com.br

# Certbot irá configurar automaticamente o Nginx para HTTPS
```

Após instalar o SSL, atualize o `.env`:

```env
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

E reinicie a aplicação:

```bash
sudo supervisorctl restart standart7
```

---

## Comandos Úteis

### Gerenciar a Aplicação

```bash
# Reiniciar aplicação
sudo supervisorctl restart standart7

# Ver status
sudo supervisorctl status standart7

# Ver logs em tempo real
tail -f /var/www/standart7/logs/gunicorn.log
tail -f /var/www/standart7/logs/nginx_access.log
```

### Gerenciar Nginx

```bash
# Reiniciar Nginx
sudo systemctl restart nginx

# Verificar configuração
sudo nginx -t

# Ver status
sudo systemctl status nginx
```

### Django Management

```bash
cd /var/www/standart7
source venv/bin/activate

# Fazer migrações
python manage.py makemigrations
python manage.py migrate

# Coletar arquivos estáticos
python manage.py collectstatic

# Criar superusuário
python manage.py createsuperuser
```

### Atualizar o Projeto

```bash
# 1. Fazer backup do banco de dados
cp /var/www/standart7/db.sqlite3 /var/www/standart7/db.sqlite3.backup

# 2. Atualizar código (se usando Git)
cd /var/www/standart7
git pull origin main

# 3. Ativar ambiente virtual
source venv/bin/activate

# 4. Instalar novas dependências (se houver)
pip install -r requirements.txt

# 5. Fazer migrações
python manage.py migrate

# 6. Coletar arquivos estáticos
python manage.py collectstatic --noinput

# 7. Reiniciar aplicação
sudo supervisorctl restart standart7
```

---

## Estrutura de Diretórios no Servidor

```
/var/www/standart7/
├── core/                   # App Django
├── standart7/             # Configurações do projeto
├── templates/             # Templates
├── static/                # Arquivos estáticos (CSS, JS, imagens)
├── media/                 # Uploads de usuários
├── venv/                  # Ambiente virtual Python
├── logs/                  # Logs da aplicação
│   ├── gunicorn.log
│   ├── gunicorn_error.log
│   ├── nginx_access.log
│   └── nginx_error.log
├── deploy/                # Scripts e configurações de deploy
├── manage.py
├── requirements.txt
├── .env                   # Variáveis de ambiente (NÃO versionar)
└── db.sqlite3            # Banco de dados SQLite
```

---

## Troubleshooting

### Erro 502 Bad Gateway

```bash
# Verificar se Gunicorn está rodando
sudo supervisorctl status standart7

# Se não estiver, iniciar
sudo supervisorctl start standart7

# Ver logs de erro
tail -f /var/www/standart7/logs/gunicorn_error.log
```

### Erro 500 Internal Server Error

```bash
# Ver logs da aplicação
tail -f /var/www/standart7/logs/gunicorn.log

# Verificar configurações do Django
cd /var/www/standart7
source venv/bin/activate
python manage.py check
```

### Arquivos estáticos não carregam

```bash
# Coletar arquivos estáticos novamente
cd /var/www/standart7
source venv/bin/activate
python manage.py collectstatic --clear --noinput

# Verificar permissões
sudo chown -R www-data:www-data /var/www/standart7/static
```

### Permissões de mídia

```bash
# Garantir que www-data pode escrever em media/
sudo chown -R www-data:www-data /var/www/standart7/media
sudo chmod -R 775 /var/www/standart7/media
```

---

## Migração para PostgreSQL (Opcional)

Para melhor performance em produção, considere migrar para PostgreSQL:

1. **Instalar PostgreSQL**:
```bash
sudo apt-get install postgresql postgresql-contrib
```

2. **Criar banco de dados**:
```bash
sudo -u postgres psql
CREATE DATABASE standart7_db;
CREATE USER standart7_user WITH PASSWORD 'senha_segura';
GRANT ALL PRIVILEGES ON DATABASE standart7_db TO standart7_user;
\q
```

3. **Atualizar .env**:
```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=standart7_db
DB_USER=standart7_user
DB_PASSWORD=senha_segura
DB_HOST=localhost
DB_PORT=5432
```

4. **Migrar dados**:
```bash
# Fazer dump do SQLite (no ambiente de desenvolvimento)
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 4 > datadump.json

# Copiar para o servidor e carregar
python manage.py loaddata datadump.json
```

---

## Contato e Suporte

- **Domínio**: http://oportunidadenaplanta.com.br
- **Admin**: http://oportunidadenaplanta.com.br/admin/

---

## Checklist de Deploy

- [ ] Código enviado para o servidor
- [ ] Arquivo .env configurado corretamente
- [ ] Script deploy.sh executado com sucesso
- [ ] Superusuário criado
- [ ] Banco de dados e mídia transferidos (se aplicável)
- [ ] Nginx configurado e rodando
- [ ] Gunicorn rodando via Supervisor
- [ ] Site acessível via domínio
- [ ] SSL/HTTPS configurado (recomendado)
- [ ] Backup configurado
- [ ] Monitoramento configurado (opcional)

---

**Última atualização**: Novembro 2025
