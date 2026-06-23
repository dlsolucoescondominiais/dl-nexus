# MANUAL OPERACIONAL — 151_MAQUINA_CONTEUDO_META_DL_4X_DIA

> **Versão:** 1.0  
> **Data:** 2026-06-23  
> **Autor:** DL Nexus V3 — Engenharia de Integração  
> **Classificação:** Interno / Operacional  

---

## Índice

1. [Visão Geral](#1-visão-geral)
2. [Matriz de Pautas Semanais](#2-matriz-de-pautas-semanais)
3. [Variáveis de Ambiente Obrigatórias](#3-variáveis-de-ambiente-obrigatórias)
4. [Fluxo de Execução](#4-fluxo-de-execução)
5. [Regras de Conteúdo](#5-regras-de-conteúdo)
6. [Regras de Imagem](#6-regras-de-imagem)
7. [KILLCRITIC](#7-killcritic)
8. [Linha Editorial Baseada em Notícia](#8-linha-editorial-baseada-em-notícia)
9. [Formato Carrossel](#9-formato-carrossel)
10. [Publicadores Downstream](#10-publicadores-downstream)
11. [Troubleshooting](#11-troubleshooting)

---

## 1. Visão Geral

O workflow **151_MAQUINA_CONTEUDO_META_DL_4X_DIA** é a máquina autônoma de geração e publicação de conteúdo para **Facebook** e **Instagram** da **DL Soluções Condominiais LTDA**.

### Características Principais

| Atributo | Valor |
|---|---|
| **Frequência** | 4 publicações por dia |
| **Horários programados** | 08:00, 12:00, 18:00, 20:00 (horário de Brasília) |
| **Trigger alternativo** | Webhook manual (para testes e publicações emergenciais) |
| **Plataformas alvo** | Facebook Page + Instagram Business |
| **Modo padrão** | Publicação automática (`AUTO_PUBLISH_META=true`) |
| **Aprovação humana** | Opcional (via workflow 020) |
| **Geração de imagem** | Via provedor configurável (Gemini Imagen / DALL-E / Flux) |
| **Validação de conteúdo** | KILLCRITIC integrado (barreira obrigatória) |
| **Registro** | Supabase (histórico de publicações) |

### Objetivo

Manter presença digital constante e profissional nas redes Meta, posicionando a DL Soluções como referência técnica em:
- Segurança eletrônica (CFTV)
- Infraestrutura elétrica predial
- Controle de acesso e portaria autônoma
- Equipamentos comerciais
- Energia solar e backup
- Prevenção e manutenção hidráulica
- Contratos de manutenção recorrente

---

## 2. Matriz de Pautas Semanais

A máquina de conteúdo segue um **cronograma temático semanal fixo**, garantindo cobertura equilibrada de todas as linhas de negócio da DL Soluções.

| Dia da Semana | Linha DL | Temas Abordados | Público-alvo Principal |
|---|---|---|---|
| **Segunda-feira** | **DL Guardião** | CFTV, câmeras IP, pontos cegos, gravação em nuvem, acesso remoto, monitoramento 24h, analíticos de vídeo | Síndicos, gestores de facilities |
| **Terça-feira** | **DL Volt** | Elétrica predial, quadros de distribuição, bombas, iluminação de áreas comuns, comandos elétricos, adequação NR-10 | Síndicos, administradoras |
| **Quarta-feira** | **DL Fortress** | Controle de acesso, portaria autônoma, biometria facial, tags RFID, catracas, interfones IP, integração com aplicativos | Síndicos, construtoras |
| **Quinta-feira** | **DL Express** | Chapas elétricas, grills, fritadeiras industriais, equipamentos para restaurantes, lanchonetes, confeitarias, padarias | Donos de estabelecimentos comerciais |
| **Sexta-feira** | **DL EcoVolt / DL VoltCharge** | Energia solar fotovoltaica, Lei 14.300, backup com baterias, nobreaks, carregadores de veículos elétricos, gestão energética | Síndicos, gestores de sustentabilidade |
| **Sábado** | **DL Alerta / DL Acqua** | Prevenção de incêndios, manutenção de bombas, caixas d'água, cisternas, sensores de nível, automação hidráulica | Síndicos, zeladores |
| **Domingo** | **DL Partner** | Manutenção recorrente, contratos SLA, checklist mensal, relatórios de manutenção, disponibilidade 24/7, planos de atendimento | Síndicos, administradoras |

### Observações sobre a Matriz

- A linha editorial é **automática**: o nó de geração de conteúdo recebe o dia da semana via `new Date().getDay()` e seleciona a pauta correspondente.
- É possível forçar uma pauta diferente via webhook manual, enviando o campo `tema_override` no payload.
- Cada publicação deve conter **pelo menos 1 hashtag** da linha DL correspondente (ex: `#DLGuardião`, `#DLVolt`).
- O tom deve ser **técnico, preventivo e comercial moderado** — nunca agressivo ou sensacionalista.

---

## 3. Variáveis de Ambiente Obrigatórias

Todas as variáveis abaixo devem estar configuradas no ambiente do n8n **antes** da primeira execução do workflow.

| Variável | Descrição | Exemplo / Padrão | Obrigatória |
|---|---|---|---|
| `META_PAGE_ID_DL` | ID numérico da Facebook Page da DL Soluções | `123456789012345` | ✅ Sim |
| `META_IG_BUSINESS_ID_DL` | ID numérico da conta Instagram Business vinculada | `17841400000000000` | ✅ Sim |
| `META_PAGE_ACCESS_TOKEN_DL` | Page Access Token de longa duração (nunca User Token) | `EAABs...` | ✅ Sim |
| `META_APP_ID_N8N_INTEGRACAO` | App ID do aplicativo Meta registrado para integração n8n | `100200300400` | ✅ Sim |
| `GOOGLE_DRIVE_FOLDER_ACERVO_POSTS_N8N` | ID da pasta do Google Drive onde imagens geradas são armazenadas | `1aBcDeFgHiJkLmNoPq` | ✅ Sim |
| `IMAGE_PROVIDER` | Provedor de geração de imagem (`gemini`, `openai`, `flux`) | `gemini` | ✅ Sim |
| `IMAGE_API_KEY` | Chave de API do provedor de imagem configurado | `sk-...` ou `AIza...` | ✅ Sim |
| `IMAGE_MODEL` | Modelo específico de geração de imagem | `imagen-4-ultra` | ✅ Sim |
| `AUTO_PUBLISH_META` | Se `true`, publica automaticamente sem aprovação humana | `true` | ✅ Sim |
| `TELEGRAM_CHAT_ID_DL` | Chat ID do grupo/canal Telegram para notificações | `-1001234567890` | ✅ Sim |
| `SUPABASE_URL` | URL da instância Supabase do DL Nexus | `https://xxx.supabase.co` | ✅ Sim |
| `SUPABASE_SERVICE_ROLE_KEY` | Service Role Key do Supabase (acesso administrativo) | `eyJhbGci...` | ✅ Sim |

> [!CAUTION]
> **NUNCA** insira tokens ou chaves diretamente no JSON do workflow. Sempre referencie via `{{$env.NOME_DA_VARIAVEL}}`. Tokens hardcoded são uma violação crítica de segurança e resultam em rejeição imediata no code review.

> [!WARNING]
> O `META_PAGE_ACCESS_TOKEN_DL` deve ser um **Page Access Token**, não um User Access Token. Tokens de usuário expiram rapidamente e não funcionam para publicações automatizadas em páginas.

---

## 4. Fluxo de Execução

O workflow segue uma pipeline linear com validação obrigatória antes da publicação.

### 4.1 Diagrama de Fluxo

```
TRIGGER (Cron 4x/dia OU Webhook Manual)
    │
    ▼
[1] IDENTIFICAR DIA DA SEMANA
    │
    ▼
[2] SELECIONAR PAUTA (Matriz Semanal)
    │
    ▼
[3] BUSCAR CONTEXTO (Supabase: últimos posts, evitar repetição)
    │
    ▼
[4] GERAR CONTEÚDO (LLM: texto + prompt de imagem)
    │
    ▼
[5] KILLCRITIC (Validação de compliance)
    │
    ├── ❌ REPROVADO → Regenerar (até 3 tentativas) → Notificar Telegram
    │
    ▼
[6] GERAR IMAGEM (IMAGE_PROVIDER configurado)
    │
    ▼
[7] UPLOAD IMAGEM (Google Drive → URL pública)
    │
    ▼
[8] DECIDIR ROTA (AUTO_PUBLISH_META?)
    │
    ├── true  → [9A] PUBLICAR DIRETO
    ├── false → [9B] ENVIAR PARA APROVAÇÃO (020)
    │
    ▼
[9A] PUBLICAR
    ├── Facebook (082_PUBLICADOR_FACEBOOK_META_API)
    ├── Instagram (081_PUBLICADOR_INSTAGRAM_META_API)
    │
    ▼
[10] REGISTRAR NO SUPABASE
    │
    ▼
[11] NOTIFICAR TELEGRAM (resumo da publicação)
    │
    ▼
[12] FIM
```

### 4.2 Descrição Detalhada dos Nós

#### [1] Trigger — Cron Schedule + Webhook

- **Cron Schedule Trigger:** Executa nos horários 08:00, 12:00, 18:00 e 20:00 (America/Sao_Paulo).
- **Webhook Trigger:** Aceita requisição POST com payload opcional contendo `tema_override`, `formato_override` (post/carrossel/reels) e `dry_run` (boolean).
- Ambos os triggers convergem para o mesmo nó seguinte.

#### [2] Identificar Dia da Semana (Code Node)

```javascript
const diasSemana = ['domingo','segunda','terca','quarta','quinta','sexta','sabado'];
const hoje = new Date().toLocaleDateString('pt-BR', { 
  timeZone: 'America/Sao_Paulo', 
  weekday: 'long' 
});
const diaIndex = new Date().getDay();
return [{ json: { dia: diasSemana[diaIndex], diaIndex } }];
```

#### [3] Selecionar Pauta (Switch Node)

Mapeia o dia da semana para a linha DL correspondente conforme a Matriz de Pautas (Seção 2). Se houver `tema_override` no payload do webhook, esse valor tem prioridade sobre o dia da semana.

#### [4] Buscar Contexto (Supabase Query)

Consulta a tabela `posts_publicados` para recuperar os últimos 10 posts da mesma linha DL, evitando repetição de abordagens e títulos.

#### [5] Gerar Conteúdo (AI Agent / HTTP Request)

Envia prompt estruturado para o LLM (Gemini ou DeepSeek conforme configuração) contendo:
- Linha DL do dia
- Histórico de posts anteriores (para evitar repetição)
- Regras de conteúdo (Seção 5)
- Regras de imagem para o prompt de geração (Seção 6)
- Formato solicitado (post único ou carrossel)

Retorna:
- `texto_post`: Texto completo para publicação
- `prompt_imagem`: Prompt de geração de imagem
- `hashtags`: Array de hashtags relevantes
- `slides` (se carrossel): Array de objetos `{ texto_slide, prompt_imagem_slide }`

#### [6] KILLCRITIC (Code Node — Validação)

Aplica todas as regras de compliance automaticamente. Detalhado na **Seção 7**.

#### [7] Gerar Imagem (HTTP Request)

Envia o `prompt_imagem` para o provedor configurado em `IMAGE_PROVIDER`. Para carrosséis, gera uma imagem por slide (3 a 10 imagens).

#### [8] Upload para Google Drive (Google Drive Node)

Faz upload da(s) imagem(ns) gerada(s) para a pasta configurada em `GOOGLE_DRIVE_FOLDER_ACERVO_POSTS_N8N`. Retorna o link público da imagem.

#### [9] Decidir Rota (If Node)

Verifica o valor de `AUTO_PUBLISH_META`:
- Se `true`: segue para publicação direta.
- Se `false`: envia para o workflow de aprovação (020).

#### [10A] Publicar — Facebook (Sub-workflow 082)

Chama o workflow `082_PUBLICADOR_FACEBOOK_META_API` com:
- `message`: texto do post
- `image_url` (opcional): URL pública da imagem

#### [10B] Publicar — Instagram (Sub-workflow 081)

Chama o workflow `081_PUBLICADOR_INSTAGRAM_META_API` com:
- `caption`: texto do post
- `image_url`: URL pública HTTPS da imagem (obrigatório para Instagram)

#### [11] Registrar no Supabase (Supabase Insert)

Insere registro na tabela `posts_publicados` com:
- `linha_dl`, `texto`, `image_url`, `plataforma`, `post_id`, `media_id`
- `created_at`, `horario_publicacao`, `formato` (post/carrossel)
- `killcritic_aprovado` (boolean)

#### [12] Notificar Telegram (Telegram Bot Node)

Envia mensagem resumida para o chat configurado com:
- ✅ ou ❌ status da publicação
- Linha DL do dia
- Horário
- Link do post (quando disponível)
- Erros encontrados (se houver)

---

## 5. Regras de Conteúdo

### 5.1 Regras OBRIGATÓRIAS (Violação = Rejeição Automática pelo KILLCRITIC)

| # | Regra | Motivo |
|---|---|---|
| RC-01 | **NÃO acusar o leitor diretamente.** Nunca usar "você" ligado a risco, falha, negligência ou insegurança. | Evita tom acusatório que gera reação negativa e denúncias no Meta. |
| RC-02 | **NÃO prometer resultado garantido.** Frases como "economia de 40% garantida" ou "segurança total" são proibidas. | Propaganda enganosa — infração ao CDC e políticas do Meta. |
| RC-03 | **NÃO prometer economia garantida.** Valores percentuais ou monetários só podem ser usados como exemplo genérico com disclaimers. | Cada condomínio tem realidade diferente. |
| RC-04 | **NÃO prometer segurança total.** Nenhum sistema de segurança é 100% infalível. | Responsabilidade jurídica. |
| RC-05 | **NÃO prometer prazo sem avaliação técnica prévia.** | Cada projeto tem escopo diferente. |
| RC-06 | **NÃO usar termos sensacionalistas.** Proibidos: "blindado 24h", "nunca mais terá problema", "risco de morte", "tragédia", "perigo total", "urgente!!!", "chocante". | Políticas do Meta e credibilidade profissional. |
| RC-07 | **NÃO copiar notícias textualmente.** A máquina pode se inspirar em fatos jornalísticos, mas NUNCA reproduzir parágrafos de notícias. | Direitos autorais e originalidade. |
| RC-08 | **NÃO usar o termo "B2B" em texto público.** É jargão interno. O público final não precisa saber que o modelo é B2B. | Comunicação inadequada para o público-alvo. |
| RC-09 | **SEMPRE usar "Avaliação Técnica"** em vez de "visita técnica", "orçamento grátis" ou "inspeção gratuita". | Padronização e posicionamento premium. |
| RC-10 | **SEMPRE usar "tempo de resposta para chamados"** quando o assunto for SLA ou contratos de manutenção. | Clareza para síndicos que não conhecem o termo "SLA". |
| RC-11 | **NÃO afirmar que a DL é parceira oficial da Meta**, Facebook, Instagram ou WhatsApp. | Falsa associação — violação grave das políticas Meta. |
| RC-12 | **NÃO inventar convênio com Guarda Municipal** ou qualquer força policial. | Informação falsa. |
| RC-13 | **NÃO inventar integração oficial com órgãos públicos** (Defesa Civil, Corpo de Bombeiros como parceiros, etc). | Informação falsa. |
| RC-14 | **NÃO afirmar compatibilidades não comprovadas** (ex: "compatível com todos os sistemas do mercado"). | Propaganda enganosa. |
| RC-15 | **NÃO garantir prevenção total** de qualquer tipo de sinistro. | Responsabilidade jurídica. |
| RC-16 | **Tom deve ser técnico, preventivo e comercial moderado.** | Identidade da marca DL Soluções. |

### 5.2 CTAs Seguros (Aprovados)

| CTA | Uso Recomendado |
|---|---|
| "Solicite uma Avaliação Técnica" | Todos os posts |
| "Chame no Direct" | Instagram |
| "Envie uma mensagem" | Facebook |
| "Fale com a DL Soluções" | Genérico |
| "Conheça nosso portfólio" | Posts de case/resultado |
| "Agende uma conversa com nosso time técnico" | Posts de manutenção/SLA |

### 5.3 CTAs Proibidos

| CTA Proibido | Motivo |
|---|---|
| "Compre agora" | Tom de varejo — incompatível com B2B |
| "Últimas vagas" | Falsa urgência |
| "Só hoje" | Falsa escassez |
| "Orçamento grátis" | Desvaloriza o serviço técnico |
| "Não perca" | Sensacionalismo |

---

## 6. Regras de Imagem

### 6.1 Regras OBRIGATÓRIAS para Prompts de Geração de Imagem

| # | Regra | Detalhe |
|---|---|---|
| RI-01 | **Fotorrealista.** Todas as imagens devem ter aparência de fotografia profissional. | Iluminação natural ou estúdio. Sem aparência de videogame, 3D genérico ou render artificial. |
| RI-02 | **SEM texto dentro da imagem.** Nenhuma palavra, frase, número ou legenda renderizada na imagem. | Modelos de IA geram texto ilegível e desalinhado — destrói a credibilidade. |
| RI-03 | **SEM logotipos.** Nenhum logotipo de nenhuma marca (DL Soluções, Meta, fabricantes, etc). | Evita problemas de marca registrada e garante versatilidade. |
| RI-04 | **SEM rostos identificáveis.** Pessoas podem aparecer de costas, silhueta ou foco em mãos/equipamento. | LGPD e direito de imagem. |
| RI-05 | **SEM placas de carro.** Se um veículo aparecer, a placa deve estar desfocada ou ausente. | Privacidade. |
| RI-06 | **SEM número de apartamento** visível. | Privacidade. |
| RI-07 | **SEM fachada identificável de cliente.** Prédios devem ser genéricos. | Privacidade do cliente e sigilo comercial. |
| RI-08 | **SEM uniforme com marca falsa.** Se houver trabalhador, o uniforme deve ser genérico (sem logo). | Evita associação indevida. |
| RI-09 | **SEM cenas de pânico, incêndio real, acidente, vítima ou tragédia.** | Políticas Meta e sensibilidade social. |
| RI-10 | **SEM aparência de videogame, 3D genérico ou render artificial.** | Credibilidade e profissionalismo. |

### 6.2 Formatos de Imagem

| Formato | Dimensão | Uso |
|---|---|---|
| Feed (quadrado) | 1080×1080 (1:1) | Posts de feed padrão |
| Stories/Reels (vertical) | 1080×1920 (9:16) | Stories e Reels |
| Carrossel | 1080×1080 por slide | Cada slide do carrossel |

### 6.3 Proibições de URL de Imagem

- **NÃO usar `picsum.photos`** ou qualquer placeholder genérico para publicações reais.
- **NÃO usar URLs privadas do Google Drive** para Instagram (a Meta não consegue acessar).
- A imagem **DEVE** estar acessível via URL pública HTTPS e retornar `Content-Type: image/jpeg` ou `image/png`.

---

## 7. KILLCRITIC

### 7.1 O que é

O **KILLCRITIC** é um nó do tipo **Code Node** dentro do workflow 151 que funciona como **barreira de compliance obrigatória**. Todo conteúdo gerado pela IA passa por essa validação **antes** de ser publicado.

### 7.2 Funcionamento Interno

```
ENTRADA: { texto_post, prompt_imagem, hashtags, formato }
    │
    ▼
[KC-1] VERIFICAÇÃO DE TEXTO
    ├── Regex: detecta termos proibidos (blacklist)
    ├── Regex: detecta "você/seu/sua" + contexto negativo
    ├── Regex: detecta promessas absolutas ("garantido", "total", "100%", "nunca mais")
    ├── Regex: detecta sensacionalismo ("urgente", "chocante", "tragédia")
    ├── Verificação: "Avaliação Técnica" presente?
    ├── Verificação: CTA está na lista de CTAs seguros?
    ├── Verificação: NÃO contém "B2B"?
    ├── Verificação: NÃO contém "parceira da Meta"?
    ├── Verificação: NÃO contém "Guarda Municipal" como parceira?
    ├── Verificação: NÃO contém integração oficial fictícia?
    │
    ▼
[KC-2] VERIFICAÇÃO DE PROMPT DE IMAGEM
    ├── Regex: NÃO contém instrução de texto na imagem
    ├── Regex: NÃO contém instrução de logo
    ├── Regex: NÃO contém instrução de rosto
    ├── Regex: NÃO contém termos de pânico/tragédia
    ├── Verificação: contém "photorealistic" ou "fotorrealista"?
    │
    ▼
[KC-3] DECISÃO
    ├── TODAS as verificações OK → { aprovado: true, motivo: null }
    ├── QUALQUER falha → { aprovado: false, motivo: "RC-XX: descrição da violação" }
    │
    ▼
SAÍDA: { aprovado, motivo, tentativa_atual, max_tentativas: 3 }
```

### 7.3 Comportamento em Caso de Reprovação

1. O conteúdo **NÃO** é publicado.
2. O sistema tenta **regenerar** o conteúdo até **3 vezes**, informando ao LLM qual regra foi violada.
3. Se após 3 tentativas o KILLCRITIC continuar reprovando, o workflow:
   - Registra o evento no Supabase com `killcritic_aprovado = false`.
   - Envia notificação no Telegram com o motivo da reprovação.
   - **NÃO publica nada** — é preferível ficar sem post a publicar conteúdo que viola as regras.

### 7.4 Blacklist de Termos (Exemplos)

```javascript
const blacklist = [
  'blindado 24h', 'nunca mais terá problema', 'risco de morte',
  'tragédia', 'perigo total', 'urgente!!!', 'chocante',
  'parceira da Meta', 'parceira do Facebook', 'parceira do Instagram',
  'convênio com a Guarda', 'integração oficial com',
  'segurança total', 'garantia total', 'economia garantida',
  'orçamento grátis', 'visita técnica gratuita',
  'compre agora', 'últimas vagas', 'só hoje', 'não perca',
  'B2B', 'Manus.IA', 'manus_api'
];
```

---

## 8. Linha Editorial Baseada em Notícia

### 8.1 Conceito

A máquina de conteúdo pode utilizar **fatos jornalísticos recentes** como base editorial para criar posts relevantes e conectados com a realidade. Isso aumenta o engajamento orgânico e posiciona a DL Soluções como referência técnica que acompanha o mercado.

### 8.2 Estrutura do Post Baseado em Notícia

| Etapa | Descrição | Exemplo |
|---|---|---|
| **1. Abertura com fato** | Mencionar um fato noticioso SEM sensacionalismo. Sem copiar o texto original. | "Recentemente, um condomínio na Zona Norte do Rio precisou revisar todo o sistema de acesso após uma falha de segurança." |
| **2. Contextualização** | Explicar que o caso reforça a necessidade de **revisar acessos, monitoramento e rotinas de segurança**. | "Situações como essa reforçam a importância de manter os sistemas de controle de acesso e monitoramento sempre atualizados e com manutenção preventiva em dia." |
| **3. Conexão com linhas DL** | Conectar com **DL Guardião** (CFTV), **DL Fortress** (controle de acesso) e/ou **DL Partner** (manutenção recorrente). | "A DL Fortress oferece soluções de controle de acesso com biometria facial e integração com aplicativos de gestão condominial." |
| **4. Alavancagem técnica** | Quando aplicável, mencionar **analíticos de vídeo** e aproveitamento técnico da infraestrutura existente. | "Com analíticos de vídeo inteligentes, é possível detectar movimentações atípicas e gerar alertas em tempo real, sem necessidade de trocar todo o sistema — muitas vezes basta atualizar o software do DVR/NVR existente." |
| **5. CTA** | Chamada para Avaliação Técnica. | "Solicite uma Avaliação Técnica e descubra como otimizar a segurança do seu condomínio." |

### 8.3 Regras ABSOLUTAS para Posts Baseados em Notícia

> [!CAUTION]
> As regras abaixo são **invioláveis**. Qualquer descumprimento resulta em rejeição pelo KILLCRITIC.

| # | Regra |
|---|---|
| LN-01 | **NUNCA inventar convênios com a Guarda Municipal** ou qualquer força policial. |
| LN-02 | **NUNCA inventar integrações oficiais com órgãos públicos** (Defesa Civil, Corpo de Bombeiros como parceiros, prefeitura, etc). |
| LN-03 | **NUNCA afirmar compatibilidades não comprovadas** entre sistemas. |
| LN-04 | **NUNCA garantir prevenção total** de qualquer tipo de sinistro. |
| LN-05 | **NUNCA reproduzir parágrafos da notícia original** — apenas inspirar-se no fato. |
| LN-06 | **NUNCA identificar o condomínio, endereço ou vítimas** mencionados na notícia. |
| LN-07 | **NUNCA usar tom alarmista** ("isso pode acontecer com VOCÊ!"). |

---

## 9. Formato Carrossel

### 9.1 Especificação

O workflow 151 suporta a geração de **carrosséis** (posts com múltiplos slides) para Facebook e Instagram.

| Atributo | Valor |
|---|---|
| **Frequência mínima** | 1 carrossel por dia |
| **Quantidade de slides** | 3 a 10 slides por carrossel |
| **Cada slide possui** | Imagem própria + legenda/caption próprio |
| **Formato de imagem** | 1080×1080 (1:1) por slide |
| **Narrativa** | Cada slide deve contribuir para uma narrativa progressiva |

### 9.2 Estrutura de um Carrossel

```json
{
  "formato": "carrossel",
  "titulo": "5 sinais de que o CFTV do seu condomínio precisa de manutenção",
  "slides": [
    {
      "ordem": 1,
      "texto_slide": "Slide 1: Imagens com ruído excessivo ou tremidas podem indicar câmeras com lente suja ou foco desregulado.",
      "prompt_imagem_slide": "Professional photorealistic photograph of a clean CCTV security camera mounted on a modern condominium wall, soft natural lighting, shallow depth of field, no text, no logos, no faces"
    },
    {
      "ordem": 2,
      "texto_slide": "Slide 2: Se o DVR mostra 'sem sinal' em algum canal, pode haver cabo rompido ou fonte queimada.",
      "prompt_imagem_slide": "Professional photorealistic photograph of a modern DVR/NVR unit with LED indicators in a server rack, clean environment, no text, no logos, no faces"
    }
  ]
}
```

### 9.3 Publicação de Carrosséis

- **Facebook:** Publicado como álbum de fotos com legenda geral + legendas individuais.
- **Instagram:** Publicado via Meta Graph API como carrossel (endpoint `/media` com `media_type=CAROUSEL`). Cada slide requer `image_url` pública HTTPS.

> [!IMPORTANT]
> Para carrosséis no Instagram, **todas** as imagens dos slides devem estar em URLs públicas HTTPS acessíveis pela Meta. URLs privadas do Google Drive **não funcionam**.

---

## 10. Publicadores Downstream

O workflow 151 **não publica diretamente** nas redes sociais. Ele prepara o conteúdo e delega a publicação para workflows especializados.

### 10.1 — 082_PUBLICADOR_FACEBOOK_META_API

| Atributo | Detalhe |
|---|---|
| **Função** | Publicar posts na Facebook Page da DL Soluções |
| **Endpoint** | `POST https://graph.facebook.com/v21.0/{{$env.META_PAGE_ID_DL}}/feed` |
| **Payload** | `{ message: "texto", link: "url_opcional" }` |
| **Imagem** | Opcional — se fornecida, usa endpoint `/photos` |
| **Autenticação** | `access_token={{$env.META_PAGE_ACCESS_TOKEN_DL}}` |
| **Retorno esperado** | `{ id: "PAGE_ID_POST_ID" }` |

### 10.2 — 081_PUBLICADOR_INSTAGRAM_META_API

| Atributo | Detalhe |
|---|---|
| **Função** | Publicar posts no Instagram Business da DL Soluções |
| **Endpoint (Passo 1)** | `POST https://graph.facebook.com/v21.0/{{$env.META_IG_BUSINESS_ID_DL}}/media` |
| **Payload (Passo 1)** | `{ image_url: "URL_PUBLICA_HTTPS", caption: "texto" }` |
| **Endpoint (Passo 2)** | `POST https://graph.facebook.com/v21.0/{{$env.META_IG_BUSINESS_ID_DL}}/media_publish` |
| **Payload (Passo 2)** | `{ creation_id: "ID_DO_PASSO_1" }` |
| **Autenticação** | `access_token={{$env.META_PAGE_ACCESS_TOKEN_DL}}` |
| **Retorno esperado** | `{ id: "MEDIA_ID" }` |

> [!WARNING]
> O Instagram **exige** `image_url` pública. O fluxo de 2 etapas (criar container → publicar) é obrigatório. Não é possível enviar imagem como upload direto via Graph API.

### 10.3 — 020_PUBLICADOR_SOCIAL_DL_NEXUS_V3_APROVACAO (Opcional)

| Atributo | Detalhe |
|---|---|
| **Função** | Central de aprovação humana antes da publicação |
| **Quando ativo** | Quando `AUTO_PUBLISH_META=false` |
| **Canal** | Notificação via Telegram com botões Aprovar/Rejeitar |
| **Timeout** | 4 horas — se não aprovado, descarta e notifica |

---

## 11. Troubleshooting

### Problemas Comuns e Soluções

#### 11.1 Instagram não publica — "The image URL is not accessible"

| Causa | Solução |
|---|---|
| URL da imagem é privada (Google Drive com permissão restrita) | Configurar compartilhamento público no Google Drive OU usar CDN dedicada |
| URL não retorna `Content-Type: image/jpeg` ou `image/png` | Verificar se a URL aponta diretamente para o arquivo de imagem |
| URL usa HTTP em vez de HTTPS | Garantir que todas as URLs de imagem usam HTTPS |
| URL redireciona para página de login | Testar URL em aba anônima do navegador |

#### 11.2 Facebook publica mas sem imagem

| Causa | Solução |
|---|---|
| Campo `image_url` está vazio ou null | Verificar se o nó de geração de imagem retornou URL válida |
| Endpoint usado foi `/feed` em vez de `/photos` | Para posts com imagem, usar endpoint `/PAGE_ID/photos` |

#### 11.3 KILLCRITIC rejeita tudo (3/3 tentativas)

| Causa | Solução |
|---|---|
| Prompt do LLM não inclui as regras de conteúdo | Verificar se o system prompt do nó de geração contém todas as regras da Seção 5 |
| LLM insiste em termos proibidos | Adicionar exemplos negativos ao prompt ("NÃO use: ...") |
| Regex do KILLCRITIC muito restritivo | Revisar os patterns — pode estar pegando falsos positivos |

#### 11.4 Token expirou — "Invalid OAuth access token"

| Causa | Solução |
|---|---|
| Usando User Token em vez de Page Token | Gerar Page Access Token de longa duração via Graph API Explorer |
| Page Token expirou (raro, mas possível) | Regenerar via Graph API: `GET /me/accounts?access_token=USER_TOKEN` |

#### 11.5 Supabase não registra publicação

| Causa | Solução |
|---|---|
| `SUPABASE_URL` ou `SUPABASE_SERVICE_ROLE_KEY` incorretos | Verificar variáveis de ambiente |
| Tabela `posts_publicados` não existe | Criar tabela com schema correto no Supabase |
| Row Level Security bloqueando | Verificar RLS policies — Service Role Key deve ter bypass |

#### 11.6 Telegram não recebe notificação

| Causa | Solução |
|---|---|
| `TELEGRAM_CHAT_ID_DL` incorreto | Verificar se o chat ID inclui o prefixo `-100` para grupos |
| Bot não é membro do grupo/canal | Adicionar o bot ao grupo/canal |
| Bot não tem permissão de postagem | Conceder permissão de administrador ao bot |

#### 11.7 Workflow não dispara nos horários programados

| Causa | Solução |
|---|---|
| Timezone incorreto no Cron | Verificar se está configurado como `America/Sao_Paulo` |
| Workflow desativado | Ativar o workflow no n8n |
| n8n parado ou em manutenção | Verificar status do container/serviço n8n |

---

## Apêndice A — Glossário

| Termo | Significado |
|---|---|
| **KILLCRITIC** | Nó de validação de compliance que bloqueia conteúdo inadequado |
| **Linha DL** | Marca/produto da DL Soluções (ex: DL Guardião, DL Volt, etc.) |
| **Avaliação Técnica** | Termo padronizado para visita técnica / diagnóstico |
| **Page Access Token** | Token de acesso vinculado à Facebook Page (longa duração) |
| **Graph API** | API oficial da Meta para interação com Facebook e Instagram |
| **SLA** | Service Level Agreement — apresentado como "tempo de resposta para chamados" |
| **CDN** | Content Delivery Network — rede de distribuição de conteúdo para imagens públicas |

---

## Apêndice B — Referências

- [Meta Graph API — Pages](https://developers.facebook.com/docs/pages/)
- [Meta Graph API — Instagram Content Publishing](https://developers.facebook.com/docs/instagram-platform/content-publishing)
- [n8n Documentation](https://docs.n8n.io/)
- [Supabase Documentation](https://supabase.com/docs)

---

> **Documento mantido pela equipe de Engenharia de Integração — DL Nexus V3**  
> Última atualização: 2026-06-23
