# 📋 Auditoria Técnica: Workflows n8n (DL Nexus)

**Data da Auditoria:** 24 de Abril de 2026
**Objetivo:** Identificar anti-patterns, nós quebrados, variáveis inexistentes e falhas de roteamento interno nos arquivos JSON da infraestrutura do n8n (`backend/n8n/workflows/`).

---

## 🛑 1. Anti-Pattern de Roteamento Interno (Grau de Risco: Alto)

Foi identificado um erro crítico de arquitetura em vários workflows: eles estão utilizando a **URL externa** do proxy Caddy/Cloudflare (`https://n8n.dlsolucoescondominiais.com.br`) para fazer chamadas HTTP de um workflow para outro.

**Por que isso é um erro?**
Isso força a requisição a sair da rede interna do Docker, ir até a internet (Cloudflare), resolver o DNS, descer pelo proxy reverso (Caddy) e entrar novamente no container do n8n. Isso gera latência desnecessária (overhead) e cria um ponto de falha absurdo: se a internet da HostGator cair ou o Cloudflare oscilar, os agentes do n8n não conseguem "conversar" entre si, mesmo estando no mesmo servidor.

**Arquivos Afetados:**
*   `002_roteador_aninha.json` (Node: "Chamar Especialista")
*   `003_roteador_diego.json` (Node: "Chamar Técnicos (004)")
*   `004_roteador_agentes_especializados.json` (Node: "Notificar Diogo (006)")
*   `005_roteador_jules.json` (Node: "Notificar (006)")

**Correção Imediata (Obrigatória):**
Alterar todos os `httpRequest` Nodes para utilizar a URL interna da rede Docker:
Substituir: `https://n8n.dlsolucoescondominiais.com.br/webhook/...`
Por: `http://n8n:5678/webhook/...`

---

## ⚠️ 2. Inconsistência de Rotas (Grau de Risco: Médio)

Foi detectada uma inconsistência no encadeamento dos Agentes.

*   No arquivo `004_roteador_agentes_especializados.json`, o webhook de entrada chama-se `dl-especialistas` e o nome do agente é "Jules".
*   No arquivo `005_roteador_jules.json`, o webhook de entrada chama-se `dl-jules` e o fluxo aponta direto para o notificador.

Parece haver uma redundância ou confusão de nomenclatura entre o "Especialista Jules" (workflow 004) e o "Roteador Jules" (workflow 005). Isso pode causar loops infinitos ou perda de leads no pipeline comercial (Supabase).

---

## 🔑 3. Dependência de Credenciais não Abstraídas (Grau de Risco: Baixo)

Alguns workflows (como o `003` e `004`) chamam o Supabase usando o ID de credencial estático `"QzziIRhKJMDNAE1m"`. Se esse JSON for importado em uma nova instância do n8n (ex: ambiente de homologação), as credenciais quebrarão imediatamente, pois os IDs são gerados dinamicamente no banco de dados SQLite interno de cada n8n.

**Boas Práticas:**
No ambiente de Produção isso funcionará (desde que a credencial com esse ID exista), mas caso migre a infraestrutura, será necessário recadastrar o Node.

---

## ✅ Conclusão e Próximos Passos

Para que a operação da DL Nexus fique 100% otimizada, resiliente e siga as diretrizes arquiteturais (Zone 1):

1.  **Ação Imediata:** Devo rodar um script de substituição em massa (via `sed`) em todos os arquivos JSON para trocar o roteamento de domínio público para `http://n8n:5678`.
2.  **Ação Secundária:** Precisamos que você (Engenheiro) revise qual é o papel exato do workflow `005_roteador_jules` contra o `004_roteador_agentes_especializados`, pois as responsabilidades estão sobrepostas.
