# Plano de Organização do Repositório - DL Nexus V3

**Objetivo:** Estabelecer a ordem e a arquitetura oficial do repositório da DL Soluções Condominiais, eliminando o caos de arquivos espalhados, subprojetos injetados incorretamente e duplicidades.

## 1. Classificação Estrutural de Pastas

Para manter a sanidade do projeto, todos os arquivos devem obedecer à seguinte categorização estrita:

### 🟢 1. Produção (Fonte da Verdade)
*Pasta:* `DL_NEXUS_V3_LOCAL\09_PRONTOS_PARA_PRODUCAO\`
- **Regra:** Contém apenas JSONs de workflows n8n testados, validados pelo KILLCRITIC e com `active: false`.
- **Ação Git:** Tracking rigoroso. Nenhuma alteração direta sem commit descritivo.

### 🟡 2. Pronto para n8n (Upload)
*Pasta:* `DL_NEXUS_V3_LOCAL\20_UPLOAD_N8N\`
- **Regra:** Contém réplicas exatas da produção, com sufixo opcional `_config_FIXED.json` após injeção de IDs corretos para deploy na VPS.
- **Ação Git:** Rastreável. Serve de ponte entre o local e o Docker container do n8n.

### 🔵 3. Rascunhos e Próximos
*Pasta:* `DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS\`
- **Regra:** Ambiente de desenvolvimento para o Manus e Antigravity. Workflows em construção ou revisão.
- **Ação Git:** Rastreado, mas sujeito a mudanças constantes.

### 🟠 4. Quarentena / Avaliação
*Pasta:* `DL_NEXUS_V3_LOCAL\99_QUARENTENA\`
- **Regra:** Códigos suspeitos, workflows quebrados ou legados em análise de descarte.
- **Ação Git:** Rastreado temporariamente até decisão final.

### 🟤 5. Legado Histórico
*Pasta:* `DL_NEXUS_V3_LOCAL\98_LEGADO\`
- **Regra:** Workflows antigos substituídos (ex: V1 e V2). Mantidos para fallback.
- **Ação Git:** Arquivados. Read-only.

### 🔴 6. Ignorar no Git (.gitignore)
*Arquivos:* `.env`, `node_modules/`, `venv/`, arquivos de log locais, `*.log`, `__pycache__/`, tokens soltos (`token_arquivista.json`).
- **Ação Git:** Adicionar no `.gitignore` imediatamente. Remover do tracking se já estiverem (`git rm --cached`).

### 🟣 7. Revisão Manual Pendente
*Pastas suspeitas encontradas no repositório:* `backend/picoclaw`, `frontend_react_dl`.
- **Regra:** Código de terceiros ou frontends desacoplados não devem poluir o core da IA do n8n.
- **Próxima Ação:** Diogo precisa analisar e mover para repositórios próprios ou aplicar `git submodule`.

---

## 2. Ações Imediatas (Próximo Deploy)

1. **Rodar Auditor.** O script `AUDITOR_ORGANIZADOR_GITHUB_DL_NEXUS.ps1` já está na pasta `30_DEPLOY_N8N`.
2. **Avaliar Relatório.** Ler as saídas no `RELATORIO_AUDITORIA_GITHUB_ORGANIZACAO_DL_NEXUS.md`.
3. **Limpar a Raiz.** Mover scripts python como `01_gerar_n8n...py`, `gerar_manus_prospeccao.py`, `corrigir_workflows...py` para uma pasta como `DL_NEXUS_V3_LOCAL\30_DEPLOY_N8N\PYTHON_TOOLS`.
4. **Validar Segredos.** Caso o auditor aponte segredos expostos, alterar a senha/token na plataforma origem IMEDIATAMENTE (o GitHub histórico já os vazou internamente).

> **Aviso de Execução:** Antigravity e Manus não estão autorizados a executar exclusões (rm) no GitHub sem o consentimento direto do Tecnólogo Responsável da DL. A execução deste plano de reestruturação física demanda um OK explícito.
