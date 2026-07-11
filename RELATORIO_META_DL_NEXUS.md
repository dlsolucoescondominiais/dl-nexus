# Relatório Meta DL Nexus

Este relatório documenta a auditoria técnica e a validação de segurança da integração da Meta Graph API para a automação de postagens e atendimento na **DL Soluções Condominiais** (DL Nexus / n8n).

---

## 1. IDs Configurados

| Parâmetro | Conjunto Solicitado (Fase 1) | Conjunto Real Validado (Comunicações OK) | Observação |
| :--- | :--- | :--- | :--- |
| **FACEBOOK_PAGE_ID** | `100063696635033` | `100166804716824` | O token não possui permissão para o ID solicitado. |
| **INSTAGRAM_BUSINESS_ACCOUNT_ID** | `3136866194` | `17841403185822108` | O token não possui permissão para o ID solicitado. |

---

## 2. Tokens Encontrados e Status

- **META_ACCESS_TOKEN (no arquivo `execution/.env`):**
  - Status: **Revogado / Expirado** (Erro de validação: *Session has been invalidated because the user changed their password...*).
- **META_PAGE_ACCESS_TOKEN_DL (no arquivo `.env` principal):**
  - **Token anterior (`EAAUo98...`):** **Inválido / Incompatível** (Erro: *Invalid appsecret_proof*).
  - **Novo token detectado e alinhado (`EAF4ob...`):** **ATIVO E VÁLIDO**. Token do tipo User Token com expiração de longa duração (`expires_at: 0` - indeterminado).
- **META_APP_SECRET (no arquivo `.env` principal):**
  - Status: **Válido** (`db2b2cbb91193147c82913d5dca5cb8f`).
- **META_APP_ID_N8N_INTEGRACAO:**
  - Status: **Válido** (`26503104075966862` - aplicativo *n8n_Integracao_Nexus*).

---

## 3. Permissões Detectadas (Escopo do Token)

O token ativo e validado de longa duração (`EAF4ob...`) possui os seguintes privilégios e escopos ativos:
* `pages_manage_posts`, `pages_read_engagement`, `pages_manage_metadata`, `pages_read_user_content`, `pages_show_list`, `pages_manage_ads`, `pages_manage_engagement`, `pages_messaging`
* `instagram_basic`, `instagram_content_publish`, `instagram_manage_comments`, `instagram_manage_insights`, `instagram_manage_messages`, `instagram_shopping_tag_products`
* `business_management`, `ads_management`, `ads_read`, `leads_retrieval`, `whatsapp_business_management`, `whatsapp_business_messaging`

---

## 4. Validação dos Endpoints de Leitura

### Cenário A: Com os IDs solicitados pelo usuário (Set 1)
* **GET /me:** ✅ **SUCESSO** (Retorna `Diogo Luiz de Oliveira`, ID `27652729750993755`).
* **GET /100063696635033?fields=id,name,access_token:** ❌ **FALHOU** (HTTP 400 - *Unsupported get request. Object does not exist or missing permissions*).
* **GET /3136866194?fields=id,username,name:** ❌ **FALHOU** (HTTP 400 - *Unsupported get request*).
* **GET /100063696635033?fields=instagram_business_account:** ❌ **FALHOU** (HTTP 400 - *Unsupported get request*).

### Cenário B: Com os IDs Reais associados ao Token (Set 2)
* **GET /me:** ✅ **SUCESSO** (Retorna `Diogo Luiz de Oliveira`, ID `27652729750993755`).
* **GET /100166804716824?fields=id,name,access_token:** ✅ **SUCESSO** (Retorna Página: `DL Soluções Condominiais`).
* **GET /17841403185822108?fields=id,username,name:** ✅ **SUCESSO** (Retorna Instagram: `@dl.solucoescondominiais`).
* **GET /100166804716824?fields=instagram_business_account:** ✅ **SUCESSO** (Retorna o vínculo correto: `instagram_business_account.id = 17841403185822108`).

---

## 5. Riscos e Compliance

1. **Assinatura Exigida (App Secret Proof):** O aplicativo da Meta está configurado para **exigir assinatura** (`appsecret_proof`) em todas as chamadas de servidor (erro `GraphMethodException Code 100` ocorre se omitido). O n8n calcula isso dinamicamente no nó de verificação e no nó de publicação, garantindo conformidade.
2. **Incompatibilidade de IDs:** Utilizar os IDs solicitados (`100063696635033` / `3136866194`) causará quebra imediata da automação do n8n com erros HTTP 400. É mandatório utilizar os IDs reais validados (`100166804716824` / `17841403185822108`).
3. **Exposição de Credenciais:** O token e o secret estão devidamente protegidos no arquivo `.env` and **não estão expostos** em código duro nos workflows n8n.

---

## 6. Próximas Ações Recomendadas

1. **Atualizar Variáveis Globais de IDs:** Alterar no `.env` do servidor de produção as variáveis para apontar para a infraestrutura real:
   ```env
   FACEBOOK_PAGE_ID=100166804716824
   INSTAGRAM_BUSINESS_ACCOUNT_ID=17841403185822108
   ```
2. **Reinicializar/Recarregar Variáveis no n8n:** Certificar-se de que o contêiner do n8n carregou o arquivo `.env` principal atualizado.
3. **Executar Teste em Sandbox (DRY RUN):** Ativar a automação em modo de rascunho sem publicar de fato nas redes sociais para verificar a montagem correta dos payloads de imagem e copy do robô.
