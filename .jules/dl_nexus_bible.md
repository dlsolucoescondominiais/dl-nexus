# BÍBLIA ARQUITETURAL DO PROJETO DL NEXUS

## 1. IDENTIDADE E REGRA DE NEGÓCIO
- **Empresa:** DL Soluções Condominiais.
- **Região:** Zonas Sul, Sudoeste, Oeste e Norte do Rio de Janeiro.
- **Liderança:** Diogo Luiz de Oliveira (Tecnólogo em Infraestrutura e Pós-Graduado em Energia Solar). *PROIBIDO uso do termo "engenheiro".*
- **Pilares:** Elétrica, Energia Solar Híbrida, Mobilidade / CVE, Segurança Eletrônica, Prevenção de Incêndio.
- **Objetivo:** Máquina autônoma de captação, triagem, avaliação técnica, relacionamento, orçamento e fechamento de vendas.

## 2. ARQUITETURA TÉCNICA (AS 4 CAMADAS)
- **CAMADA 1 (Frontend):** React + Vite + TailwindCSS no Render (nexus.dlsolucoescondominiais.com.br). Interfaces: Portal do Síndico, Dashboards (Técnico, Comercial), Mobile Checklist, Painéis.
- **CAMADA 2 (Orquestração):** n8n self-hosted via Docker na HostGator. Webhooks exigem HeaderAuth. Retries e fallbacks obrigatórios.
- **CAMADA 3 (Cérebro IA):** FastAPI (Antigravity) na HostGator. Agentes: Aninha (Triagem/Roteamento), Diego (Orquestração Técnica), Agentes Técnicos. Integrações protegidas e com controle de rate limit/cache.
- **CAMADA 4 (Banco de Dados):** Supabase PostgreSQL. Regras: uuid-ossp, RLS estrito, Realtime, soft deletes, audit logs.

## 3. O FLUXO DO CRM
- Estágio 0: Atração (Posts automáticos via n8n).
- Estágio 1: Entrada (Multicanal).
- Estágio 2: Triagem (Aninha qualifica e salva no Supabase).
- Estágio 3: Gestão (Realtime no React Dashboard).
- Estágio 4: Campo (Checklist mobile pelos técnicos).
- Estágio 5: Fechamento (Agente Python gera proposta PDF -> n8n envia para orcamentos@ e cliente).
- Estágio 6: Pós-venda (Follow-up automático, renovação).

## 4. DIRETRIZES DE CÓDIGO
1. Sem caminhos hardcoded do Windows (ex: C:/, D:/). Usar env vars e paths relativos.
2. Webhooks e endpoints protegidos (HeaderAuth, JWT, CORS).
3. Logs, retries e fallbacks obrigatórios.
4. Código modular, multi-tenant e desacoplado.
5. Sem placeholders. Entregas completas, funcionais e otimizadas.
