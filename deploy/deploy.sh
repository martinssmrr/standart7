#!/bin/bash

# Script de Deploy para VPS Hostinger - Standart 7
# Execute este script no servidor após fazer upload do projeto

echo "=========================================="
echo "Iniciando Deploy - Standart 7"
echo "=========================================="

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Variáveis
PROJECT_NAME="standart7"
PROJECT_DIR="/var/www/$PROJECT_NAME"
VENV_DIR="$PROJECT_DIR/venv"
USER="www-data"

# Verificar se está executando como root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}Por favor, execute como root (sudo)${NC}"
    exit 1
fi

echo -e "${YELLOW}1. Instalando dependências do sistema...${NC}"
apt-get update
apt-get install -y python3 python3-pip python3-venv nginx supervisor git

echo -e "${YELLOW}2. Criando diretórios necessários...${NC}"
mkdir -p $PROJECT_DIR
mkdir -p $PROJECT_DIR/logs
mkdir -p $PROJECT_DIR/static
mkdir -p $PROJECT_DIR/media

echo -e "${YELLOW}3. Criando ambiente virtual Python...${NC}"
cd $PROJECT_DIR
python3 -m venv $VENV_DIR

echo -e "${YELLOW}4. Ativando ambiente virtual e instalando dependências...${NC}"
source $VENV_DIR/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo -e "${YELLOW}5. Configurando arquivo .env...${NC}"
if [ ! -f "$PROJECT_DIR/.env" ]; then
    echo -e "${RED}ATENÇÃO: Arquivo .env não encontrado!${NC}"
    echo -e "${YELLOW}Por favor, crie o arquivo .env baseado no .env.example${NC}"
    echo -e "${YELLOW}Você pode fazer isso agora ou após o deploy.${NC}"
else
    echo -e "${GREEN}Arquivo .env encontrado!${NC}"
fi

echo -e "${YELLOW}6. Executando migrações do Django...${NC}"
python manage.py migrate --noinput

echo -e "${YELLOW}7. Coletando arquivos estáticos...${NC}"
python manage.py collectstatic --noinput

echo -e "${YELLOW}8. Criando superusuário (se necessário)...${NC}"
echo -e "${YELLOW}Você pode fazer isso depois com: python manage.py createsuperuser${NC}"

echo -e "${YELLOW}9. Configurando permissões...${NC}"
chown -R $USER:$USER $PROJECT_DIR
chmod -R 755 $PROJECT_DIR
chmod -R 775 $PROJECT_DIR/media
chmod -R 775 $PROJECT_DIR/static
chmod -R 775 $PROJECT_DIR/logs

echo -e "${YELLOW}10. Configurando Nginx...${NC}"
if [ -f "$PROJECT_DIR/deploy/nginx_$PROJECT_NAME.conf" ]; then
    cp $PROJECT_DIR/deploy/nginx_$PROJECT_NAME.conf /etc/nginx/sites-available/$PROJECT_NAME
    ln -sf /etc/nginx/sites-available/$PROJECT_NAME /etc/nginx/sites-enabled/
    rm -f /etc/nginx/sites-enabled/default
    nginx -t && systemctl restart nginx
    echo -e "${GREEN}Nginx configurado com sucesso!${NC}"
else
    echo -e "${RED}Arquivo de configuração do Nginx não encontrado!${NC}"
fi

echo -e "${YELLOW}11. Configurando Supervisor...${NC}"
if [ -f "$PROJECT_DIR/deploy/supervisor_$PROJECT_NAME.conf" ]; then
    cp $PROJECT_DIR/deploy/supervisor_$PROJECT_NAME.conf /etc/supervisor/conf.d/$PROJECT_NAME.conf
    supervisorctl reread
    supervisorctl update
    supervisorctl restart $PROJECT_NAME
    echo -e "${GREEN}Supervisor configurado com sucesso!${NC}"
else
    echo -e "${RED}Arquivo de configuração do Supervisor não encontrado!${NC}"
fi

echo -e "${YELLOW}12. Verificando status dos serviços...${NC}"
systemctl status nginx --no-pager
supervisorctl status $PROJECT_NAME

echo ""
echo -e "${GREEN}=========================================="
echo -e "Deploy concluído!"
echo -e "==========================================${NC}"
echo ""
echo -e "${YELLOW}Próximos passos:${NC}"
echo "1. Verifique o arquivo .env e ajuste conforme necessário"
echo "2. Crie um superusuário: cd $PROJECT_DIR && source venv/bin/activate && python manage.py createsuperuser"
echo "3. Acesse http://oportunidadenaplanta.com.br"
echo "4. Configure SSL/HTTPS com Let's Encrypt (recomendado)"
echo ""
echo -e "${YELLOW}Comandos úteis:${NC}"
echo "- Reiniciar aplicação: sudo supervisorctl restart $PROJECT_NAME"
echo "- Ver logs: tail -f $PROJECT_DIR/logs/gunicorn.log"
echo "- Reiniciar Nginx: sudo systemctl restart nginx"
echo ""
