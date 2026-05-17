# Relatório de Plano de Deploy Dinâmico N8N

**Data:** 2026-05
**Contexto:** DL Nexus V3

## Visão Geral

Este documento descreve a nova estratégia de deploy dinâmico e seguro para workflows do n8n na DL Soluções Condominiais.

O objetivo é evitar erros passados de corrupção ou quebra de fluxos de produção (como o incidente com o workflow ID faltante ou credenciais vazadas) e garantir a conformidade estrita com o protocolo KILLCRITIC.

## Pipeline de Deploy

1. **Staging Local**: Workflows prontos para deploy são copiados manualmente para `DL_NEXUS_V3_LOCAL/20_UPLOAD_N8N/`.
2. **Validação Automática**: O script `deploy_n8n_workflows.sh` (ou `.ps1`) roda o script de validação `validar_killcritic_v3.py` na pasta de upload.
   * Verifica a existência de chaves vitais (`id`, `name`, `nodes`, `connections`).
   * Verifica `active: false` obrigatório para injeção inativa.
   * Verifica regras lexicais do KILLCRITIC ("visita técnica", etc).
   * Varre por chaves de `api_key`, `token` ou `password`.
3. **Simulação de Importação**: O script gera os comandos do `docker exec -it n8n-main n8n import:workflow`.
4. **Deploy Manual e Consciente**: Os comandos gerados são copiados e colados no servidor de produção pelo responsável.

## Estrutura de Pastas (Base `DL_NEXUS_V3_LOCAL`)

- `/00_BACKUP_N8N`: Arquivos JSON de backup exportados do n8n antes de novos deploys.
- `/05_RELATORIOS`: Relatórios de auditoria e execução.
- `/20_UPLOAD_N8N`: Área de staging final dos arquivos `.json` que passarão pelo processo de CI de deploy.
- `/30_DEPLOY_N8N`: Scripts de execução e de rollback.

## Nota sobre 135 Workflows Legados

Foi decidido que os 135+ workflows gerados em modo "scaffold" no backend/ não fazem parte do deploy real atual e são mantidos separados na tarefa de inventário legada. Apenas workflows manualmente inseridos na pasta `/20_UPLOAD_N8N/` serão afetados por este plano.
