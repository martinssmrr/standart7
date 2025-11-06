# ✅ Checklist de Deploy - Standart 7

## 📋 Pré-Deploy (No seu computador)

- [x] Código testado localmente
- [x] Arquivo `.env` criado com configurações de produção
- [x] `.gitignore` configurado
- [x] `requirements.txt` atualizado
- [x] Scripts de deploy criados
- [x] Documentação preparada
- [ ] Backup do banco de dados local (se houver dados)
- [ ] Backup das imagens/mídia local (se houver)

## 🚀 Deploy Inicial

### Acesso ao Servidor
- [ ] Acesso SSH à VPS Hostinger configurado
- [ ] Permissões de sudo/root disponíveis
- [ ] Domínio apontando para o IP do servidor

### Transferência de Arquivos
- [ ] Código enviado para `/var/www/standart7/`
- [ ] Arquivo `.env` transferido
- [ ] Banco de dados transferido (se aplicável)
- [ ] Arquivos de mídia transferidos (se aplicável)

### Execução do Deploy
- [ ] Script `deploy.sh` executado com sucesso
- [ ] Ambiente virtual criado
- [ ] Dependências instaladas
- [ ] Migrações aplicadas
- [ ] Arquivos estáticos coletados
- [ ] Permissões configuradas

### Configuração de Serviços
- [ ] Nginx configurado e rodando
- [ ] Gunicorn configurado
- [ ] Supervisor configurado
- [ ] Todos os serviços iniciados

### Configuração da Aplicação
- [ ] Superusuário criado
- [ ] Admin acessível
- [ ] Dados iniciais carregados (se necessário)

## 🔒 Segurança

- [ ] `DEBUG=False` no arquivo `.env`
- [ ] `SECRET_KEY` única gerada
- [ ] `ALLOWED_HOSTS` configurado corretamente
- [ ] `CSRF_TRUSTED_ORIGINS` configurado
- [ ] Arquivo `.env` não versionado no Git
- [ ] SSL/HTTPS configurado (Let's Encrypt)
- [ ] Certificado SSL válido
- [ ] Redirecionamento HTTP → HTTPS ativo
- [ ] Headers de segurança configurados

## 🧪 Testes Pós-Deploy

### Testes Básicos
- [ ] Site acessível via domínio
- [ ] Homepage carrega corretamente
- [ ] Imagens/CSS/JS carregam
- [ ] Links internos funcionam
- [ ] Admin acessível

### Testes Funcionais
- [ ] Login no admin funciona
- [ ] Upload de imagens funciona
- [ ] Criação de lançamentos funciona
- [ ] Criação de diferenciais funciona
- [ ] Galeria de imagens funciona
- [ ] Formulários funcionam
- [ ] Páginas de erro personalizadas (404, 500)

### Performance
- [ ] Tempo de carregamento aceitável
- [ ] Imagens otimizadas
- [ ] Cache configurado
- [ ] Compressão Gzip ativa

## 📊 Monitoramento

- [ ] Logs configurados
- [ ] Backup automático configurado
- [ ] Cron job de backup ativo
- [ ] Monitoramento de uptime (opcional)
- [ ] Alertas configurados (opcional)

## 🔄 Procedimentos de Manutenção

### Documentado
- [ ] Como fazer backup
- [ ] Como restaurar backup
- [ ] Como atualizar a aplicação
- [ ] Como acessar logs
- [ ] Como reiniciar serviços

### Scripts Prontos
- [ ] `deploy.sh` - Deploy inicial
- [ ] `update.sh` - Atualização da aplicação
- [ ] `backup.sh` - Backup manual
- [ ] Configurações de cron para backup automático

## 📱 Responsividade e Compatibilidade

- [ ] Testado em desktop
- [ ] Testado em tablet
- [ ] Testado em mobile
- [ ] Testado em diferentes navegadores
  - [ ] Chrome
  - [ ] Firefox
  - [ ] Safari
  - [ ] Edge

## 🎯 SEO e Marketing

- [ ] Meta tags configuradas
- [ ] Open Graph tags (para redes sociais)
- [ ] Favicon configurado
- [ ] robots.txt criado
- [ ] sitemap.xml gerado (se necessário)
- [ ] Google Analytics (se necessário)

## 📞 Informações de Contato

- [ ] WhatsApp configurado e funcional
- [ ] Links de contato testados
- [ ] Informações de contato atualizadas

## 🎨 Conteúdo

- [ ] Textos revisados
- [ ] Imagens otimizadas
- [ ] Lançamentos cadastrados
- [ ] Diferenciais cadastrados
- [ ] Hero section configurada
- [ ] Seção sobre configurada
- [ ] CTA de investimento configurado

## 🐛 Resolução de Problemas

### Se algo der errado:

**502 Bad Gateway**
```bash
sudo supervisorctl status standart7
sudo supervisorctl restart standart7
tail -f /var/www/standart7/logs/gunicorn_error.log
```

**500 Internal Server Error**
```bash
tail -f /var/www/standart7/logs/gunicorn.log
cd /var/www/standart7
source venv/bin/activate
python manage.py check
```

**Arquivos estáticos não carregam**
```bash
cd /var/www/standart7
source venv/bin/activate
python manage.py collectstatic --clear --noinput
sudo chown -R www-data:www-data static/
sudo systemctl reload nginx
```

## 📝 Informações do Projeto

- **Domínio**: http://oportunidadenaplanta.com.br
- **Servidor**: VPS Hostinger
- **Framework**: Django 5.2.7
- **Servidor Web**: Nginx
- **Servidor App**: Gunicorn
- **Gerenciador**: Supervisor
- **Banco de Dados**: SQLite (inicial) / PostgreSQL (recomendado)

## 🎉 Deploy Completo!

Quando todos os itens estiverem marcados, seu deploy está completo e pronto para produção!

---

**Data do Deploy**: ___/___/2025
**Responsável**: ________________
**Versão**: 1.0.0
