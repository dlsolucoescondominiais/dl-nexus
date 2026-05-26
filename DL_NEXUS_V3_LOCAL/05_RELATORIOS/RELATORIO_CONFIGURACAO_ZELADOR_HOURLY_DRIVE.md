# Configuração: Zelador Hourly Drive

**Arquivo de Configuração:** `dl_nexus_google_drive_midia_config.json`

## Parâmetros Críticos Aplicados
- `modo_execucao`: DRY_RUN
- `frequencia`: hourly
- `limite_por_execucao`: 50
- `processar_subpastas`: true
- `nao_apagar_originais`: true
- `nao_mover_originais_em_dry_run`: true
- `nao_renomear_originais_em_dry_run`: true

## Lista de Origens (IDs)
O agente está configurado para inspecionar passivamente os 28 diretórios (e possivelmente subdiretórios) fornecidos no arquivo de configuração, que formam o INVENTÁRIO_GERAL do sistema.
