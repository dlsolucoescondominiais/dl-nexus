# Guia de Uso: Deploy Social 08X DL Nexus V3

**Arquivo:** `DEPLOY_SOCIAL_08X_N8N.ps1`
**Data:** 22 de Maio de 2026
**Responsável:** Diogo Luiz de Oliveira - Tecnólogo Responsável

---

## 1. O que este script faz?

Este script PowerShell automatiza totalmente o deploy da esteira de publicação social (workflows 081 a 085) da máquina local para a VPS de produção (`n8n.dlsolucoescondominiais.com.br`).

**Ações automatizadas:**
1. Lê os arquivos `_config.json` originais da pasta `20_UPLOAD_N8N`.
2. Corrige o ID raiz (`id`) de cada JSON para bater com o prefixo (081, 082, etc.), evitando conflitos no banco do n8n.
3. Força a flag `"active": false` no payload para garantir que não haja disparo acidental.
4. Gera arquivos temporários com o sufixo `_FIXED.json`.
5. Transfere os arquivos processados para a VPS via `scp` (protocolo SSH).
6. Usa `docker cp` para injetar os arquivos dentro do container Docker `n8n-main`.
7. Executa o comando de importação CLI (`n8n import:workflow`) na **ordem estrita de dependência**:
   - `084` (TikTok)
   - `082` (Facebook)
   - `081` (Instagram)
   - `083` (Google Business)
   - `085` (Dispatcher)
8. Verifica o sucesso de cada comando.
9. Se e somente se **todos** importarem com sucesso, executa `docker restart n8n-main` para aplicar mudanças na memória cache.
10. Remove todos os arquivos temporários criados e gera um relatório `.txt` na pasta `05_RELATORIOS`.

---

## 2. Pré-requisitos para execução

Antes de rodar o script, você deve garantir que:
- O sistema possui cliente `ssh` e `scp` configurados e acessíveis via PowerShell.
- Sua chave SSH pública está autorizada na VPS (`n8n.dlsolucoescondominiais.com.br`) para o usuário especificado (`root` por padrão no script).
- Você testou o acesso executando: `ssh root@n8n.dlsolucoescondominiais.com.br`. Se não pedir senha, a chave está OK.
- Os arquivos originais (ex: `081_PUBLICADOR_INSTAGRAM_META_API_config.json`) estão íntegros na pasta `20_UPLOAD_N8N`.

---

## 3. Como executar

Abra o terminal do PowerShell como Administrador e navegue até a pasta raiz do projeto.

```powershell
cd D:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\30_DEPLOY_N8N
.\DEPLOY_SOCIAL_08X_N8N.ps1
```

> **Aviso de Política de Execução:** Se o Windows bloquear a execução de scripts `.ps1`, rode este comando antes de executar o deploy:
> `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`

---

## 4. O que verificar após a execução

- Abra a pasta `05_RELATORIOS` e confira o `RELATORIO_DEPLOY_SOCIAL_08X_YYYYMMDD_HHMMSS.txt`.
- Acesse o painel do n8n e valide se os novos workflows (081-085) constam na lista.
- Certifique-se de que todos estão **Inativos** (active=false).
- Proceda com a atualização dos placeholders (`PAGE_ID_AQUI`, etc.) manualmente pelo n8n, como documentado no Relatório de Ativação Geral.

---

## 5. Riscos e Tratativas

- **Erro de Conexão SSH:** O script usa `ErrorActionPreference = "Stop"`. Se a rede cair ou o SSH não conectar, ele abortará o deploy sem corromper a VPS.
- **Conflito de ID:** Resolvido pela injeção forçada do ID base no script antes do upload.
- **Workflow Ativado Acidentalmente:** Resolvido pela injeção forçada de `active=false`. O n8n vai respeitar essa flag e deixá-los inativos.
- **Importação Falha:** Se um import falhar (ex: schema inválido), o script registrará o erro no console, pulará o reboot do n8n e registrará a falha no relatório final, garantindo a estabilidade da VPS.
