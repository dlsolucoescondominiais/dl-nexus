# LISTA DE PENDÊNCIAS CRÍTICAS DA DL NEXUS

Abaixo encontram-se as urgências estruturais que impedem a liberação de workflows de "Pausados/Homologação" para "Ativo (Produção)".

## 1. Meta API (Publicação Automática N8N)
- **Token Definitivo Cloud:** A variável de ambiente do `Page Access Token` atualizada recentemente só foi aplicada aos arquivos locais de homologação (`.env` local, etc.). É necessário fazer a inserção real no servidor n8n cloud / Railway para que os workflows 082 e 081 operem.
- **Instagram Content Publish:** O token tem permissão, mas o workflow `081_PUBLICADOR_INSTAGRAM_META_API` falhará até que uma `image_url` HTTPS 100% pública válida seja fornecida dinamicamente ou estaticamente ao payload JSON de publicação.

## 2. Rotação de Credenciais e Segurança Git
- **Alerta GH013 (Histórico do GitHub):** Embora o push local tenha sido limpo (`rebase` / exclusão física nos arquivos `*_SAFE.json`), **apenas limpar não basta**. A credencial original que foi exposta um dia no passado precisa ser rodada (revogada no emissor e gerada uma nova chave) para prevenir roubo de dados se alguém copiou o histórico antes.

## 3. Implementação Oficial Orçamentos V2
- **Homologação Prolongada:** O ambiente V2 (workflows 061 a 064) foi desenhado e estruturado, mas depende da injeção de conexões reais do Google Docs/Sheets no n8n e ativação das credenciais de serviço. 
- **Substituição do Fallback:** A ativação do webhook oficial (`/webhook/orcamento-v2`) no frontend da DL Nexus. Atualmente, a recepção continua fluindo pelo fallback do `#dl-contact-form`.

## 4. Remoção Física Manus.IA
- **Limpeza de Variáveis:** As variáveis `MANUS_API_KEY` devem ser apagadas de fato do ambiente cloud Railway/Docker. Os arquivos locais já as isolaram ou depreciaram.

---
*Nenhuma destas tarefas deve ser burlada ("fake it till you make it") sem testes reais comprovando as URLs, Posts IDs ou respostas de banco de dados.*
