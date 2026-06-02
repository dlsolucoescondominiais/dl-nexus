# Relatório de Automação de Publicação Social (013_MAQUINA_DE_ATRACAO)

## Respostas:

- **O workflow publica automaticamente:** Sim, publicações são automáticas após validação técnica.
- **Depende de webhook manual:** Não. O fallback manual pode ser configurado, mas não bloqueia por padrão.
- **Telegram bloqueia publicação:** Não. O Telegram apenas recebe avisos sobre falhas ou sumários, mas não entra no caminho crítico da publicação.
- **KILLCRITIC ativo:** Sim, os testes verificam e bloqueiam conteúdo que viola as regras corporativas.
- **Canais configurados:** Configurações apontam para Facebook, Instagram, Google Meu Negócio e TikTok (conforme config de `fallback`). O n8n base publicado inclui Facebook, passível de adicionar as etapas subsequentes.
- **Tabela `conteudos_marketing` validada:** Sim.
- **Status usados na tabela:** `gerado`, `aprovado_killcritic`, `bloqueado_killcritic`, `publicado`, `erro_publicacao`.
- **Erros pendentes:** Não existem erros impeditivos detectados no fluxo principal, desde que as credenciais Postgres e HTTP Request estejam ativas.
- **Seguro para importar no n8n:** Sim.
- **Seguro para ativar produção:** Não, requer um teste controlado devido às credenciais de banco e da Meta Graph.

## Simulação:
- **Tema:** Manutenção preventiva de bombas em condomínios
- **Produto:** DL Partner + DL Volt
- **Canal:** Facebook, Instagram e Google Meu Negócio
- **Resultado Esperado:**
O workflow vai gerar o conteúdo de acordo com o prompt.
Se passar as condições `não contém visita técnica`, etc., entrará em aprovação KILLCRITIC.
Sendo aprovado, a linha do Postgres é atualizada e o texto cai para publicação (Facebook).
O status fica como 'publicado' e 'canal' é definido como 'facebook'. Em caso de erro, atualiza para 'erro_publicacao'.
