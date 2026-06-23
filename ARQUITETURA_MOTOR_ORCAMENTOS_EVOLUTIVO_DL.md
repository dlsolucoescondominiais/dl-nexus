# Arquitetura do Motor de Orçamentos Evolutivo — DL Soluções Condominiais

**Data:** 2026-06-21
**Responsável Técnico:** Arquiteto Sênior de Integração
**Filosofia:** Operação viva, iterativa e prática. O sistema aprende com cada orçamento real feito por Diogo, Nielton ou futuros funcionários.

---

## 1. Princípio Fundamental

O Motor de Orçamentos NÃO é um sistema travado esperando testes longos. É uma **esteira evolutiva** que:

- Começa simples e funcional no dia 1.
- Melhora conforme orçamentos reais são feitos e revisados.
- Nunca apaga, nunca sobrescreve, nunca perde histórico.
- Cada orçamento enviado vira uma **versão congelada** (imutável).
- Qualquer alteração gera nova versão com rastreabilidade.

---

## 2. Perfis de Cliente Atendidos

O Motor atende 7 perfis distintos, cada um com catálogo e linguagem específica:

| Perfil | Código | Catálogo Principal |
|---|---|---|
| Síndico / Condomínio | `condominio` | Guardião, Fortress, Acqua, Gatekeeper, Volt, VoltCharge, EcoVolt, Alerta, Partner |
| Pessoa Física | `pessoa_fisica` | Energia solar, sistema solar com baterias, backup 8h/12h/24h, CFTV residencial, elétrica técnica |
| PJ Escola | `escola` | CFTV, controle de acesso, elétrica, alarme, automação |
| PJ Restaurante | `restaurante` | DL Express, Mult•Grill, chapas, grills, fritadeiras, elétrica, CFTV |
| PJ Lanchonete | `lanchonete` | DL Express, Mult•Grill, chapas, grills, fritadeiras, elétrica, CFTV |
| PJ Confeitaria | `confeitaria` | DL Express, elétrica, quadros, tomadas de potência, manutenção preventiva |
| PJ Empresa / Comércio | `empresa` | CFTV, controle de acesso, elétrica, automação, energia solar |

---

## 3. Stack Tecnológica (Barata e Eficiente)

| Camada | Ferramenta | Justificativa |
|---|---|---|
| **Base operacional** | Google Sheets | Diogo e Nielton já sabem usar. Editável em tempo real. Zero custo. |
| **Modelo editável** | Google Docs | Template visual que vira PDF direto. Zero custo. |
| **PDF para cliente** | Google Docs → Export PDF ou Gotenberg | Profissional e instantâneo. |
| **Histórico leve** | Markdown | Economia brutal de tokens. Versionável no Git. |
| **Histórico estruturado** | Supabase (tabela `dl_orcamentos_site_v2`) | Consultas, filtros, relatórios, auditoria. |
| **Geração de texto** | DeepSeek ou Gemini Flash | Barato para rascunho de proposta. |
| **Revisão crítica** | Modelo forte (Claude/GPT-4) | Apenas quando o KILLCRITIC precisa auditar margem ou escopo. |
| **Orquestração** | n8n | Motor central. Webhooks, fluxos, integrações. |

---

## 4. Fluxo Completo do Orçamento (8 Workflows)

```
[SITE] Aba Orçamentos
  │
  ▼
060_ORCAMENTO_RECEPCAO_SITE_DL
  │  Recebe payload, valida, normaliza, registra no Supabase, alerta Telegram.
  ▼
061_ORCAMENTO_CLASSIFICADOR_CLIENTE_DL
  │  Identifica perfil (condomínio, PF, restaurante...).
  │  Seleciona catálogo de serviços aplicável.
  │  Define campos obrigatórios por perfil.
  ▼
062_ORCAMENTO_PLANILHA_GOOGLE_SHEETS_DL
  │  Cria nova linha na planilha operacional.
  │  Campos: cliente, serviço, materiais, mão de obra, margem.
  │  Diogo/Nielton podem editar valores diretamente na planilha.
  ▼
063_ORCAMENTO_GERADOR_MARKDOWN_DL
  │  Gera rascunho da proposta em Markdown (modelo leve via DeepSeek/Flash).
  │  Salva no Supabase e opcionalmente no Google Drive.
  ▼
064_ORCAMENTO_KILLCRITIC_DL
  │  Audita margem, escopo e coerência.
  │  Bloqueia se margem < limiar mínimo.
  │  Bloqueia se numero_unidades faltar para rateio em condomínio.
  │  Marca pendências, nunca descarta.
  ▼
065_ORCAMENTO_GOOGLE_DOCS_PDF_DL
  │  Preenche template Google Docs com os dados aprovados.
  │  Exporta PDF profissional para envio.
  │  Versão congelada salva no Drive e Supabase.
  ▼
066_ORCAMENTO_ENVIO_E_FOLLOWUP_DL
  │  Envia PDF via WhatsApp ou E-mail.
  │  Registra data/hora de envio.
  │  Agenda follow-up automático (3, 7, 15 dias).
  ▼
067_AGENTE_EVOLUCAO_ORCAMENTOS_DL
     Analisa orçamentos feitos. Compara proposta vs resultado real.
     Sugere melhorias no formulário, planilha e templates.
     NUNCA apaga, NUNCA sobrescreve.
```

---

## 5. Regras de Versionamento e Segurança

1. **Orçamento enviado = versão congelada.** Nunca editar diretamente. Criar `v2`, `v3`, etc.
2. **CPF mascarado.** Nunca armazenar pleno. Nunca usar para busca pública automática.
3. **CNPJ recomendado** para condomínio, empresa e administradora. Se faltar, não bloquear lead — bloquear apenas enriquecimento.
4. **`numero_unidades`** obrigatório APENAS para rateio em condomínio. Se faltar, lead entra normalmente, mas o cálculo de "valor por unidade" fica bloqueado.
5. **Dados insuficientes** → usar a cláusula: *"Dados insuficientes para confirmação definitiva"*.
6. **Sem "visita técnica"** — usar "Avaliação Técnica".
7. **Sem "B2B"** em texto público — usar "corporativo e condominial".
8. **Formulários antigos preservados.** O `#dl-contact-form` do `index.html` continua como fallback.
9. **`/webhook/dl-receptor`** intocável. Novos fluxos usam `/webhook/orcamento-v2`.

---

## 6. Evolução Planejada

| Fase | Escopo | Dependência |
|---|---|---|
| **Fase 1 (agora)** | Documentação + 060 + migration Supabase + formulário V2 isolado | Nenhuma |
| **Fase 2** | 061 classificador + 062 Google Sheets + aba no site | Google Sheets API + credencial |
| **Fase 3** | 063 gerador Markdown + 064 Killcritic | DeepSeek ou Gemini Flash no n8n |
| **Fase 4** | 065 Google Docs/PDF + 066 envio + follow-up | Google Docs API + template + Gotenberg |
| **Fase 5** | 067 agente evolutivo | Histórico acumulado de orçamentos reais |
