# 📊 DL COMMANDER (ENTERPRISE MASTER PLAN)
**Arquiteto Estratégico: Diogo Luiz de Oliveira (Tecnólogo em Infraestrutura)**

---

## 1. O Pipeline Comercial de 10 Etapas (Supabase V6)
Cada nova mensagem de WhatsApp que passa pela "Aninha" agora nasce como um **Lead Controlado** na tabela, caminhando automaticamente pelas seguintes etapas:
1. `novo_lead`: Webhook recebeu contato.
2. `triagem_ia`: Gemini Flash avaliou se é urgente, qualificação, ou lixo.
3. `avaliacao_agendada`: O Síndico aceitou a nossa visita (nunca chamada de 'visita técnica').
4. `proposta_enviada`: Antigravity e GPT-4o geraram a oferta.
5. `negociacao`: Você está no Whatsapp quebrando objeções de preço.
6. `fechado_ganho`: Pix na conta.
7. `fechado_perdido`: O síndico foi pro concorrente amador.
8. `pos_venda`: Suporte técnico da instalação executada.
9. `contrato_recorrente`: Virou OPEX (Manutenção mensal).
10. `renovacao`: 30 dias antes do ano virar, o n8n reaquece a proposta.

---

## 2. A Régua de Follow-Up Automática
Os workflows de acompanhamento rodam via **CRON Jobs diários** que escutam a coluna `ultima_interacao` do banco Supabase V6:
- **1 hora:** Mensagem suave "Tudo bem? Vi que está com urgência em energia solar, podemos conversar hoje?"
- **24 horas:** Mensagem do Claude 3.5: Reforça que a sobrecarga elétrica pode causar incêndios (gatilho de urgência).
- **3 dias:** "Veja como ajudamos o Condomínio X a reduzir 30% da conta com OPEX Solar (Case de Sucesso)."
- **7 dias:** "Síndico, nossa equipe vai focar nos chamados urgentes. Tem certeza de que não podemos agendar a Avaliação Técnica?"
- **15 dias:** Reativação comercial (Mensagem de Saudade).
- **30 dias:** Lembrete de manutenção preventiva nos painéis ou elétrica.

---

## 3. Dashboard Executivo Front-End (O Próximo Módulo)
O React (Hospedado no Render) evoluirá do simples painel atual para exibir:
- **Taxa de Conversão:** Quantos % do `novo_lead` chegaram no `fechado_ganho`?
- **Custos de IA:** A API puxará os cálculos da tabela `mensagens_whatsapp` (onde logamos `custo_estimado_usd` e `ia_utilizada`). Vamos saber se gastamos mais com o Claude ou GPT.
- **Gargalos Operacionais:** Em que etapa da tubulação os leads morrem de "fechado_perdido"? É culpa do preço ou da IA?
- **Caixa de Entrada Humana (Human Handoff):** Se o bot se perder ou a conversa esfriar, o botão vermelho "Aprovar/Reprovar IA" entra em ação.

---

## 4. O Fallback System (Fail-Safe)
Conforme programado no `001_webhook_receptor.json`:
* **Se o n8n sofrer ataque:** Tem `RateLimit` ativo no nó inicial (10 msg por minuto, por IP).
* **Se a API do Claude Cair (Urgência):** Automaticamente vai pro OpenAI GPT-4o Mini tentar fechar a porta.
* **Se o OpenAI Cair junto:** Uma mensagem Text Plain vai ser disparada dizendo "Olá, a IA está indisponível e nosso Especialista vai assumir seu caso logo mais".
* **Se o Próprio Supabase Cair:** A função do n8n possui uma rota de erro final que tenta engatilhar numa tabela isolada (`dl_erros_criticos`), ou manda alerta para o seu Discord/Telegram.

---

## 5. Plano de Deploy Escalado (Próximos Passos)
1. Rodar `MIGRATIONS_DL_NEXUS_V6_ENTERPRISE.sql` no Painel do Supabase.
2. Importar o novo `001_webhook_receptor_enterprise.json` na HostGator e deletar a versão V1.
3. Refatorar o Front-End para absorver os KPIs (Dashboard DL Commander).
