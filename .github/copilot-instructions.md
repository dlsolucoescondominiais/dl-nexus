# GitHub Copilot — Instruções do Repositório DL Nexus
## Empresa: DL Soluções Condominiais LTDA | CREA-RJ Habilitada

> Este ficheiro define o comportamento esperado do GitHub Copilot em TODAS as interações dentro deste repositório.
> Trata cada instrução como uma Hard Rule de engenharia. Não negoceies variações.

---

## 🏗️ Stack Tecnológica

- **Frontend:** Next.js 14+ (App Router), React 18, TypeScript estrito
- **Estilo:** TailwindCSS v3 com `tailwind.config.ts` customizado (paleta DL Soluções)
- **Backend/DB:** Supabase (PostgreSQL 15), RLS ativado em TODAS as tabelas
- **Automação:** n8n (self-hosted em `n8n.dlsolucoescondominiais.com.br`)
- **Auth:** Supabase Auth + JWT
- **Deploy:** Vercel (frontend) + Render (backend Python/FastAPI)
- **Linguagem padrão:** TypeScript (frontend), Python 3.11+ (backend), SQL (migrações)

---

## 🚫 REGRAS LINGUÍSTICAS — HARD RULES (sem exceções)

### Vocabulário Proibido → Substituto Obrigatório

| ❌ NUNCA usar | ✅ SEMPRE usar |
|---|---|
| `visita` / `visita técnica` | `Avaliação Técnica` |
| `canaleta plástica` / `canaletas` | `eletroduto corrugado` ou `eletroduto galvanizado` |
| `barato` / `econômico` / `low-cost` | `custo-eficiente` / `ROI otimizado` |
| `instalação simples` | `execução conforme ABNT NBR [número]` |
| `cliente` (em contexto jurídico) | `contratante` |
| `orçamento grátis` | `Avaliação Técnica sem custo` |
| `energia solar barata` | `sistema fotovoltaico com retorno comprovado` |
| `câmera de segurança` | `sistema de CFTV (Circuito Fechado de TV)` |
| `automatização` | `automação predial` |
| `sindicato` | `síndico` ou `administração condominial` |

### Regras de Tom (em strings UI, copy, comentários de código)
- Tom: **Técnico-autoritativo**. Nunca informal. Nunca alarmista.
- Sempre referenciar normas: `ABNT NBR 5410`, `NR-10`, `Lei 14.300/2022`, `CREA-RJ`
- Persona da IA de atendimento: **"Aninha"** — nunca "bot", "chatbot" ou "assistente virtual"
- CTA padrão: `"Solicitar Avaliação Técnica"` — nunca `"Fale Conosco"` genérico

---

## 📁 Convenções de Código

### TypeScript / Next.js
```typescript
// Sempre usar tipos explícitos — nunca `any`
// Componentes: PascalCase, arquivos: kebab-case
// Server Components por defeito; marcar 'use client' apenas quando necessário
// API Routes: sempre validar payload com Zod antes de tocar no Supabase
// Erros: sempre retornar { success: false, error: string } — nunca lançar exceções não tratadas
```

### Supabase / SQL
```sql
-- Toda nova tabela DEVE ter: id UUID DEFAULT gen_random_uuid(), created_at TIMESTAMPTZ, updated_at TIMESTAMPTZ
-- RLS obrigatório: CREATE POLICY antes de qualquer INSERT
-- Nunca usar SELECT * em queries de produção — sempre listar colunas
-- Migrações: ficheiros em /backend/supabase/MIGRATIONS_DL_NEXUS.sql com comentário de data
```

### Python / FastAPI (backend)
```python
# Sempre usar type hints (PEP 484)
# HTTP errors: sempre HTTPException com detail descritivo
# Variáveis de ambiente: sempre via os.getenv() com valor default explícito
# Logs: sempre estruturados com structlog ou logging.getLogger(__name__)
```

---

## 🎯 Contexto de Negócio (para geração de copy e UI)

**Segmento:** B2B — Síndicos profissionais, administradoras de condomínios, facility managers no Rio de Janeiro.

**Serviços Core:**
1. Energia Solar Fotovoltaica (Lei 14.300/2022 — SCEE e GD Local)
2. CFTV e Segurança Predial (Intelbras / câmeras IP)
3. Automação Predial (controle de acesso, portões, iluminação)
4. Elétrica Predial (ABNT NBR 5410, SPDA, QGBT)
5. Prevenção e Combate a Incêndio (IT CBMERJ)

**Diferenciais obrigatórios a mencionar:**
- Habilitação CREA-RJ (sempre citar em contextos de credibilidade)
- ART (Anotação de Responsabilidade Técnica) emitida em todos os projetos
- Garantia pós-execução documentada
- Financiamento via BNB FNE / BNDES Finem disponível

**Lead scoring (para lógica de CRM/n8n):**
- Score alto (>70): síndico profissional certificado, >1 condomínio gerido
- Score médio (40-70): administradora, >50 unidades
- Score baixo (<40): síndico não profissional, 1 condomínio

---

## 🔐 Segurança (DevSecOps)

- **NUNCA** sugerir hardcoding de secrets, API keys ou senhas no código
- Sempre usar variáveis de ambiente: `process.env.NEXT_PUBLIC_*` (frontend público) e `process.env.*` (backend)
- Ficheiro `.env.local` nunca deve ser commitado — verificar `.gitignore`
- Rate limiting obrigatório em qualquer endpoint que receba dados do utilizador
- Sanitização de inputs: sempre usar `DOMPurify` (frontend) ou `bleach` (Python)
- Headers de segurança: `X-Frame-Options`, `Content-Security-Policy` no `next.config.js`

---

## 🤖 Agente "Aninha" — Regras Específicas

Quando gerar código relacionado ao fluxo de atendimento da IA:
- Persona: consultora técnica especializada — nunca simpática genérica
- Sempre oferecer `"Avaliação Técnica"` como próximo passo, nunca "reunião" ou "call"
- Prioridade de canal: WhatsApp > Email > Telefone
- Tempo de resposta alvo: < 2 minutos para primeira resposta automática
- Workflow base: `002_roteador_aninha.json` (n8n)

---

## 📋 Estrutura de Pastas (referência)

```
projeto_01/
├── .github/
│   ├── copilot-instructions.md          ← este ficheiro
│   └── instructions/                    ← instruções por contexto
├── frontend/                            ← Next.js principal
├── frontend_dl_partner/                 ← Landing page HTML estática
├── frontend_react_dl/                   ← React SPA alternativa
├── backend/
│   ├── n8n/workflows/                   ← Workflows n8n (JSON)
│   ├── supabase/                        ← SQL migrations + types
│   └── api/                             ← FastAPI endpoints
├── .agents/skills/                      ← Skills do Antigravity
└── .vscode/                             ← Configurações do editor
```
