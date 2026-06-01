# Relatório de Correção Técnica - PR #168 (013_MAQUINA_DE_ATRACAO)

## Escopo da Correção
A revisão foi aplicada **estritamente** ao workflow `013_MAQUINA_DE_ATRACAO.json`.
Nenhum outro workflow, incluindo Aninha, CRM, Supabase (além da tabela específica), Orçamentos ou fluxos de publicação autônomos (08x) foram alterados. Nenhuma credencial ou API foi apagada ou recriada.

## 1. Facebook
- **O que foi corrigido:** O endpoint `/me/feed` genérico foi substituído por `https://graph.facebook.com/v20.0/{{$env.META_FACEBOOK_PAGE_ID}}/feed`, utilizando variáveis de ambiente para a identificação da página.
- **Risco mitigado:** Evita hardcoding de IDs e garante a publicação no local exato sem vazar tokens.

## 2. Instagram
- **O que foi corrigido:** O fluxo foi dividido na arquitetura oficial da Graph API:
  1. Primeiro passo (`/media`): Cria o container enviando o link da mídia (`image_url` resgatado do banco).
  2. Segundo passo (`/media_publish`): Se o container for gerado com sucesso, o n8n envia o `creation_id` para publicá-lo.
- **Variáveis aplicadas:** Foi substituído o placeholder genérico por `{{$env.META_INSTAGRAM_BUSINESS_ID}}`.
- **Risco mitigado:** A publicação do IG falharia silenciosamente ao enviar `caption` para `/media` sem criação do contêiner.

## 3. Google Business Profile
- **O que foi corrigido:** Os URLs placeholders foram parametrizados utilizando as variáveis globais de ambiente: `{{$env.GOOGLE_BUSINESS_ACCOUNT_ID}}` e `{{$env.GOOGLE_BUSINESS_LOCATION_ID}}`.
- **Risco mitigado:** Previne hardcoding e facilita a portabilidade caso as filiais mudem.

## 4. Gestão de Mídia e Condições
- **O que foi corrigido:** Adicionado um nó Postgres (`Buscar Mídia`) logo no início para buscar `media_url`.
- **Lógica adicionada:** Antes de disparar o container do Instagram, há um nó "IF IG Media". Se não houver mídia no banco, a postagem do Instagram é **pulada de forma controlada** (salvando o status `pulado_sem_midia`) e o fluxo **segue diretamente** para o Google Business, não interrompendo a cadeia.

## 5. KILLCRITIC Automático
- **O que foi corrigido:** O nó "Validar KILLCRITIC" manteve a checagem automática (sem aprovação via Telegram) verificando sete (7) condições:
  - Não contém: `visita técnica`, `Condfy`, `engenheiro`, `preço final`, `residencial`.
  - Contém obrigatoriamente as URLs da DL Soluções e o número de WhatsApp.
- **Risco mitigado:** Garante a arquitetura B2B (Condomínios) sem envolver tempo humano em validação.

## 6. Logs Individuais e Separação de Status
- **O que foi corrigido:** O workflow não sobrescreve mais a coluna `status` genérica no final de todos os nós. Foram introduzidas atualizações pontuais para as colunas: `status_facebook`, `post_id_facebook`, `erro_facebook`, `status_instagram`, e afins. O campo `tentativa_publicacao_at` é atualizado a cada interação.
- **Risco mitigado:** Previne que a falha do Google (último nó) apague a evidência de sucesso do Facebook, mantendo granularidade.

## 7. Continuidade Operacional (Obrigatória)
- **O que foi corrigido:** As lógicas encadeadas de sucesso ou erro (IF -> Postgres Update) não interrompem o fluxo (nenhum nó joga para o vazio). Independente de o status no Facebook ser marcado como `FB Sucesso` ou `FB Erro`, ambos desembocam na etapa de validação "IF IG Media". O mesmo ocorre na transição IG -> Google Business.
- **Risco mitigado:** Cumpre a regra principal: "se não está postando em 1 rede social, não pare; continue postando nas outras redes sociais."

Auditoria e edição concluídas respeitando as políticas READ-ONLY nos demais módulos.
