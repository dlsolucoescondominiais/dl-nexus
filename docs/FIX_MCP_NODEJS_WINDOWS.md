# Correção de Erro MCP no Windows: 'exec: "npx": executable file not found in %PATH%'

Se os seus servidores MCP falharam no Windows com o erro dizendo que `npx` não foi encontrado, é porque o Node.js não está instalado ou o seu editor de código ainda não detectou o Node.js na variável de ambiente `%PATH%`.

## Como Resolver (Passo a Passo)

### Opção 1: Usando o Script Automático

Nós criamos um script para automatizar a instalação para si.
1. Abra o PowerShell como Administrador.
2. Navegue até o diretório do projeto e execute:
   ```powershell
   .\scripts\install_nodejs.ps1
   ```
*(Se receber um erro de "Execution Policy", corra `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` primeiro).*

### Opção 2: Instalação Manual

Se preferir resolver manualmente:
1. Abra o Terminal (PowerShell ou CMD) e digite o seguinte comando do Winget:
   ```cmd
   winget install OpenJS.NodeJS.LTS --silent
   ```
2. **Se o Winget falhar ou não existir:** Faça o download do instalador oficial aqui: [https://nodejs.org/en/download/](https://nodejs.org/en/download/). Certifique-se de baixar a versão LTS (Recommended) e avance no instalador padrão clicando em 'Next'.

---

## 🚨 O PASSO MAIS IMPORTANTE: ATUALIZAR O PATH

O Windows instalou o Node.js e modificou a variável `%PATH%`, mas os programas que **já estavam abertos** (como o VS Code ou o Cursor) não herdam essa nova variável em tempo real. Eles continuam usando o PATH que estava ativo no momento em que foram iniciados.

Para que o editor volte a carregar os servidores MCP:
1. Feche o VS Code ou Cursor **por completo**. Se possível, aceda ao Gestor de Tarefas (`Ctrl + Shift + Esc`) e garanta que não há nenhum processo do editor a correr no fundo.
2. Reinicie o editor de código.
3. Se quiser confirmar antes de tudo, abra um Novo Terminal dentro do editor e digite `npx -v`. Ele agora deve retornar um número de versão.
