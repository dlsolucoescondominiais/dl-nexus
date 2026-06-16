# Configuração ManyChat -> n8n (Aninha) para Comentários em Redes Sociais

Este documento detalha o procedimento para capturar comentários no **TikTok**, **Instagram** e **Facebook** usando o ManyChat, e enviá-los para a IA Aninha no n8n.

## 1. Configurando o Gatilho no ManyChat

1. Acesse sua conta do ManyChat e vá em **Automações** -> **Nova Automação**.
2. No passo inicial (Trigger / Gatilho), adicione os seguintes gatilhos (conforme as plataformas que deseja conectar):
   - **Instagram:** "User comments on a Post or Reel" (Usuário comenta em um Post ou Reel).
   - **Facebook:** "User comments on a Post" (Usuário comenta em um Post).
   - **TikTok:** "User comments on a Video" (Usuário comenta em um Vídeo).
3. Configure as palavras-chave se desejar filtrar, ou deixe em branco para capturar qualquer comentário.

## 2. Configurando o Fluxo de Resposta e Captura

1. Após o gatilho, adicione um nó de **Send Message** (Enviar Mensagem) ou **Reply in Comments** (Responder nos Comentários) para dar um feedback imediato (ex: "Oi! Já vamos te atender no direct!").
2. Adicione uma **Ação** (Action) -> **Add Tag** (Adicionar Tag), por exemplo: `lead_comentario_rede_social`.

## 3. Disparando o Webhook para o n8n

Para enviar os dados para o n8n, adicione um último passo na sua automação do ManyChat:

1. Adicione um nó de **External Request** (Requisição Externa).
2. Configure a requisição:
   - **Method:** `POST`
   - **Request URL:** `https://n8n.dlsolucoescondominiais.com.br/webhook/manychat-entrada` *(Ajuste para a URL exata do seu webhook do n8n)*
3. Na aba **Headers**:
   - `Content-Type`: `application/json`
   - `X-DL-API-KEY`: `dl-nexus-auth-2026` *(Chave de segurança padrão do n8n)*
4. Na aba **Body** (Corpo), selecione `Add Full Subscriber Data` ou monte um JSON customizado:
   ```json
   {
     "origem": "manychat",
     "nome": "{{user_full_name}}",
     "telefone": "{{phone}}",
     "mensagem_original": "{{last_text_input}}",
     "plataforma": "TikTok/Instagram/Facebook"
   }
   ```
5. Salve e clique em **Publish** (Publicar) ou **Ativar**.

## 4. Roteamento no n8n

O n8n deve ter um workflow configurado para receber esse Webhook. O webhook atual (`001_webhook_receptor`) foi feito para a API oficial do Meta.
Você deve ter um novo workflow (ex: `014_manychat_receptor.json`) ou adaptar o `001` para ler o formato de payload acima e enviá-lo para a fila da **Aninha** via nó HTTP Request para o Antigravity (`/api/aninha/triagem`).

### Exemplo de Tratamento no n8n:
- **Webhook Node:** Escutando `POST /manychat-entrada` com Header Auth.
- **Set Node:** Mapear `{{$json.body.nome}}` e `{{$json.body.mensagem_original}}`.
- **HTTP Request Node:** Fazer POST para o Antigravity `https://api.dlsolucoescondominiais.com.br/api/aninha/triagem` passando o objeto formatado.
