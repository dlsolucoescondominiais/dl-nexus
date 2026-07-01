# Checklist de Testes - MVP DL Orçamento (Fase 1)

## 1. Banco de Dados (Supabase)
- [ ] Executar o script `schema.sql` no Supabase SQL Editor.
- [ ] Confirmar se todas as tabelas foram criadas.
- [ ] Inserir os serviços de teste na tabela `servicos_catalogo` e verificar (ex: "DL Guardião", "DL Volt").
- [ ] Inserir configurações base na tabela `configuracoes_precificacao`.

## 2. API e Webhooks (n8n)
- [ ] Enviar payload de teste POST para `/api/n8n/webhook` sem Authorization.
  - *Esperado:* Retorno 401 Não Autorizado.
- [ ] Enviar payload de teste com Authorization incorreto.
  - *Esperado:* Retorno 401 Não Autorizado.
- [ ] Enviar payload válido simulando n8n (action: 'criar_avaliacao_tecnica').
  - *Esperado:* Retorno 201 Created.

## 3. Front-end (Next.js)
- [ ] Executar `npm run build` e confirmar que não há erros de tipagem TypeScript.
- [ ] Acessar página inicial (`/`) - Dashboard deve renderizar os cards básicos.
- [ ] Acessar `/avaliacoes-tecnicas/nova` - Formulário deve carregar sem erros.
- [ ] Acessar `/orcamentos` - Tabela de listagem mockada deve carregar.
- [ ] Acessar `/orcamentos/novo` - Tela com layout de duas colunas e carrinho lateral deve carregar.

## 4. Lógica de Precificação
- [ ] Testar função `calcularResumoOrcamento` (em script ou jest futuramente) com 1 material R$ 1000 + 1 mão de obra R$ 500.
- [ ] Testar a aplicação da margem (ex: 30%) em cima do custo base R$ 1500.
- [ ] Testar aplicação do imposto (ex: 15%) com a fórmula de gross-up e validar o Valor Final.
