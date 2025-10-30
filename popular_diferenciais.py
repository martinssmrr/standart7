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

from core.models import Diferencial

# Textos descritivos para cada diferencial
diferenciais_data = [
    {
        'titulo': 'Atendimento Personalizado',
        'descricao': '''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.

Nossa equipe está comprometida em entender suas necessidades específicas e oferecer soluções customizadas para cada cliente. Valorizamos o relacionamento próximo e a confiança mútua.''',
        'imagem_origem': 'static/img/1.jpg',
        'ordem': 1
    },
    {
        'titulo': 'Transparência Total',
        'descricao': '''Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia.

Mantemos nossos clientes sempre informados sobre cada etapa do processo, com documentação clara e comunicação aberta. Sua segurança e confiança são nossas prioridades.''',
        'imagem_origem': 'static/img/2.jpg',
        'ordem': 2
    },
    {
        'titulo': 'Expertise no Mercado',
        'descricao': '''Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis.

Com anos de experiência no mercado imobiliário, nossa equipe possui conhecimento profundo das melhores oportunidades e tendências do setor.''',
        'imagem_origem': 'static/img/3.jpg',
        'ordem': 3
    },
    {
        'titulo': 'Tecnologia Avançada',
        'descricao': '''Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt.

Utilizamos as mais modernas ferramentas tecnológicas para garantir agilidade, segurança e precisão em todos os nossos processos.''',
        'imagem_origem': 'static/img/4.jpg',
        'ordem': 4
    },
    {
        'titulo': 'Suporte Completo',
        'descricao': '''Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore.

Do primeiro contato até a entrega das chaves, nossa equipe oferece suporte integral, garantindo uma experiência tranquila e satisfatória em cada etapa.''',
        'imagem_origem': 'static/img/5.jpg',
        'ordem': 5
    }
]

def popular_diferenciais():
    """Popula o banco de dados com diferenciais de exemplo"""
    
    # Remove diferenciais existentes
    Diferencial.objects.all().delete()
    print("Diferenciais anteriores removidos.")
    
    # Cria o diretório de upload se não existir
    media_dir = BASE_DIR / 'media' / 'diferenciais'
    media_dir.mkdir(parents=True, exist_ok=True)
    
    # Cria os novos diferenciais
    for data in diferenciais_data:
        # Copia a imagem para o diretório de media
        imagem_origem = BASE_DIR / data['imagem_origem']
        nome_arquivo = f"diferencial_{data['ordem']}.jpg"
        imagem_destino = media_dir / nome_arquivo
        
        if imagem_origem.exists():
            copyfile(imagem_origem, imagem_destino)
            imagem_relativa = f'diferenciais/{nome_arquivo}'
        else:
            print(f"Aviso: Imagem {imagem_origem} não encontrada!")
            imagem_relativa = ''
        
        # Cria o diferencial
        diferencial = Diferencial.objects.create(
            titulo=data['titulo'],
            descricao=data['descricao'],
            imagem=imagem_relativa,
            ordem=data['ordem'],
            ativo=True
        )
        print(f"✓ Diferencial criado: {diferencial.titulo} (ordem: {diferencial.ordem})")
    
    print(f"\n{len(diferenciais_data)} diferenciais foram criados com sucesso!")
    print("\nAcesse http://127.0.0.1:8000/diferenciais/ para visualizar.")
    print("Para gerenciar via admin: http://127.0.0.1:8000/admin/core/diferencial/")

if __name__ == '__main__':
    popular_diferenciais()
