# Relatório de Ativação Social — DL Nexus V3
**Data:** 22 de Maio de 2026  
**Responsável:** Diogo Luiz de Oliveira — Tecnólogo Responsável  
**Objetivo:** Ativação controlada da esteira de publicação social multicanal

---

## 1. O Que Pode Ser Ativado Hoje

| Workflow | Canal | Pode Ativar Hoje? | Bloqueio |
|---|---|---|---|
| `020_PUBLICADOR_SOCIAL` | Orquestrador IA | ✅ Sim, após IDs | CHAT_ID pendente |
| `081_PUBLICADOR_INSTAGRAM` | Instagram | ⚠️ Parcial | INSTAGRAM_BUSINESS_ACCOUNT_ID + CHAT_ID |
| `082_PUBLICADOR_FACEBOOK` | Facebook | ⚠️ Parcial | PAGE_ID + CHAT_ID |
| `083_PUBLICADOR_GOOGLE` | Google Meu Negócio | ❌ Não | OAuth Google não configurado |
| `084_PUBLICADOR_TIKTOK_ASSISTIDO` | TikTok (manual) | ✅ Sim, após CHAT_ID | CHAT_ID pendente |
| `085_SOCIAL_DISPATCHER` | Roteador | ⚠️ Após 081/082 | Depende de 081 e 082 ativos |
| `021_DESCOBRIR_IDS_SOCIAIS` | Utilitário | ✅ Executar imediatamente | Nenhum |

> **Ação imediata recomendada:** Execute o `021_DESCOBRIR_IDS_SOCIAIS_DL_NEXUS` para desbloquear 081, 082 e 020.

---

## 2. IDs Pendentes

| Placeholder | Onde usar | Como obter |
|---|---|---|
| `CHAT_ID_AQUI` | Todos os workflows | Enviar `/start` ao bot → `api.telegram.org/bot{TOKEN}/getUpdates` → copiar `chat.id` |
| `PAGE_ID_AQUI` | 082 Facebook, 020 | Executar `021_DESCOBRIR_IDS_SOCIAIS` ou Meta Business Suite |
| `INSTAGRAM_BUSINESS_ACCOUNT_ID_AQUI` | 081 Instagram, 020 | Executar `021_DESCOBRIR_IDS_SOCIAIS` ou Meta Business Suite |
| `GOOGLE_ACCOUNT_ID_AQUI` | 083 Google | Console Google My Business API |
| `GOOGLE_LOCATION_ID_AQUI` | 083 Google | Console Google My Business API |

---

## 3. Credenciais Necessárias no n8n

| Credencial | Workflows | Status |
|---|---|---|
| `Aplicativo do Facebook` | 081, 082, 085 | ✅ Já existe no n8n |
| `Conta do Telegram` | Todos | ✅ Já existe no n8n |
| `SMTP - Suporte DL` | 020, 021 | ✅ Já existe no n8n |
| `Conta OpenAi` | 020 | ✅ Já existe no n8n |
| OAuth Google Business Profile | 083 | ❌ **Criar no n8n** — requer app Google Cloud |

---

## 4. Ordem de Teste (Sem Publicar)

```
1. Executar 021_DESCOBRIR_IDS_SOCIAIS → obter PAGE_ID e INSTAGRAM_ID via e-mail
2. Preencher CHAT_ID_AQUI em todos os workflows (Telegram getUpdates)
3. Preencher PAGE_ID_AQUI no 082 e no 020
4. Preencher INSTAGRAM_BUSINESS_ACCOUNT_ID_AQUI no 081 e no 020
5. Testar 081: enviar POST manual ao webhook com approved=false → verificar bloqueio
6. Testar 082: enviar POST manual ao webhook com approved=false → verificar bloqueio
7. Testar 084: enviar POST manual → verificar se pacote TikTok chega no Telegram
8. Testar 020: executar manualmente → verificar se prévia chega no Telegram
9. Testar 085: enviar POST com approved=true → verificar dispatch para sub-webhooks
```

---

## 5. Ordem de Ativação Controlada

```
Fase 1 — Utilitário (hoje):
  → Ativar 021_DESCOBRIR_IDS_SOCIAIS (temporário, desativar após uso)

Fase 2 — Canal mais seguro (TikTok assistido):
  → Ativar 084_PUBLICADOR_TIKTOK_ASSISTIDO (sem publicação automática)

Fase 3 — Telegram (controle):
  → 020 já envia prévia via Telegram; confirmar CHAT_ID

Fase 4 — Facebook + Instagram:
  → Ativar 082_PUBLICADOR_FACEBOOK_META_API
  → Ativar 081_PUBLICADOR_INSTAGRAM_META_API
  → Ativar 020_PUBLICADOR_SOCIAL (toggle Ativo)

Fase 5 — Dispatcher:
  → Ativar 085_SOCIAL_DISPATCHER_DL_NEXUS

Fase 6 — Google (quando OAuth configurado):
  → Configurar credencial OAuth Google Business Profile no n8n
  → Obter GOOGLE_ACCOUNT_ID e LOCATION_ID
  → Ativar 083_PUBLICADOR_GOOGLE_BUSINESS_PROFILE
```

---

## 6. Riscos

| Risco | Severidade | Mitigação |
|---|---|---|
| Publicar sem aprovação humana | 🔴 Crítico | `approved=true` obrigatório em todos os nós |
| Token expirado no Facebook App | 🟡 Médio | Renovar token de longa duração no Meta Developer |
| KILLCRITIC falso-positivo (bloquear post legítimo) | 🟡 Médio | Revisar lista de termos proibidos antes de ativar |
| Google OAuth expirar | 🟡 Médio | Usar refresh token de longa duração |
| CHAT_ID errado (mensagem vai para bot errado) | 🟠 Alto | Confirmar chat_id antes de ativar qualquer workflow |
| Dispatcher 085 chamar webhooks desativados | 🟡 Médio | Ativar 081/082/084 antes do 085 |
| TikTok: postagem fora do horário de pico | 🟢 Baixo | Pacote assistido — Diogo controla o horário manual |

---

## 7. Checklist para Raphael / Operador

```
[ ] 1. Executar 021_DESCOBRIR_IDS_SOCIAIS e anotar PAGE_ID e INSTAGRAM_ID
[ ] 2. Obter CHAT_ID via Telegram getUpdates
[ ] 3. Substituir todos os placeholders nos workflows no n8n UI
[ ] 4. Testar bloqueio KILLCRITIC (enviar post com "visita técnica")
[ ] 5. Testar aprovação negada (enviar approved=false)
[ ] 6. Testar fluxo completo com approved=true (sem publicar — workflow inactive)
[ ] 7. Ativar 084_TIKTOK_ASSISTIDO primeiro (menor risco)
[ ] 8. Ativar 082_FACEBOOK após confirmar PAGE_ID
[ ] 9. Ativar 081_INSTAGRAM após confirmar INSTAGRAM_ID
[ ] 10. Ativar 020_PUBLICADOR_SOCIAL
[ ] 11. Ativar 085_DISPATCHER por último
[ ] 12. Configurar OAuth Google Business Profile (prazo: próxima semana)
[ ] 13. Fazer commit de cada etapa concluída
```

---

## 8. Workflows Criados Nesta Sessão

| Arquivo | Status |
|---|---|
| `081_PUBLICADOR_INSTAGRAM_META_API.json` | ✅ Criado |
| `082_PUBLICADOR_FACEBOOK_META_API.json` | ✅ Criado |
| `083_PUBLICADOR_GOOGLE_BUSINESS_PROFILE.json` | ✅ Criado |
| `084_PUBLICADOR_TIKTOK_ASSISTIDO.json` | ✅ Criado |
| `085_SOCIAL_DISPATCHER_DL_NEXUS.json` | ✅ Criado |
| Relatórios individuais por workflow | ✅ Criados |
| Este relatório mestre | ✅ Criado |

**Nenhum workflow foi ativado. Nenhuma publicação foi feita. Zero segredos expostos.**
