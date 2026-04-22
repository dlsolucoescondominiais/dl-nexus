---
description: "Convenções para workflows n8n e automação da DL Soluções"
applyTo: "backend/n8n/**/*.json,tmp/**/*.json"
---

# Instruções: Workflows n8n — DL Nexus Automation

## Nomenclatura de Workflows

```
[NNN]_[categoria]_[descricao].json
```

Exemplos:
- `001_triagem_email_entrada.json`
- `002_roteador_aninha.json`
- `003_pipeline_leads_supabase.json`
- `004_roteador_agentes_especializados.json`

## Estrutura de Nó HTTP Request (padrão)

Ao sugerir código para chamar APIs externas via n8n:

```json
{
  "method": "POST",
  "url": "={{ $env.API_BASE_URL }}/endpoint",
  "headers": {
    "Content-Type": "application/json",
    "Authorization": "Bearer {{ $env.API_SECRET_KEY }}"
  },
  "body": { ... }
}
```

**NUNCA** hardcodar URLs de produção ou API keys em nós n8n.

## Agente Aninha — Fluxo Base

O fluxo da Aninha (`002_roteador_aninha.json`) segue esta lógica:

1. **Receber lead** → Webhook POST `/webhook/aninha`
2. **Classificar persona** → Síndico Pro / Administradora / Escola / Pessoa Física
3. **Calcular score** → Inserir em `leads` no Supabase
4. **Responder via WhatsApp** → Evolution API / Twilio
5. **Agendar Avaliação Técnica** → Se score > 40

Qualquer código gerado para este fluxo deve respeitar estas etapas.

## Segurança em Webhooks n8n

- Sempre adicionar `Header Auth` ou `Basic Auth` nos webhooks expostos
- Validar `X-Webhook-Secret` antes de processar o payload
- Logs: sempre usar nó `Set` para estruturar logs antes do `Supabase` node

## Mensagens Automáticas (copy para nós de mensagem)

Ao gerar mensagens automáticas da Aninha:
- Nunca usar "Olá!" genérico → usar "Bom dia, [Nome]." ou equivalente temporal
- Sempre incluir referência técnica no 1º parágrafo
- Fechar com: "Posso agendar uma **Avaliação Técnica** sem custo para o seu condomínio?"
- Nunca mencionar preço na primeira mensagem
