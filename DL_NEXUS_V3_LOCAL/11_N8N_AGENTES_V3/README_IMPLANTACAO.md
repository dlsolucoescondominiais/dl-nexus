# DL Nexus V3  n8n com Agentes

Este pacote cria a base lógica dos workflows do n8n para coordenar:

- Aninha: atendimento e triagem.
- Diego: técnico e roteador.
- SocialPilot: postagens e marketing.
- Canais: WhatsApp, Telegram, Instagram Direct, Facebook, Google Meu Negócio, site e e-mail.
- Receita principal: contratos recorrentes para condomínios e colégios/escolas.

## Arquivos

000_DL_NEXUS_ORQUESTRADOR.json
Workflow central que recebe mensagens por webhook e decide se a demanda é atendimento, técnica ou postagem.

030_AGENT_ANINHA_ATENDIMENTO.json
Workflow de triagem de atendimento.

031_AGENT_DIEGO_TECNICO.json
Workflow técnico.

080_AGENT_SOCIALPILOT_POSTAGENS.json
Workflow para gerar conteúdo de marketing para aprovação humana.

## Regra de implantação

1. Importar primeiro o 000_DL_NEXUS_ORQUESTRADOR no n8n.
2. Testar via webhook manual.
3. Importar Aninha, Diego e SocialPilot.
4. Não conectar Meta, TikTok ou Google Meu Negócio antes dos testes manuais.
5. Toda publicação deve iniciar com aprovação humana.

## KILLCRITIC

Termos proibidos:
- visita técnica
- visita
- agendar visita
- canaleta plástica
- manutenção hidráulica pura

Termos obrigatórios:
- Avaliação Técnica
- infraestrutura profissional
- contrato recorrente
- setup separado da mensalidade
