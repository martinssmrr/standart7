# Script para gerenciar o servidor Django
# Execute no PowerShell

$PYTHON = "C:/Users/teste/OneDrive/Desktop/Standart 7/.venv/Scripts/python.exe"
$PROJECT_DIR = "c:\Users\teste\OneDrive\Desktop\Standart 7"

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "  STANDART 7 - Gerenciador" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Escolha uma opcao:" -ForegroundColor Yellow
Write-Host "1. Iniciar servidor (http://127.0.0.1:8000/)" -ForegroundColor White
Write-Host "2. Criar superusuario" -ForegroundColor White
Write-Host "3. Fazer migrações" -ForegroundColor White
Write-Host "4. Abrir shell Django" -ForegroundColor White
Write-Host "5. Listar lançamentos ativos" -ForegroundColor White
Write-Host "0. Sair" -ForegroundColor White
Write-Host ""

$opcao = Read-Host "Digite o numero da opcao"

switch ($opcao) {
    "1" {
        Write-Host "`nIniciando servidor..." -ForegroundColor Green
        Write-Host "Acesse: http://127.0.0.1:8000/" -ForegroundColor Cyan
        Write-Host "Admin: http://127.0.0.1:8000/admin/" -ForegroundColor Cyan
        Write-Host "Pressione CTRL+C para parar`n" -ForegroundColor Yellow
        Set-Location $PROJECT_DIR
        & $PYTHON manage.py runserver
    }
    "2" {
        Write-Host "`nCriando superusuario..." -ForegroundColor Green
        Set-Location $PROJECT_DIR
        & $PYTHON manage.py createsuperuser
    }
    "3" {
        Write-Host "`nFazendo migrações..." -ForegroundColor Green
        Set-Location $PROJECT_DIR
        & $PYTHON manage.py makemigrations
        & $PYTHON manage.py migrate
    }
    "4" {
        Write-Host "`nAbrindo shell Django..." -ForegroundColor Green
        Write-Host "Digite 'exit()' para sair`n" -ForegroundColor Yellow
        Set-Location $PROJECT_DIR
        & $PYTHON manage.py shell
    }
    "5" {
        Write-Host "`nListando lançamentos ativos..." -ForegroundColor Green
        Set-Location $PROJECT_DIR
        & $PYTHON -c "import os, django; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'standart7.settings'); django.setup(); from core.models import Lancamento; lancamentos = Lancamento.objects.filter(ativo=True); print(f'\nTotal: {lancamentos.count()} lancamentos ativos\n'); [print(f'- {l.titulo} ({l.cidade})') for l in lancamentos]"
    }
    "0" {
        Write-Host "`nAte logo!" -ForegroundColor Green
        exit
    }
    default {
        Write-Host "`nOpcao invalida!" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Pressione Enter para sair..." -ForegroundColor Gray
Read-Host
