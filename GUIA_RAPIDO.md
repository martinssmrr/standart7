# 🎯 Guia Rápido de Uso - Standart 7

## ✅ Status do Projeto

**PROJETO CONCLUÍDO E FUNCIONANDO!**

- ✅ Backend Django configurado
- ✅ Modelos criados (Lancamento e GaleriaImagem)
- ✅ Painel admin customizado
- ✅ Views e URLs configuradas
- ✅ Templates responsivos com TailwindCSS
- ✅ Banco de dados criado e migrado
- ✅ Superusuário criado
- ✅ 3 lançamentos de exemplo adicionados
- ✅ Servidor rodando em http://127.0.0.1:8000/

## 🚀 Como Acessar

### Site Principal
**URL**: http://127.0.0.1:8000/

Você verá:
- Hero section com banner
- 3 cards de lançamentos (Residencial Chicago, Condomínio Riviera, Sky Tower)
- Seção de contato
- Footer com informações

### Painel Administrativo
**URL**: http://127.0.0.1:8000/admin/

**Credenciais**:
- Usuário: `admin`
- Senha: `admin123`

## 📝 Como Adicionar Imagens aos Lançamentos

1. Acesse o admin: http://127.0.0.1:8000/admin/
2. Faça login com admin/admin123
3. Clique em **Lançamentos**
4. Selecione um dos lançamentos existentes
5. No campo **Imagem Principal**, clique em "Escolher arquivo" e faça upload de uma imagem
6. Role até a seção **Imagens da Galeria**
7. Adicione múltiplas imagens com legendas opcionais
8. Clique em **Salvar**

**Dica**: Você já tem 3 imagens na raiz do projeto:
- `chicago.jpg`
- `riviera.jpg`
- `sky.jpg`

Pode usá-las como imagens principais dos respectivos lançamentos!

## 🎨 Páginas Disponíveis

### 1. Home (/)
- Lista todos os lançamentos ativos
- Cards com imagem, título, localização e descrição curta
- Badge de status colorido (Breve Lançamento/Em Obras/Pronto)
- Botão "Ver Detalhes" para cada lançamento

### 2. Detalhes do Lançamento (/lancamentos/{slug}/)
Exemplos:
- http://127.0.0.1:8000/lancamentos/residencial-chicago/
- http://127.0.0.1:8000/lancamentos/condominio-riviera/
- http://127.0.0.1:8000/lancamentos/edificio-sky-tower/

Mostra:
- Banner com imagem principal
- Descrição completa do empreendimento
- Galeria de imagens (se adicionadas)
- Informações de localização e status
- Formulário de contato lateral

## 🔧 Funcionalidades do Admin

### Gerenciar Lançamentos
- **List Display**: Ver título, status, cidade, bairro, ativo e data
- **Filtros**: Filtrar por status, cidade, ativo e data
- **Busca**: Buscar por título, cidade, bairro ou descrição
- **Slug Automático**: Gerado automaticamente a partir do título
- **Ativar/Desativar**: Marque/desmarque o checkbox "Ativo" na listagem
- **Galeria Inline**: Adicione múltiplas imagens diretamente na página do lançamento

### Adicionar Novo Lançamento
1. No admin, clique em **Lançamentos** > **Adicionar Lançamento**
2. Preencha:
   - Título (ex: "Residencial Horizonte")
   - Status (escolha uma opção)
   - Cidade
   - Bairro
   - Descrição Curta (max 250 caracteres)
   - Descrição Completa (use quebras de linha para formatar)
   - Imagem Principal (upload)
   - Marque "Ativo" para aparecer no site
3. Adicione imagens da galeria na seção inline (opcional)
4. Salve

## 🎯 Testar o Sistema

### Teste 1: Ver Lançamentos na Home
1. Acesse http://127.0.0.1:8000/
2. Você deve ver 3 cards de lançamentos
3. Cada card tem badge colorido de status

### Teste 2: Ver Detalhes de um Lançamento
1. Clique em "Ver Detalhes" em qualquer card
2. Você será levado para a página de detalhes
3. Verá descrição completa e formulário de contato

### Teste 3: Adicionar Imagens no Admin
1. Acesse http://127.0.0.1:8000/admin/
2. Login: admin/admin123
3. Vá em Lançamentos > Residencial Chicago
4. Faça upload da imagem `chicago.jpg` como Imagem Principal
5. Salve
6. Volte para http://127.0.0.1:8000/
7. Agora o card do Residencial Chicago terá a imagem

### Teste 4: Desativar um Lançamento
1. No admin, vá para a lista de Lançamentos
2. Desmarque o checkbox "Ativo" de um lançamento
3. Salve
4. Volte para a home - o lançamento desativado não aparece mais

### Teste 5: Adicionar Galeria de Imagens
1. Edite um lançamento no admin
2. Role até "Imagens da Galeria"
3. Adicione 3-5 imagens
4. Coloque legendas descritivas
5. Defina a ordem (0, 1, 2...)
6. Salve
7. Acesse a página de detalhes do lançamento
8. Verá a galeria em grid 2 colunas

## 🛑 Comandos do Servidor

### Parar o Servidor
Pressione `CTRL + C` no terminal onde o servidor está rodando

### Reiniciar o Servidor
```powershell
cd "c:\Users\teste\OneDrive\Desktop\Standart 7"
& "C:/Users/teste/OneDrive/Desktop/Standart 7/.venv/Scripts/python.exe" manage.py runserver
```

## 🐛 Solução de Problemas

### Problema: Imagens não aparecem
**Solução**: Certifique-se de que:
1. Fez upload da imagem no admin
2. O lançamento está marcado como "Ativo"
3. O servidor está rodando

### Problema: "Page not found (404)"
**Solução**: Verifique:
1. O servidor está rodando
2. A URL está correta
3. Use o slug correto (em minúsculas, com hífens)

### Problema: Não consigo fazer login no admin
**Solução**: Use as credenciais corretas:
- Usuário: `admin`
- Senha: `admin123`

### Problema: Alterações não aparecem
**Solução**: 
1. Recarregue a página (F5)
2. Limpe o cache do navegador (Ctrl + Shift + R)
3. Verifique se salvou as alterações no admin

## 📊 Estrutura de URLs

```
/                           → Página inicial com todos os lançamentos
/lancamentos/<slug>/        → Detalhes de um lançamento específico
/admin/                     → Painel administrativo
/admin/core/lancamento/     → Gerenciar lançamentos
/admin/core/galeriaimagem/  → Gerenciar imagens da galeria
```

## 💡 Próximos Passos Sugeridos

1. **Adicionar imagens reais**: Use as imagens chicago.jpg, riviera.jpg e sky.jpg
2. **Criar mais lançamentos**: Teste adicionar seus próprios empreendimentos
3. **Testar galeria**: Adicione 5-10 fotos em cada lançamento
4. **Testar filtros**: No admin, use os filtros por cidade e status
5. **Testar busca**: Busque por nome de cidade ou bairro no admin
6. **Testar responsividade**: Abra o site no celular ou redimensione a janela

## 🎨 Personalização Rápida

### Mudar Cor Principal (Azul → Outra Cor)
Edite os templates e substitua:
- `bg-blue-600` → `bg-purple-600` (roxo)
- `text-blue-600` → `text-purple-600`
- `hover:bg-blue-700` → `hover:bg-purple-700`

Cores disponíveis: red, yellow, green, blue, indigo, purple, pink, gray

### Adicionar Logo
1. Coloque sua logo em `static/img/logo.png`
2. Edite `templates/base.html`
3. Substitua o ícone `<i class="fas fa-building"></i>` por `<img src="{% static 'img/logo.png' %}">`

### Mudar Telefone/Email no Footer
Edite `templates/base.html` na seção footer

## 📱 Recursos Implementados

✅ Design responsivo (mobile, tablet, desktop)
✅ Cards com hover effect
✅ Badges de status coloridos
✅ Galeria com efeito hover
✅ Formulários estilizados
✅ Breadcrumb de navegação
✅ Footer com informações
✅ Painel admin completo
✅ Upload de múltiplas imagens
✅ Geração automática de slug
✅ Filtros e busca no admin
✅ Ordenação por data

## 🎉 Sucesso!

Seu sistema de landing page imobiliária está **100% funcional**!

Para visualizar:
1. Certifique-se de que o servidor está rodando
2. Abra http://127.0.0.1:8000/
3. Explore os 3 lançamentos de exemplo
4. Acesse o admin e adicione imagens

Divirta-se! 🏠
