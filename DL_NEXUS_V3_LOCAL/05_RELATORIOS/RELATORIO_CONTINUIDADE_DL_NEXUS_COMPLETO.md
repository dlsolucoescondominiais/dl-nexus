# RELATORIO DE CONTINUIDADE DL NEXUS V3 COMPLETO

## 1. O que já existe
- `002_roteador_aninha_v3_killcritic`: O roteador principal de atendimento, qualificação de personas e encaminhamento.
- `000_email_receptor_v3_hostgator`
- `000_meta_receptor_v3`
- `001_webhook_receptor_v3`
- `001_webhook_receptor_enterprise_v3`
- `001A_normalizador_payload_v3`
- `005_roteador_jules_v3_auditor`
- `006_notificações_v3`
- `007_tarefas_fundo_v3`
- `008_mcp_server_v3`
- `014_manychat_receptor_v3`

## 2. O que foi duplicado e preparado nesta etapa
- **`003_roteador_diego_v3_killcritic`**: Criado a partir da v2. Atualizado com as regras do protocolo KILLCRITIC (nunca gerar preço final, nunca dar visita técnica, separar hidráulica de automação, etc.) e abrangendo todas as especialidades técnicas exigidas (elétrica, CFTV, controle de acesso, infra, solar, bombas, etc.).
- **`004_skill_router_dl_nexus_v3`**: Criado a partir da v2. Atualizado para funcionar como um nó Switch (Skill Router) abrangendo as 15 skills obrigatórias: `vendas_condominios`, `suporte_eletrico`, `suporte_cftv`, `controle_acesso`, `infra_redes`, `solar_baterias`, `solar_conexao_placas`, `solar_hibrida`, `automacao_condominio`, `comandos_eletricos`, `postagem_social`, `orcamentacao_suprimentos`, `field_ops_dispatcher`, `customer_success`, `dba_supabase`.

## 3. O que falta conectar
Falta conectar os outputs do Skill Router (`004_skill_router_dl_nexus_v3`) e os roteamentos internos do `003_roteador_diego_v3_killcritic` para os respectivos workflows especializados (como os geradores de orçamento, workflows de vendas, etc.), bem como conectar o Diego V3 ao Supabase e ao Skill Router de forma fluida.
Os fluxos específicos para CRM, Drive, SocialPilot e Procurement ainda não estão integrados nos roteadores centrais atuais.

## 4. Quais workflows não devem ser mexidos
Os workflows receptores e de fundação **NÃO devem ser alterados** no momento e devem ser mantidos como estão para não quebrar a produção:
- `000_meta_receptor`
- `000_email_receptor`
- `014_manychat_receptor`
- `001_webhook_receptor`
- `006_notificações`
- `008_mcp_server`

## 5. Como os receptores antigos se conectam ao núcleo V3
Os receptores antigos (ex: webhooks legados) deverão enviar suas cargas (payloads) para o `001A_normalizador_payload_v3`. Esse normalizador tratará a entrada para que tenha um formato unificado, despachando então a requisição formatada para o `002_roteador_aninha_v3_killcritic` ou diretamente para o `003_roteador_diego_v3_killcritic`, que farão o trabalho de triagem usando os novos agentes.

## 6. Próximos workflows a criar
É necessário desenvolver os workflows periféricos e de backoffice:
- Série 019-023: Gerador de orçamentos e integrações com o Manus (Leads, Posts, Propostas, Status).
- Série 030-031: Classificador de emails do Hostgator e envio aprovado por SMTP.
- Série 040-043: Interações diretas com o Supabase (Leads, Propostas, Conversas, Logs).
- Série 050-051: Gestão de arquivos no Google Drive (Midia, Datasheets, Propostas, Relatórios).
- Série 060-065: Integrações com SocialPilot para geração e publicação de posts.
- Série 070-073: Fluxos internos (Procurement, Dispatcher, Customer Success, DBA).

## 7. Ordem segura de publicação
1. Publicar localmente e testar em sandbox.
2. Ativar `004_skill_router_dl_nexus_v3` como workflow sub-rotina passivo.
3. Ativar `003_roteador_diego_v3_killcritic` de forma espelhada ou recebendo chamadas específicas de teste do normalizador.
4. Conectar gradualmente as skills do 004 aos workflows especializados conforme forem sendo construídos.
5. Após validar Aninha V3 e Diego V3, redirecionar todo o tráfego do `001A_normalizador_payload_v3` para os novos roteadores.
