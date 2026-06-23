# PLANO_SUBSTITUICAO_MANUS_DL

## 1. Visão Geral da Substituição
O ecossistema DL Nexus (orçamentos, prospecção e postagens) possuía o `Manus.IA` no centro da prospecção outbound e planejamento diário de mídia B2B. A remoção visa otimizar custos e garantir solidez baseada em modelos comprovados via APIs robustas e nós nativos do n8n.

## 2. Modelos Substitutos
- **DeepSeek (Raciocínio Lógico e Geração Longa):** Assumirá a responsabilidade do Manus para estruturação de dados complexos, parseamento profundo e a "mente" do Agente Outbound. Seu custo reduzido e capacidade de codificação são ideais.
- **Gemini Flash (Classificação de Alta Velocidade):** Roteamentos do tipo "Classificador de Cliente", "Scoring Rápido" e "Revisor Textual" serão direcionados ao Gemini Flash para não onerar pipelines.
- **Lógica Interna n8n (Roteamento Switch/If):** Todo planejamento complexo (antigo Cron Manus) será refatorado usando Swithes/Ifs nativos com HTTP Requests diretos, eliminando "agentes em caixa preta".

## 3. Ações Técnicas nas Esteiras
- **Prospecção Ativa (Workflow 060):** Substituir o nó de geração do Manus por um `httpRequest` para a API da OpenAI/DeepSeek com prompt focado em *Prospect* de Síndicos/Administradoras.
- **Scoring (Workflow 131):** Utilizar o nó "Basic LLM" configurado para Gemini.
- **Cron Diário (Workflow 070):** O workflow não chamará o Manus para "pensar no dia", mas ativará triggers cron que invocam pipelines menores de conteúdo ou prospecção com base na inteligência embutida no Supabase + DeepSeek.

## 4. Banco de Dados (Supabase)
Nenhuma tabela será excluída. O histórico das memórias geradas pelo Manus permanecerá inalterado para servir de RAG aos novos modelos (DeepSeek).
