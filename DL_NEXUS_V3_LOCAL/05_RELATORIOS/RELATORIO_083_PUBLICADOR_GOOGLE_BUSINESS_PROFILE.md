# Relatório: 083_PUBLICADOR_GOOGLE_BUSINESS_PROFILE

**Nome do Workflow:** 083_PUBLICADOR_GOOGLE_BUSINESS_PROFILE
**Objetivo:** Publicar no Google Meu Negócio / Perfil da Empresa após aprovação.

**Funcionalidades:**
- Recebe a requisição aprovada (`approved=true`).
- Valida contra as regras rigorosas do KILLCRITIC.
- Posta um `LocalPost` via Google API.
- Associa o CTA `LEARN_MORE` ao link do Google (`https://share.google/NGEzAoHXg890EjyiR`).
- Autenticação configurada via credencial n8n `googleApi` (OAuth).

**Segurança:**
- Nenhum token no Body/Header.
- Fluxo restrito por `active=false`.
- Validação raiz pelo KILLCRITIC garantindo integridade e reputação.
