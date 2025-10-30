import os
import sys
import django
from pathlib import Path
from shutil import copyfile

# Adiciona o diretório raiz ao path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Configura o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'standart7.settings')
django.setup()

from core.models import HeroSection, SobreSection

def popular_hero_section():
    """Popula a Hero Section com dados iniciais"""
    
    # Remove dados anteriores
    HeroSection.objects.all().delete()
    
    # Cria Hero Section
    hero = HeroSection.objects.create(
        titulo='Investimento Inteligente em Imóveis',
        subtitulo='Transforme seu capital em patrimônio com segurança e rentabilidade',
        texto_botao='Consultoria Especializada',
        imagem_fundo='static/img/home.jpg',  # Usa a imagem existente
        ativo=True
    )
    
    print(f"✓ Hero Section criada: {hero.titulo}")
    print(f"  - Subtítulo: {hero.subtitulo}")
    print(f"  - Botão: {hero.texto_botao}")
    
def popular_sobre_section():
    """Popula a Seção Sobre com dados iniciais"""
    
    # Remove dados anteriores
    SobreSection.objects.all().delete()
    
    # Cria Seção Sobre
    sobre = SobreSection.objects.create(
        titulo='Nossa História',
        
        nome_fundadora='Camilla Daianne',
        texto_fundadora='''Camilla Daianne antecipou o potencial do mercado imobiliário do Oeste da Bahia em 2018. Com expertise em administração, coaching e consultoria, ela dedicou-se a aprimorar o conhecimento para atender a uma única demanda: o investimento inteligente.''',
        foto_fundadora='static/img/camila2.png',  # Usa a imagem existente
        
        nome_fundador='Marlon Deivison',
        texto_fundador='''Marlon Deivison injetou o DNA da inovação. Apaixonado por Marketing e Vendas, ele transformou o cenário regional a partir de 2021, elevando a operação para o digital. Juntos, eles criaram processos que tornaram o investimento mais rápido, acessível e totalmente seguro, sem jamais perder o foco no relacionamento humano.''',
        foto_fundador='static/img/marlon.jpg',  # Usa a imagem existente
        
        ativo=True
    )
    
    print(f"\n✓ Seção Sobre criada: {sobre.titulo}")
    print(f"  - Fundadora: {sobre.nome_fundadora}")
    print(f"  - Fundador: {sobre.nome_fundador}")

if __name__ == '__main__':
    print("=" * 50)
    print("POPULANDO HERO SECTION E SEÇÃO SOBRE")
    print("=" * 50)
    
    popular_hero_section()
    popular_sobre_section()
    
    print("\n" + "=" * 50)
    print("CONCLUÍDO COM SUCESSO!")
    print("=" * 50)
    print("\nAcesse o admin para gerenciar:")
    print("- Hero Section: http://127.0.0.1:8000/admin/core/herosection/")
    print("- Seção Sobre: http://127.0.0.1:8000/admin/core/sobresection/")
