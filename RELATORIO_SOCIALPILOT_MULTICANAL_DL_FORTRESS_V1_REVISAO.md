# 📋 Relatório de Revisão Técnica — SocialPilot Multicanal DL Fortress v1

Este documento oficializa as correções de arquitetura, banco de dados e compliance social realizadas antes do início dos testes em ambiente de produção para a **DL Soluções Condominiais**.

---

### 1. 🔑 Gerenciamento de Tokens de Acesso
- Substituição técnica de expressões obsoletas: o termo *"Token de Longa Duração Eterno / Never Expire"* foi inteiramente descontinuado na documentação técnica, sendo adotada a nomenclatura oficial: **"token de sistema/longa duração com verificação preventiva"**.
- Criamos o workflow de suporte [SOCIAL_VERIFICADOR_TOKEN_META.json](file:///D:/AntiGravity/projeto_01/DL_NEXUS_V3_LOCAL/12_N8N_WORKFLOWS_PROXIMOS/SOCIAL_VERIFICADOR_TOKEN_META.json). Este fluxo roda todas as segundas-feiras às 07:00 AM, realiza uma consulta de validação preventiva no endpoint `/me` da Graph API do Facebook e dispara alertas críticos imediatos no Telegram se o token falhar ou expirar.

---

### 2. 🗄️ Modelagem de Banco de Dados Revisada (`dl_social_publicacoes`)
Para suportar logs granulares por canal sem poluir a tabela de metadados, as seguintes colunas foram migradas para o tipo **`JSONB`**:
* `hashtags`: lista de tags estruturadas em JSON.
* `bloqueios`: array com todas as violações de compliance detectadas.
* `erros`: mapeamento de chave-valor contendo erros por canal (ex. `{"instagram": "error text"}`).
* `tentativas`: contagem de execuções por canal (ex. `{"instagram": 1, "facebook": 2}`).
* `publicado_em`: timestamp de envio por canal (ex. `{"instagram": "2026-06-11T..."}`).
* Adicionada a coluna **`status_global`** `VARCHAR(50)` para controle centralizado.

---

### 3. 🎯 Padronização de Estados do Ciclo de Vida (`status_global`)
O ciclo de vida de cada postagem segue a seguinte máquina de estados oficial:
1. `rascunho_planejado`: Conteúdo básico criado pelo planejador diário.
2. `gerado`: Textos específicos gerados pela IA para cada rede social.
3. `bloqueado_revisao`: Post reprovado nas verificações de compliance do KILLCRITIC.
4. `pronto_para_publicar`: Aprovado pelo revisor automático.
5. `publicado_parcial`: Sucesso no envio para ao menos um canal ativo, com outros falhando.
6. `publicado_total`: Sucesso total de publicação em todos os canais com credenciais configuradas.
7. `falhou_total`: Erro técnico de publicação em todos os canais ativos.
8. `pendente_credencial`: Canais com credenciais em aberto (LinkedIn, TikTok, GMB) que não falharam, mas aguardam configuração.

---

### 4. 📢 Regras Específicas por Rede Social

#### A. Google Business Profile (GMB)
- Mantido estritamente como **pendente** até que a autorização OAuth2 esteja fisicamente conectada no n8n.
- Não expõe portfólios ou dados de catálogos na interface de busca local.
- Utiliza posts curtos focados no público local, com CTA `LEARN_MORE` ou `CALL` apontando para o site institucional.

#### B. TikTok
- Mantido como **pendente/assistido** até que haja arquivos de vídeo vertical e credenciais ativas.
- O fluxo gera dinamicamente roteiros, ganchos magnéticos, textos para sobreposição de tela, legenda e hashtags dedicadas, sem travar as postagens normais de outras redes.

#### C. LinkedIn
- Mantido como **pendente** até a configuração da página de organização.
- Escreve textos com linguagem estritamente institucional, focado em tom corporativo e institucional, focado em gestores, síndicos, administradoras e facilities (riscos, previsibilidade e gestão de facilities), nunca reaproveitando a legenda informal e com hashtags do Instagram.

---

### 5. ⚠️ Compliance Avançado (KILLCRITIC Social v2)
O validador automatizado bloqueia posts de forma preventiva caso detecte:
1. **Sensacionalismo de Tragédia/Notícia:** Palavras como *morte, catástrofe, pânico, desespero, tragédia* e *incêndio fatal* são bloqueadas para evitar vendas baseadas em pânico.
2. **Promessas Absolutas/Comerciais Proibidas:** *"token eterno"*, *"never expire"*, *"garantia eterna"*, *"100% garantido"*, *"sem risco"*, *"preço final"*, *"última chance"*, *"urgente demais"*.
3. **Falta de Dados em Notícias:** Posts baseados em notícias externas são sumariamente rejeitados se faltar `fonte_nome`, `fonte_url`, `fonte_data_consulta`, `resumo_fonte`, `comentario_tecnico_dl` ou `produto_dl` relacionado.

---

### 🏆 Conclusão e Estado de Preparação

* **workflows revisados:** SIM (os arquivos foram atualizados com os novos modelos de JSONB e status_global).
* **migração SQL ajustada:** SIM (o script de migração foi redefinido).
* **pronto para dry run:** SIM (o fluxo local está validado).
* **pronto para produção:** NÃO (pendente de resolução da conectividade de DNS local para rodar a migração no Supabase e de configurar as conexões OAuth2 ativas do Google, TikTok e LinkedIn no painel n8n).
