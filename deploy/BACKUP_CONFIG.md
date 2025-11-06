# Configuração de Backup Automático

## Configurar Cron Job para Backup Diário

### 1. Dar permissão de execução ao script
```bash
chmod +x /var/www/standart7/deploy/backup.sh
```

### 2. Editar crontab
```bash
sudo crontab -e
```

### 3. Adicionar as seguintes linhas:

```cron
# Backup diário às 3h da manhã
0 3 * * * /var/www/standart7/deploy/backup.sh >> /var/www/standart7/logs/backup.log 2>&1

# Backup semanal completo (domingo às 4h)
0 4 * * 0 /var/www/standart7/deploy/backup.sh >> /var/www/standart7/logs/backup_weekly.log 2>&1
```

### 4. Verificar se o cron está ativo
```bash
sudo systemctl status cron
```

---

## Restaurar Backup

### Restaurar Banco de Dados
```bash
# Parar a aplicação
sudo supervisorctl stop standart7

# Restaurar o banco
cp /var/backups/standart7/db_YYYYMMDD_HHMMSS.sqlite3 /var/www/standart7/db.sqlite3

# Ajustar permissões
sudo chown www-data:www-data /var/www/standart7/db.sqlite3

# Iniciar a aplicação
sudo supervisorctl start standart7
```

### Restaurar Arquivos de Mídia
```bash
# Extrair backup
cd /var/www/standart7
tar -xzf /var/backups/standart7/media_YYYYMMDD_HHMMSS.tar.gz

# Ajustar permissões
sudo chown -R www-data:www-data /var/www/standart7/media
sudo chmod -R 775 /var/www/standart7/media
```

---

## Backup Manual

Para fazer um backup manual a qualquer momento:
```bash
sudo /var/www/standart7/deploy/backup.sh
```

---

## Verificar Backups

```bash
# Listar todos os backups
ls -lh /var/backups/standart7/

# Ver tamanho total dos backups
du -sh /var/backups/standart7/
```

---

## Backup para Servidor Externo (Opcional)

Para maior segurança, configure backup para outro servidor ou serviço de armazenamento:

### Usando rsync para servidor remoto:
```bash
#!/bin/bash
# Adicionar ao final do backup.sh

REMOTE_USER="usuario"
REMOTE_HOST="backup.servidor.com"
REMOTE_DIR="/backups/standart7"

rsync -avz /var/backups/standart7/ $REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR/
```

### Usando AWS S3:
```bash
#!/bin/bash
# Instalar AWS CLI primeiro: sudo apt-get install awscli

aws s3 sync /var/backups/standart7/ s3://seu-bucket/standart7/
```

---

## Monitoramento de Backups

Criar script para verificar se os backups estão sendo feitos:

```bash
#!/bin/bash
# /var/www/standart7/deploy/check_backup.sh

BACKUP_DIR="/var/backups/standart7"
LATEST_BACKUP=$(ls -t $BACKUP_DIR/db_*.sqlite3 | head -1)
BACKUP_AGE=$(( ($(date +%s) - $(stat -c %Y "$LATEST_BACKUP")) / 86400 ))

if [ $BACKUP_AGE -gt 2 ]; then
    echo "ALERTA: Último backup tem mais de 2 dias!"
    # Enviar email ou notificação
else
    echo "OK: Backup recente encontrado"
fi
```

Adicionar ao crontab para verificar diariamente:
```cron
0 12 * * * /var/www/standart7/deploy/check_backup.sh
```
