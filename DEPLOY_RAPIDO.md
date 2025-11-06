# Deploy Rápido - Standart 7

## 🚀 Como fazer o deploy na VPS Hostinger

### 1️⃣ Preparar arquivos localmente

Todos os arquivos já estão preparados:
- ✅ `.env` criado com configurações de produção
- ✅ `requirements.txt` com todas as dependências
- ✅ `settings.py` configurado para ler variáveis de ambiente
- ✅ Scripts de deploy na pasta `deploy/`

### 2️⃣ Enviar para o servidor

**Opção A: Via Git (recomendado)**
```bash
# No servidor
cd /var/www
git clone URL_DO_SEU_REPOSITORIO standart7
```

**Opção B: Via FTP/SFTP**
- Envie todos os arquivos do projeto para `/var/www/standart7/`
- Não esqueça de enviar o arquivo `.env`

### 3️⃣ Executar no servidor

Conecte via SSH e execute:

```bash
cd /var/www/standart7
chmod +x deploy/deploy.sh
sudo ./deploy/deploy.sh
```

### 4️⃣ Criar superusuário

```bash
cd /var/www/standart7
source venv/bin/activate
python manage.py createsuperuser
```

### 5️⃣ Pronto! ✨

Acesse: http://oportunidadenaplanta.com.br

---

## 📝 Variáveis importantes no .env

```env
SECRET_KEY=k)9r#ga!a1oqv0js0u2751l#)167!4=ob*@yv%_a8qls2u^_=)
DEBUG=False
ALLOWED_HOSTS=oportunidadenaplanta.com.br,www.oportunidadenaplanta.com.br
```

---

## 🔧 Comandos úteis

```bash
# Reiniciar aplicação
sudo supervisorctl restart standart7

# Ver logs
tail -f /var/www/standart7/logs/gunicorn.log

# Atualizar código
cd /var/www/standart7
git pull
source venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
sudo supervisorctl restart standart7
```

---

## 🔒 Configurar HTTPS (depois do deploy)

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d oportunidadenaplanta.com.br -d www.oportunidadenaplanta.com.br
```

Depois, atualize no `.env`:
```env
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

E reinicie:
```bash
sudo supervisorctl restart standart7
```

---

## 📦 Arquivos criados para deploy

- ✅ `.env` - Variáveis de ambiente (produção)
- ✅ `.env.example` - Exemplo de variáveis de ambiente
- ✅ `.gitignore` - Arquivos a ignorar no Git
- ✅ `requirements.txt` - Dependências Python
- ✅ `deploy/deploy.sh` - Script automático de deploy
- ✅ `deploy/nginx_standart7.conf` - Configuração Nginx
- ✅ `deploy/supervisor_standart7.conf` - Configuração Supervisor
- ✅ `deploy/README_DEPLOY.md` - Guia completo de deploy

---

## ⚠️ Importante

1. **Backup**: Sempre faça backup do banco de dados antes de atualizar
2. **Segurança**: Nunca versione o arquivo `.env` no Git
3. **SSL**: Configure HTTPS para segurança (Let's Encrypt é gratuito)
4. **Monitoramento**: Configure logs e monitoramento em produção

---

**Domínio**: http://oportunidadenaplanta.com.br
**Data**: Novembro 2025
