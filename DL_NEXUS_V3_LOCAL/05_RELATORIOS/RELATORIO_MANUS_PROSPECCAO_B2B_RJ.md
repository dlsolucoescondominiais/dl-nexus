# RELATÓRIO: Workflow n8n 130_MANUS_PROSPECCAO_B2B_RJ

## 1. Visão Geral
O workflow `130_MANUS_PROSPECCAO_B2B_RJ` foi desenvolvido como o motor de simulação de captação de leads B2B (condomínios, colégios e restaurantes) no Estado do Rio de Janeiro. Ele estrutura a captura e normalização de dados para o hub centralizado da DL Nexus V3, alimentando as próximas etapas do funil de vendas sem acionar contatos automáticos não autorizados.

## 2. Componentes e Estrutura Técnica
*   **ID Raiz do n8n:** `manusProspeccao130DlNexus20260523`
*   **Status de Atividade (Active):** `false` (Desativado conforme protocolo de segurança estrito).
*   **Nós Implementados:**
    1.  **Webhook Inicia Prospecção (GET/POST):** Ponto de entrada do fluxo, projetado para ser ativado via chamadas de agentes externos (ex. Kimiclaw) ou cron jobs futuros para prospecção ativa.
    2.  **Code Node (Simulador de Scraping):** Estrutura responsável por emular o tratamento de dados advindos do Google Places e sites institucionais, traduzindo as informações brutas para o payload estrito exigido pelo nosso banco de dados.

## 3. Conformidade de Dados e Padrões Exigidos
O payload de saída respeita estritamente o formato JSON de 17 chaves exigido pela operação DL Nexus:
1. `nome`
2. `tipo` (Condomínio, Colégio, Restaurante, etc.)
3. `bairro`
4. `cidade`
5. `endereco_publico`
6. `telefone_publico`
7. `email_institucional`
8. `site`
9. `instagram`
10. `facebook`
11. `google_business_link`
12. `dor_provavel`
13. `produto_recomendado` (Energia Solar, CFTV, Automação, Elétrica)
14. `score_oportunidade` (Definido como `0` na fase inicial de prospecção)
15. `acao_recomendada`
16. `status` (Definido como `'novo'`)
17. `observacoes`

## 4. Regras de Segurança e Semântica Cumpridas
*   **Sem Credenciais Hardcoded:** Nenhuma chave de API (Google, n8n, OpenAI) foi codificada no arquivo JSON.
*   **Automação Passiva (Safe Mode):** Nenhum nó de envio de mensagem (DM, E-mail ou WhatsApp) foi incluído para garantir 100% de compliance de aprovação do usuário.
*   **Terminologia Corrigida:** Uso estrito do termo "Avaliação Técnica" em substituição a visitas técnicas convencionais. Referências à engenharia utilizam o cargo "Responsável Técnico".

## 5. Locais de Salvamento
O fluxo finalizado e sanitizado foi exportado para os diretórios definidos de homologação, aprovação e produção local:
*   `12_N8N_WORKFLOWS_PROXIMOS\130_MANUS_PROSPECCAO_B2B_RJ.json`
*   `20_UPLOAD_N8N\130_MANUS_PROSPECCAO_B2B_RJ_FIXED.json`
*   `09_PRONTOS_PARA_PRODUCAO\130_MANUS_PROSPECCAO_B2B_RJ.json`
