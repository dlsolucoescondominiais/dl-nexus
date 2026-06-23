# Configuração de Escalonamento via Telegram — Aninha DL Nexus

Este documento detalha como a Aninha escala leads qualificados para o Diogo através do Telegram.

## 1. Por que usar o Telegram?
O WhatsApp é restrito e pago (Meta API) para envio de notificações ativas do sistema para a equipe. O Telegram é 100% gratuito, tem API fácil de usar e permite criar bots de alerta com entrega instantânea.

## 2. Onde configurar
No n8n, a variável de ambiente `TELEGRAM_DIOGO_CHAT_ID` ou a configuração direta no nó **Notificar Diogo** exige o número de identificação do chat.

## 3. Como descobrir o seu Chat ID
1. Abra o Telegram e busque por `@userinfobot` ou `@RawDataBot`.
2. Mande um `/start`.
3. O bot responderá com os seus dados, incluindo o campo `Id`. Exemplo: `Id: 123456789`.
4. Copie esse número.

## 4. Como configurar no n8n
1. Abra o workflow `002_roteador_aninha_v3_atendimento`.
2. Acesse o nó **Notificar Diogo** (Telegram).
3. Cole o ID numérico no campo **Chat ID**.
4. Salve e teste o nó manualmente.

## 5. Formato da Mensagem Recebida
Você receberá alertas neste formato sempre que a Aninha qualificar um lead (ou seja, quando ela extrair telefone + bairro + serviço):

```text
🔥 NOVO LEAD QUALIFICADO — Aninha DL Nexus

📋 Produto: Fortress
👤 Nome: Síndico Carlos
📍 Bairro: Barra da Tijuca
📞 Telefone: 21999999999

💬 Mensagem Original:
Preciso colocar uma portaria inteligente no meu prédio, a remota tá muito cara.

🎯 Próximo passo: Entrar em contato e agendar Avaliação Técnica.
⚡ Escalonamento automático via n8n.
```
