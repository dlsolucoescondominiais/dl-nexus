# Plano do Agente 067 — Evolução de Orçamentos DL

**Data:** 2026-06-21
**Status:** 🔵 PLANEJADO (Fase 5 da Arquitetura)

---

## 1. Missão do Agente

O `067_AGENTE_EVOLUCAO_ORCAMENTOS_DL` é o cérebro de melhoria contínua do Motor de Orçamentos. Ele analisa orçamentos já feitos e sugere melhorias no sistema inteiro — sem jamais apagar, sobrescrever ou alterar o histórico.

**Analogia:** Um auditor de qualidade que lê todas as propostas enviadas, compara com os resultados reais (fechou/não fechou, margem real vs estimada) e emite um relatório com sugestões práticas.

---

## 2. Gatilho de Execução

| Modo | Frequência | Descrição |
|---|---|---|
| **CRON semanal** | Toda segunda-feira 7h | Analisa todos os orçamentos da semana anterior |
| **Manual** | Sob demanda via Telegram | Diogo ou Nielton disparam com `/evolucao` |
| **Pós-envio** | Após cada `066_ENVIO` | Análise leve individual do orçamento recém-enviado |

---

## 3. Fontes de Dados

- **Supabase** (`dl_orcamentos_site_v2`): Histórico de leads e orçamentos.
- **Google Sheets**: Planilha operacional com valores reais de materiais e mão de obra.
- **Google Drive**: PDFs enviados (versões congeladas).
- **Feedback Telegram**: Status manual (ganhou/perdeu/em negociação).

---

## 4. Capacidades do Agente

### 4.1 Análise de Orçamentos Feitos
- Comparar proposta enviada vs resultado (fechou ou não).
- Calcular margem real vs margem estimada.
- Identificar padrões: "Sempre perco orçamento de CFTV acima de R$X em Copacabana".

### 4.2 Detecção de Erros
- Erro de cálculo: soma de materiais não bate com total.
- Campos faltantes: orçamento enviado sem `endereco_completo` ou `numero_unidades`.
- Inconsistência de unidade: metro linear vs metro quadrado.
- Margem negativa ou abaixo do limiar mínimo.

### 4.3 Sugestões de Evolução
- **Formulário:** "Os últimos 5 orçamentos de restaurante não tinham `voltagem_disponivel`. Sugestão: tornar esse campo visível para perfil restaurante."
- **Google Sheets:** "A coluna de mão de obra está usando valor fixo R$80/h, mas os últimos 3 trabalhos em Niterói custaram R$95/h de deslocamento. Sugestão: criar faixa por região."
- **Google Docs:** "O template não tem espaço para SLA de garantia. Sugestão: adicionar seção de garantia pós-instalação."
- **Markdown:** "O campo `observacoes_internas` está chegando vazio em 70% dos orçamentos. Sugestão: transformar em dropdown com opções pré-definidas."

### 4.4 Geração de Relatório

Formato do relatório semanal:

```markdown
# Relatório de Evolução — Semana XX/2026

## Orçamentos Analisados: N
## Fechados: X | Perdidos: Y | Em negociação: Z

## Erros Detectados
- [ORC-V2-ABC123] Margem negativa no material X
- [ORC-V2-DEF456] Campo endereco_completo vazio

## Sugestões de Melhoria
1. Formulário: adicionar campo voltagem_disponivel para restaurantes
2. Sheets: atualizar tabela de mão de obra por região
3. Template: incluir seção de garantia

## Métricas
- Taxa de conversão: XX%
- Margem média: XX%
- Ticket médio: R$ X.XXX
- Bairro mais ativo: XXXX
- Serviço mais pedido: XXXX
```

---

## 5. Regras Invioláveis

1. **NUNCA apagar orçamento.** Mesmo com erro, manter e marcar como `erro_detectado`.
2. **NUNCA sobrescrever orçamento enviado.** Alteração = nova versão (`v2`, `v3`).
3. **NUNCA alterar histórico sem criar nova versão.** Auditoria completa.
4. **NUNCA usar CPF para busca pública automática.**
5. **Sugerir, nunca impor.** As sugestões vão para o relatório e para o Telegram. Diogo decide o que implementar.

---

## 6. Modelo de IA

| Tarefa | Modelo | Custo |
|---|---|---|
| Análise de padrões | DeepSeek ou Gemini Flash | Baixo |
| Geração de relatório | DeepSeek ou Gemini Flash | Baixo |
| Auditoria de margem crítica | Claude Sonnet ou GPT-4o | Médio (sob demanda) |

---

## 7. Dependências

- Necessita de histórico acumulado (mínimo ~20 orçamentos reais).
- Necessita de feedback manual sobre resultado (ganhou/perdeu).
- Idealmente conectado ao CRM futuro ou ao campo `status_orcamento` no Supabase.
