# 📱 Estratégia de Automação de Redes Sociais (Workflow 013)
**Visão Estratégica: DL Nexus (Diogo Luiz)**

---

## 1. O Problema
A DL Soluções precisa de uma presença constante nas redes sociais (Instagram, Facebook) para atrair síndicos, mas o tempo do Diogo (Tecnólogo) é valioso demais para ficar escrevendo posts.

## 2. A Solução: Máquina de Atração (Workflow 013)
Criamos um funil **Semi-Automático** (recomendação aceita) onde a IA faz 80% do trabalho pesado e o Diogo apenas aprova (20% de esforço para controle de qualidade).

### Os 4 Estágios do Motor de Conteúdo:

1. **Geração de Copy (IA - Gemini/OpenAI)**
   * **Gatilho:** Semanal (ou frequencia a definir).
   * **Ação:** IA gera textos abordando 3 Dores Principais (Elétrica, Solar, Segurança).
   * **Tom:** Profissional B2B, sem jargões complexos, focado em Síndicos.
   * **Destino:** Salva na tabela `conteudo_pendente_aprovacao`.

2. **Aprovação Manual (Dashboard DL Nexus)**
   * **Gatilho:** O Diogo acessa a aba "Marketing" no Dashboard React.
   * **Ação:** Lê o texto gerado pela IA. Clica em "Aprovar" ou "Refazer".
   * **Tempo:** ~30 segundos por post.
   * **Destino:** Move para a tabela `conteudo_aprovado`.

3. **Agendamento nas Redes (n8n + Meta API)**
   * **Gatilho:** Gatilho ativado assim que o status muda para "aprovado".
   * **Ação:** O n8n pega a imagem associada e o texto, e envia para a Graph API do Facebook/Instagram.
   * **Destino:** Salva na tabela `posts_agendados`.
   * **Resiliência:** Se a API da Meta falhar (Token expirou, etc), o sistema tenta novamente 3 vezes antes de alertar o Diogo no WhatsApp.

4. **Monitoramento de Performance**
   * **Gatilho:** Diário/Semanal.
   * **Ação:** Coleta de métricas (Likes, Cliques, Engajamento).
   * **Destino:** Salva na tabela `performance_posts` para exibir no Dashboard de ROI.

---

## 3. Próximos Passos (Aguardando Resposta do Diogo)
Para ligarmos essa máquina, precisamos definir:
1. **Credenciais Meta Business:** App ID, App Secret e Access Tokens com permissões estendidas (`pages_manage_posts`, etc).
2. **Frequência e Horário:** Vamos usar horários fixos ou otimizados pela Meta? Quantos posts semanais?
3. **Dores Foco:** Quais são as 3 dores exatas que mais convertem hoje (ex: Fogo em painel elétrico? Conta de luz alta? Invasão de guarita?)
