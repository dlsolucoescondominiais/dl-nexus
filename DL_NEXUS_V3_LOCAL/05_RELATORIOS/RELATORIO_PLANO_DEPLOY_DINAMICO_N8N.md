# Relatório de Deploy Dinâmico do n8n

1. **Problema atual**:
   Jules atualiza o GitHub, mas isso não atualiza automaticamente o n8n.

2. **Solução proposta**:
   Pipeline controlado de deploy para importar JSON no n8n real via scripts seguros.

3. **Fluxo final desejado**:
   Jules gera workflow -> KILLCRITIC valida -> Arquivo vai para 20_UPLOAD_N8N -> script envia para VPS -> script faz backup -> script importa no n8n-main -> n8n reinicia -> Diogo testa no painel.

4. **Riscos**:
   - segredo exposto;
   - importação errada;
   - workflow duplicado;
   - workflow mock em produção;
   - workflow sem id;
   - erro no n8n;
   - ausência de rollback.

5. **Como evitar**:
   - backup antes;
   - JSON válido;
   - KILLCRITIC;
   - active=false;
   - relatório pós-deploy;
   - aprovação humana.

6. **Decisão arquitetural importante:**
   Os 135 workflows legados/scaffold/corrompidos foram excluídos do escopo deste PR. Eles serão tratados em tarefa separada de inventário e recuperação, sem impacto no deploy dinâmico atual.
