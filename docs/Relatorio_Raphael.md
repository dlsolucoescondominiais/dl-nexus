# DL Nexus - Relatório de Manutenção e Atualizações (Para: Raphael / Equipe Técnica)

Este relatório reflete as últimas atualizações arquiteturais e correções feitas no orquestrador `n8n` e nas dependências de inteligência artificial (ElevenLabs).

## 1. Correção do Nó da ElevenLabs (N8N)
Havia um erro crítico de `Tipo de nó não reconhecido: n8n-nodes-base.elevenLabs` ao tentar publicar a "Aninha Especialista DL - Triagem Pro 2026".
- **O Problema:** A instância atual do n8n via Docker não possuía suporte nativo estável ao node built-in da ElevenLabs.
- **A Solução:** Substituímos a dependência do node nativo por um Nó genérico de **Requisição HTTP (HTTP Request)**.
- **Como Funciona Agora:** O nó dispara um `POST` direto para `https://api.elevenlabs.io/v1/text-to-speech/ID_DA_VOZ` passando o JSON body com a fala do Lead gerada pela OpenAI.

## 2. IDs de Voz Extraídos (ElevenLabs)
O script local `tmp/get_voices.py` foi criado para abstrair o trabalho de caçar IDs de voz personalizados na interface web. As APIs secretas de cada agente foram associadas separadamente no cofre do `.env` do servidor.
Para consultar as vozes ou fazer hardcode nos testes:
- **Aninha (Voice ID)**: `ZzG2cDFMg8y5xP4nhpJM`
- **Diego Tecnólogo (Voice ID)**: `zZ4a1Ltgr4UVsW20edRe`

## 3. Conflitos de Webhooks (WozTell)
Haviam colisões (duplicatas) do fluxo `002_roteador_aninha` interceptando a mesma rota `/webhook/dl-aninha`.
Após testes, apenas a versão mais nova (revisada com o Agente de Orçamentos implementado) deve ser mantida com o status **Ativo**. Em caso de novos erros de "Caminho do Webhook em Conflito", basta deletar os fluxos redundantes no painel principal, garantindo que exista apenas 1 webhook escutando a porta da Aninha.

## 4. Estrutura Pós-Triagem (Supabase e ElevenLabs)
A macro arquitetura de lead B2B está montada no "Motor de Triagem Inteligente (Central)":
1. Recebe Gatilho do WozTell.
2. Aninha avalia com GPT e usa ferramenta `Ferramenta: Supabase Save`.
3. IF determina Triagem: *Verdadeiro/Falso*.
4. ElevenLabs gera áudio de resposta via HTTP Request.
5. Alerta Diego repassa o lead para Telegram/WhatsApp usando notificação imediata.

Toda essa lógica encontra-se funcional assim que os nós HTTP recebem os *headers* de Auth adequados. E para qualquer alteração no código do motor orçamentista em Python, as novas lógicas ficam abstraídas no Supabase e consumidas pela Aninha via API.
