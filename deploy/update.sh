#!/bin/bash

# Script de Atualização - Standart 7
# Execute este script quando fizer alterações no código

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

PROJECT_DIR="/var/www/standart7"
VENV_DIR="$PROJECT_DIR/venv"

echo -e "${YELLOW}=========================================="
echo -e "Atualizando Standart 7"
echo -e "==========================================${NC}"

# Verificar se está no diretório correto
if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${RED}Erro: Diretório do projeto não encontrado!${NC}"
    exit 1
fi

cd $PROJECT_DIR

# 1. Fazer backup antes da atualização
echo -e "${YELLOW}1. Fazendo backup antes da atualização...${NC}"
if [ -f "deploy/backup.sh" ]; then
    bash deploy/backup.sh
    echo -e "${GREEN}✓ Backup concluído${NC}"
else
    echo -e "${YELLOW}⚠ Script de backup não encontrado, continuando...${NC}"
fi

# 2. Atualizar código do repositório (se usando Git)
echo -e "${YELLOW}2. Atualizando código do repositório...${NC}"
if [ -d ".git" ]; then
    git pull origin main || git pull origin master
    echo -e "${GREEN}✓ Código atualizado${NC}"
else
    echo -e "${YELLOW}⚠ Não é um repositório Git, pulando...${NC}"
fi

# 3. Ativar ambiente virtual
echo -e "${YELLOW}3. Ativando ambiente virtual...${NC}"
source $VENV_DIR/bin/activate

# 4. Instalar/atualizar dependências
echo -e "${YELLOW}4. Instalando dependências...${NC}"
pip install -r requirements.txt
echo -e "${GREEN}✓ Dependências instaladas${NC}"

# 5. Fazer migrações do banco de dados
echo -e "${YELLOW}5. Executando migrações...${NC}"
python manage.py makemigrations
python manage.py migrate
echo -e "${GREEN}✓ Migrações aplicadas${NC}"

# 6. Coletar arquivos estáticos
echo -e "${YELLOW}6. Coletando arquivos estáticos...${NC}"
python manage.py collectstatic --noinput
echo -e "${GREEN}✓ Arquivos estáticos coletados${NC}"

# 7. Verificar erros no projeto
echo -e "${YELLOW}7. Verificando configurações...${NC}"
python manage.py check
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Nenhum erro encontrado${NC}"
else
    echo -e "${RED}✗ Erros encontrados! Verifique antes de continuar.${NC}"
    read -p "Continuar mesmo assim? (s/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        exit 1
    fi
fi

# 8. Ajustar permissões
echo -e "${YELLOW}8. Ajustando permissões...${NC}"
sudo chown -R www-data:www-data $PROJECT_DIR
sudo chmod -R 755 $PROJECT_DIR
sudo chmod -R 775 $PROJECT_DIR/media
sudo chmod -R 775 $PROJECT_DIR/static
echo -e "${GREEN}✓ Permissões ajustadas${NC}"

# 9. Reiniciar aplicação
echo -e "${YELLOW}9. Reiniciando aplicação...${NC}"
sudo supervisorctl restart standart7
sleep 2
sudo supervisorctl status standart7
echo -e "${GREEN}✓ Aplicação reiniciada${NC}"

# 10. Limpar cache do Nginx (opcional)
echo -e "${YELLOW}10. Reiniciando Nginx...${NC}"
sudo systemctl reload nginx
echo -e "${GREEN}✓ Nginx reiniciado${NC}"

echo ""
echo -e "${GREEN}=========================================="
echo -e "Atualização concluída com sucesso!"
echo -e "==========================================${NC}"
echo ""
echo -e "${YELLOW}Verificações pós-atualização:${NC}"
echo "1. Acesse: http://oportunidadenaplanta.com.br"
echo "2. Teste as funcionalidades principais"
echo "3. Verifique os logs: tail -f logs/gunicorn.log"
echo ""
