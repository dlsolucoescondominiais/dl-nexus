# Relatório de Localização dos Workflows Fase 2

## 1. Onde procurei
- Caminhos locais analisados: Todo o workspace `/app` (incluindo diretórios `backend/n8n/workflows` e `DL_NEXUS_V3_LOCAL/`) e pastas filhas usando `find` e `grep` recursivo.
- Repositório analisado: DL Nexus
- n8n API consultado: **Sim** (usando o host configurado em scripts e a API key).

## 2. Workflows encontrados localmente
- Nome: 001_webhook_receptor.json e 002_roteador_aninha.json
- Caminho: `/app/backend/n8n/workflows/`
- Data de modificação: Jun 12 02:12
- Parece atual ou antigo: Antigos (nenhum continha o nó "Motor Aninha V3 Atendimento").

## 3. Workflows encontrados no n8n (Remoto)
- Encontrados na API do n8n:
  - **002_roteador_aninha_v3_atendimento**
    - ID: `NgXUbJ96dXJqxGGX`
    - Active: `true`
    - UpdatedAt: `2026-06-12T02:04:49.532Z`
    - Contém Motor Aninha V3 Atendimento: **Sim**
    - Contém Chamar Gemini: **Sim**
  - **001_TELEGRAM_RECEPCAO_ANINHA_V3**
    - ID: `5NtuFZ0GXyZea9fz`
    - Active: `true`
    - UpdatedAt: `2026-06-12T02:04:50.818Z`
    - Contém Telegram Trigger: **Sim**
    - Contém Telegram Send Message: **Sim**

## 4. Divergência local x remoto
- Existe diferença? **Sim**, os locais `001_webhook_receptor.json` e `002_roteador_aninha.json` não batem com as versões remotas em execução (que possuem `_v3_atendimento` e `TELEGRAM_RECEPCAO`). O nó solicitado de fato não está no código local, apenas no remoto da nuvem!
- Qual parece ser a versão correta? A versão da API remota do n8n (`NgXUbJ96dXJqxGGX` e `5NtuFZ0GXyZea9fz`) é a correta da Fase 2.
- Risco de sobrescrever workflow funcional: Alto, se fizéssemos deploy dos arquivos `backend/n8n/workflows/001...json` sobrescreveríamos a Fase 2 funcional. É preciso aplicar as edições diretas nos downloads que acabei de fazer via API para `/tmp/`.

## 5. Próxima ação recomendada
Aplicar a correção do `jsCode` (remover duplicidades, validando o JSON) diretamente no arquivo baixado `/tmp/002_roteador_aninha_v3_atendimento.json`, fazer backups dos workflows `/tmp/001_...` e `/tmp/002_...`, validar estruturalmente e fazer upload (PUT) dos novos .json atualizados para as respectivas rotas de ID da API.
