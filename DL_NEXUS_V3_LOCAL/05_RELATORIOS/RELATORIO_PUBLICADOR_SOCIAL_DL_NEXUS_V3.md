# Relatório de Governança e Implementação - Publicador Social DL Nexus V3

**Data de Validação:** 18 de Maio de 2026  
**Finalidade:** Esteira assistida de postagem social para Facebook, Instagram e Telegram, projetada para evitar alucinações de IA e garantir a adoção estrita das regras KILLCRITIC, exigindo **obrigatoriamente aprovação humana** antes de qualquer publicação.

## Arquivos Criados
- `DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS\020_PUBLICADOR_SOCIAL_DL_NEXUS_V3_APROVACAO.json`
- `DL_NEXUS_V3_LOCAL\20_UPLOAD_N8N\020_PUBLICADOR_SOCIAL_DL_NEXUS_V3_APROVACAO_config.json`

## Arquitetura de Validação e Bloqueios (KILLCRITIC)
O motor foi estruturado para **não agir autonomamente em produção**.
1. **Verificação Léxica:** Qualquer conteúdo contendo "visita técnica", "preço final", "hidráulica pura" ou afins é sumariamente vetado pela rotina "KILLCRITIC Social".
2. **Força Tática:** É obrigatória a presença do termo "Avaliação Técnica" no Call to Action (CTA). Caso contrário, o workflow reporta falha.
3. **Approval Webhook:** Se o post passar pela triagem semântica, ele ficará represado no nó de "Wait" do n8n até receber o payload de liberação através do endpoint `/webhook/aprovar-post-dl-nexus-v3`.

## Credenciais Esperadas (Sem Exposição de Tokens Locais)
Foram utilizadas exclusivamente as strings de mapeamento para as credenciais já existentes no seu cofre do n8n (HostGator):
* `Conta OpenAi` (Geração de Conteúdo)
* `Conta do Telegram` (Avisos, Triagem e Postagem)
* `Aplicativo do Facebook` (API Graph para FB e IG)
* `SMTP - Suporte DL` (Envio de Relatórios Operacionais)

## Pontos Críticos e Campos Pendentes
Ao importar o workflow via interface do n8n, você precisará preencher as seguintes tags de espaço reservado (Placeholders):
1. **`CHAT_ID_AQUI`** - Nos nós do Telegram.
2. **`PAGE_ID_AQUI`** - No nó da API do Facebook.
3. **`INSTAGRAM_BUSINESS_ACCOUNT_ID_AQUI`** - Nos nós da API do Instagram.

## Como Importar e Testar
1. Acesse seu n8n (`https://n8n.dlsolucoescondominiais.com.br`).
2. Vá em **Workflows** > **Import from File**.
3. Selecione o arquivo `020_PUBLICADOR_SOCIAL_DL_NEXUS_V3_APROVACAO_config.json` gerado na pasta `20_UPLOAD_N8N`.
4. Preencha os campos pendentes (IDs do Meta e Telegram).
5. O workflow importa com a flag **`active: false`**.
6. **Teste seguro:** Clique em "Execute Workflow". O workflow deve parar no nó "Wait Aprovação Webhook". Envie um POST manual para o webhook de liberação com `{"decisao": "aprovar"}` para confirmar que a cadeia transacional inteira funciona sem ativar o gatilho geral.

## Confirmações de Segurança
- **Status `active=false`:** Garantido ✅
- **Sem exposição de segredos:** Nenhum token foi imputado nos arquivos locais ✅
- **Integridade dos Receptores Legados:** Intocados (`000_meta`, `001_webhook`, routers v3) ✅
- **Nenhum Deploy Automático Realizado:** Validação estritamente local. Tudo seguro. ✅
