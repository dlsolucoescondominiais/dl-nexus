# Roadmap Técnico - Fase 2 e Além

## Fase 2: Integração e Autenticação (Próxima)
1. **Configurar Supabase Client**: Instalar `@supabase/supabase-js` e `@supabase/ssr`.
2. **Autenticação**: Configurar Login e Middleware para rotas protegidas usando Supabase Auth.
3. **Integração Front e Back**: Conectar as páginas estáticas às tabelas do Supabase (ler dados reais).
4. **CRUD de Itens do Orçamento**: Melhorar a UI da página de Novo Orçamento para adicionar itens dinamicamente (Materiais, Mão de Obra, Indiretos, BDI) em estados do React.

## Fase 3: Documentos e Clientes
1. **Geração de PDF**: Implementar conversão de HTML para PDF (ex: `puppeteer` via API ou bibliotecas como `@react-pdf/renderer`) para gerar as versões cliente e interna do orçamento.
2. **Módulo de Clientes (DL CRM)**: Implementar telas completas de criação e edição de clientes e locais de atendimento.
3. **Anexos**: Conectar o upload de anexos de avaliações técnicas com o Supabase Storage ou Google Drive via n8n.

## Fase 4: Automações (n8n)
1. **Pipeline de Aprovação**: Integrar n8n para realizar o fluxo automático após aprovação de orçamento (Cliente -> PDF -> Drive -> WhatsApp -> Email -> CRM -> Agenda Follow-up -> Notificação responsável).
2. **DL AI**: Integração de IA especialista em infraestrutura condominial para analisar fotos (apontar riscos como NBR 5410, sugerir materiais, custos) e gerar textos persuasivos de introdução para as propostas automaticamente.
3. **Cronograma Base**: Gerador de cronograma macro a partir dos itens do orçamento para apresentação no PDF.

## Fase 5: Financeiro e Partner (Futuro)
1. **DL Financeiro**: Lançamento automático de entradas (30%), medições e fluxo de caixa a partir do orçamento.
2. **DL Partner**: Tela específica para atendimento de chamados de manutenção recorrente (tempo de resposta).
