# 🔍 Comandos de Verificação - Standart 7

## Verificações Locais (Antes do Deploy)

### 1. Verificar configuração do Django
```bash
python manage.py check
```
**Esperado**: `System check identified no issues (0 silenced).`

### 2. Verificar migrações pendentes
```bash
python manage.py showmigrations
```
**Esperado**: Todas as migrações com [X]

### 3. Testar servidor local
```bash
python manage.py runserver
```
**Esperado**: Servidor inicia sem erros

### 4. Verificar dependências
```bash
pip list
```
**Verificar**: Django, Pillow, python-decouple, gunicorn, whitenoise

### 5. Testar coleta de arquivos estáticos
```bash
python manage.py collectstatic --dry-run
```
**Esperado**: Lista de arquivos sem erros

---

## Verificações no Servidor (Após Deploy)

### 1. Verificar se o Gunicorn está rodando
```bash
sudo supervisorctl status standart7
```
**Esperado**: `standart7 RUNNING pid XXXXX, uptime X:XX:XX`

### 2. Verificar se o Nginx está rodando
```bash
sudo systemctl status nginx
```
**Esperado**: `active (running)`

### 3. Verificar porta do Gunicorn
```bash
sudo netstat -tulpn | grep :8000
```
**Esperado**: Mostra processo escutando na porta 8000

### 4. Verificar configuração do Nginx
```bash
sudo nginx -t
```
**Esperado**: `syntax is ok` e `test is successful`

### 5. Verificar logs em tempo real
```bash
# Logs do Gunicorn
tail -f /var/www/standart7/logs/gunicorn.log

# Logs do Nginx
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### 6. Testar resposta do servidor
```bash
curl -I http://localhost:8000
```
**Esperado**: HTTP 200 OK

### 7. Testar resposta do Nginx
```bash
curl -I http://oportunidadenaplanta.com.br
```
**Esperado**: HTTP 200 OK

### 8. Verificar permissões
```bash
ls -la /var/www/standart7/
ls -la /var/www/standart7/media/
ls -la /var/www/standart7/static/
```
**Esperado**: Owner `www-data:www-data`

### 9. Verificar processos Python
```bash
ps aux | grep gunicorn
```
**Esperado**: Mostra processos do Gunicorn rodando

### 10. Verificar espaço em disco
```bash
df -h
```
**Verificar**: Espaço suficiente disponível

---

## Testes Funcionais

### 1. Testar página inicial
```bash
curl http://oportunidadenaplanta.com.br/
```
**Esperado**: HTML da página inicial

### 2. Testar admin
```bash
curl -I http://oportunidadenaplanta.com.br/admin/
```
**Esperado**: HTTP 200 ou 302 (redirect para login)

### 3. Testar arquivos estáticos
```bash
curl -I http://oportunidadenaplanta.com.br/static/css/style.css
```
**Esperado**: HTTP 200 OK

### 4. Testar arquivos de mídia
```bash
curl -I http://oportunidadenaplanta.com.br/media/hero/ALGUMA_IMAGEM.jpg
```
**Esperado**: HTTP 200 OK (se existir a imagem)

---

## Verificações de Segurança

### 1. Verificar DEBUG está desligado
```bash
grep DEBUG /var/www/standart7/.env
```
**Esperado**: `DEBUG=False`

### 2. Verificar SECRET_KEY está configurada
```bash
grep SECRET_KEY /var/www/standart7/.env
```
**Esperado**: Uma chave longa e aleatória

### 3. Verificar ALLOWED_HOSTS
```bash
grep ALLOWED_HOSTS /var/www/standart7/.env
```
**Esperado**: Contém o domínio do site

### 4. Testar headers de segurança
```bash
curl -I https://oportunidadenaplanta.com.br
```
**Verificar**: Headers de segurança (após configurar SSL)

---

## Verificações de Performance

### 1. Tempo de resposta
```bash
time curl http://oportunidadenaplanta.com.br/ > /dev/null
```
**Esperado**: < 2 segundos

### 2. Tamanho da página
```bash
curl http://oportunidadenaplanta.com.br/ | wc -c
```
**Verificar**: Tamanho razoável

### 3. Verificar compressão Gzip
```bash
curl -H "Accept-Encoding: gzip" -I http://oportunidadenaplanta.com.br/
```
**Esperado**: `Content-Encoding: gzip`

---

## Verificações de Backup

### 1. Verificar se o backup existe
```bash
ls -lh /var/backups/standart7/
```
**Esperado**: Lista de backups

### 2. Verificar cron jobs
```bash
sudo crontab -l
```
**Esperado**: Jobs de backup configurados

### 3. Verificar último backup
```bash
ls -lt /var/backups/standart7/db_*.sqlite3 | head -1
```
**Verificar**: Data recente

---

## Comandos de Diagnóstico

### Se o site não carrega:

```bash
# 1. Verificar todos os serviços
sudo systemctl status nginx
sudo supervisorctl status standart7

# 2. Ver últimos erros do Gunicorn
tail -50 /var/www/standart7/logs/gunicorn_error.log

# 3. Ver últimos erros do Nginx
tail -50 /var/log/nginx/error.log

# 4. Testar conexão direta com Gunicorn
curl http://localhost:8000

# 5. Verificar DNS
nslookup oportunidadenaplanta.com.br

# 6. Verificar firewall
sudo ufw status
```

### Se arquivos estáticos não carregam:

```bash
# 1. Verificar se foram coletados
ls -la /var/www/standart7/static/

# 2. Verificar permissões
sudo chown -R www-data:www-data /var/www/standart7/static/

# 3. Recoletar
cd /var/www/standart7
source venv/bin/activate
python manage.py collectstatic --clear --noinput

# 4. Verificar configuração do Nginx
cat /etc/nginx/sites-enabled/standart7 | grep static
```

---

## Checklist Rápido

Após o deploy, execute em ordem:

```bash
# 1. Verificações básicas
sudo supervisorctl status standart7        # ✓ RUNNING
sudo systemctl status nginx                # ✓ active
curl -I http://localhost:8000              # ✓ HTTP 200

# 2. Verificações de acesso
curl -I http://oportunidadenaplanta.com.br # ✓ HTTP 200
curl -I http://oportunidadenaplanta.com.br/admin/ # ✓ HTTP 200/302

# 3. Verificações de logs
tail -20 /var/www/standart7/logs/gunicorn.log      # ✓ Sem erros
tail -20 /var/log/nginx/error.log                   # ✓ Sem erros

# 4. Verificações de arquivos
ls -la /var/www/standart7/media/           # ✓ www-data
ls -la /var/www/standart7/static/          # ✓ www-data

# 5. Verificação Django
cd /var/www/standart7
source venv/bin/activate
python manage.py check                     # ✓ No issues
```

Se todos passarem: **✅ Deploy bem-sucedido!**

---

## Monitoramento Contínuo

Configure um script de monitoramento:

```bash
#!/bin/bash
# /var/www/standart7/deploy/monitor.sh

echo "=== Status dos Serviços ==="
sudo supervisorctl status standart7
sudo systemctl status nginx --no-pager

echo ""
echo "=== Últimas 5 linhas do log ==="
tail -5 /var/www/standart7/logs/gunicorn.log

echo ""
echo "=== Uso de Disco ==="
df -h | grep -E '/$|/var'

echo ""
echo "=== Uso de Memória ==="
free -h

echo ""
echo "=== Processos Gunicorn ==="
ps aux | grep gunicorn | grep -v grep | wc -l
echo "workers rodando"
```

Execute periodicamente:
```bash
chmod +x /var/www/standart7/deploy/monitor.sh
/var/www/standart7/deploy/monitor.sh
```

---

**Última atualização**: 06/11/2025
