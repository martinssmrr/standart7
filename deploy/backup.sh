#!/bin/bash

# Script de Backup - Standart 7
# Execute periodicamente para fazer backup do banco de dados e arquivos de mídia

# Configurações
PROJECT_NAME="standart7"
PROJECT_DIR="/var/www/$PROJECT_NAME"
BACKUP_DIR="/var/backups/$PROJECT_NAME"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Iniciando backup do Standart 7...${NC}"

# Criar diretório de backup se não existir
mkdir -p $BACKUP_DIR

# Backup do banco de dados SQLite
echo -e "${YELLOW}Fazendo backup do banco de dados...${NC}"
if [ -f "$PROJECT_DIR/db.sqlite3" ]; then
    cp $PROJECT_DIR/db.sqlite3 $BACKUP_DIR/db_$DATE.sqlite3
    echo -e "${GREEN}✓ Backup do banco de dados concluído${NC}"
else
    echo -e "${YELLOW}Banco de dados não encontrado${NC}"
fi

# Backup dos arquivos de mídia
echo -e "${YELLOW}Fazendo backup dos arquivos de mídia...${NC}"
if [ -d "$PROJECT_DIR/media" ]; then
    tar -czf $BACKUP_DIR/media_$DATE.tar.gz -C $PROJECT_DIR media/
    echo -e "${GREEN}✓ Backup dos arquivos de mídia concluído${NC}"
else
    echo -e "${YELLOW}Pasta de mídia não encontrada${NC}"
fi

# Backup do arquivo .env
echo -e "${YELLOW}Fazendo backup do arquivo .env...${NC}"
if [ -f "$PROJECT_DIR/.env" ]; then
    cp $PROJECT_DIR/.env $BACKUP_DIR/env_$DATE.txt
    echo -e "${GREEN}✓ Backup do .env concluído${NC}"
fi

# Remover backups antigos (manter apenas os últimos X dias)
echo -e "${YELLOW}Removendo backups antigos (> $RETENTION_DAYS dias)...${NC}"
find $BACKUP_DIR -name "db_*.sqlite3" -mtime +$RETENTION_DAYS -delete
find $BACKUP_DIR -name "media_*.tar.gz" -mtime +$RETENTION_DAYS -delete
find $BACKUP_DIR -name "env_*.txt" -mtime +$RETENTION_DAYS -delete

# Listar backups existentes
echo ""
echo -e "${GREEN}Backups existentes:${NC}"
ls -lh $BACKUP_DIR

echo ""
echo -e "${GREEN}Backup concluído com sucesso!${NC}"
echo -e "Localização: $BACKUP_DIR"
