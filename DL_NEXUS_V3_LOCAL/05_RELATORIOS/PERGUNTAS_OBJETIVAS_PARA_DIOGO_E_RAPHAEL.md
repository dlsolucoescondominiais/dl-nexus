# Perguntas Objetivas para Diogo e Raphael - DL Nexus V3

Este questionário visa coletar as informações estritamente necessárias para tornar o DL Nexus V3 operacional, seguro e alinhado aos objetivos comerciais da DL Soluções Condominiais.

---

## Para Diogo Responder (Negócios, Operações e Limites)

### 1. Metas Comerciais e Volume
* Qual é a meta mensal de faturamento esperada através do DL Nexus?
* Qual a meta mensal de fechamento de contratos recorrentes (DL Partner)?
* Qual o ticket médio desejado global e por produto principal?
* Qual é o volume de leads diários que a equipe tem capacidade de absorver?
* Quantas propostas devem ser enviadas semanalmente (idealmente)?

### 2. Preços e Custos
* Qual a margem mínima aceitável por produto/serviço?
* Qual é o preço mínimo admissível para um projeto de portaria Fortress?
* Qual é o custo estimado de hora/equipe técnica e o custo de deslocamento padrão?
* Quais os custos reais mensais/anuais de licenças das plataformas (Condfy, Metabo, Mobgate, etc)?

### 3. Operação e Atendimento
* Quem será o responsável primário por responder/assumir o atendimento humano no WhatsApp?
* Quem tem a palavra final para aprovar posts nas redes sociais?
* Quem é o responsável final pela aprovação das propostas geradas?
* Quem será a equipe designada para executar o serviço de campo (Avaliação Técnica e Implantação)?
* Quantos chamados/dia a equipe técnica de campo da DL suporta atualmente?
* Quais são os horários oficiais de atendimento (ex: 08h-18h)? Há SLA diferente para DL Partner?

### 4. Limites de SLA e Prioridades
* Qual o tempo máximo aceitável para a primeira resposta a um lead?
* Qual o tempo máximo admissível para entrega de um orçamento preliminar (após coleta de dados)?
* Qual o prazo máximo ideal para agendamento e execução de uma Avaliação Técnica?
* Confirmando a regra KILLCRITIC: Que tipos de serviços *não* devem ser aceitos de forma alguma (ex: hidráulica pura)?
* Quais as regiões/bairros/cidades prioritárias para atuação no momento?

### 5. Autorizações para os Agentes de IA
* Os agentes têm permissão para publicar automaticamente em redes sociais, ou tudo deve ir para uma fila de aprovação (draft)?
* Os agentes têm permissão para responder automaticamente a dúvidas técnicas de clientes conhecidos no WhatsApp (Tier 1 Support)?
* Até onde vai a autonomia para fechar um preço sem passar por aprovação humana (após a Avaliação Técnica)?

---

## Para Raphael Responder (Técnico, Credenciais e Infraestrutura)

### 1. Status Real de Credenciais
* As credenciais IMAP/SMTP (HostGator/Titan) estão ativas, testadas e prontas para uso em produção?
* Qual o status real da conexão com a API Oficial do Meta/WhatsApp para o número 21 99269-8612? (É WABA Cloud API? O token é permanente? Qual o ID do número?)
* As credenciais do Telegram Bot estão validadas e funcionais?
* Redes Sociais: Existe conexão ativa (via OAuth ou Token) para Instagram, Facebook Page/Business Manager, TikTok e Google Meu Negócio?
* As APIs de inteligência artificial (ElevenLabs, DeepSeek, Kimi/KimiClaw/PicoClaw, Manus) estão com saldo e chaves de produção ativas no n8n?

### 2. Status Real do Google Drive
* O n8n tem acesso de gravação e leitura à estrutura do Google Drive? (Usa Service Account ou OAuth pessoal?)
* A estrutura de pastas `DL_NEXUS_MIDIA_E_DATASHEETS` existe e qual é o ID da pasta raiz?

### 3. Status Real do Supabase (Banco de Dados)
* A estrutura de tabelas mínima existe? (`leads`, `clientes`, `propostas`, `chamados`, `posts`, `logs`)
* As políticas de segurança (RLS) estão ativadas no Supabase para evitar vazamento de dados via API anônima?
* Onde e como o n8n está gravando os dados hoje (qual a URL e qual chave está sendo usada nos nodes)?

### 4. Status Operacional do n8n (https://n8n.dlsolucoescondominiais.com.br)
* Quais workflows estão rodando como "Ativo" neste exato momento?
* Qual a causa raiz dos erros reportados no workflow `007_tarefas_background`?
* Quais nodes específicos nos workflows V3 importados (`002`, `003`, `004`) já possuem credenciais de produção configuradas de verdade e quais estão vazios/mockados?
