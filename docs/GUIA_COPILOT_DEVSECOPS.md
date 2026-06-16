# Guia de DevSecOps: Configuração e Governança do GitHub Copilot / Cursor

Bem-vindo ao guia de implantação de Assistentes de IA (GitHub Copilot e Cursor) para o ambiente de desenvolvimento da DL Soluções Condominiais. Como Engenheiro DevSecOps Sênior, estruturei este documento para garantir produtividade, segurança e alinhamento total com as **Hard Rules** comerciais do negócio B2B.

---

## 1. Configuração Inicial e Integração de Contexto

Para que o Copilot/Cursor entenda o nosso stack (Next.js, Tailwind, Supabase) e o ecossistema do DL Nexus, siga estes passos:

### No VS Code (GitHub Copilot)
1. Instale a extensão **GitHub Copilot** e **GitHub Copilot Chat**.
2. **Contexto Automático:** O Copilot lê automaticamente os arquivos abertos e o workspace ativo. Mantenha abertos os arquivos relacionados à tarefa que você está executando (ex: se estiver mexendo em autenticação, abra `supabaseClient.ts` e o componente de login).
3. **Instruções Personalizadas (Custom Instructions):** O VS Code agora suporta instruções personalizadas via arquivo local. Já criamos e adicionamos o arquivo ao repositório para você.

### No Cursor (AI Code Editor)
O Cursor possui uma integração ainda mais profunda com a base de código.
1. Abra as configurações (Settings > General > Rules for AI).
2. O arquivo `.cursorrules` (que criamos neste commit) na raiz do projeto será automaticamente lido pelo Cursor para **todo** o repositório, impondo as regras em qualquer chat ou geração de código.
3. Para dar contexto de pastas específicas ao usar `Cmd+K` ou o Chat, mencione `@frontend/src` ou `@backend/supabase`.

---

## 2. Regras de Governança (Hard Rules) Ativadas

Nós criamos dois ficheiros chave que já foram comitados na raiz do repositório:

- `.github/copilot-instructions.md`: Arquivo padrão lido pelo Copilot Chat no VS Code para injetar regras globais no prompt de sistema da IA.
- `.cursorrules`: Arquivo de regras estritas nativo do editor Cursor.

### O que estes ficheiros impõem à IA?
*   **Regra da Visita (Proibido):** A IA foi instruída a NUNCA sugerir a palavra "visita técnica" nos botões, variáveis ou copy. Ela foi forçada a utilizar `"Avaliação Técnica"`.
*   **Regra de Materiais (Padrão Engenharia):** Foi bloqueado o uso e sugestão de "canaletas plásticas". A IA substituirá proativamente por `"eletrodutos galvanizados"`.
*   **Tom B2B e OPEX:** A IA vai priorizar variáveis como `contratoOpex` em vez de `venda` e focará em "SLA", "CREA-RJ" e "Segurança Jurídica".

---

## 3. Boas Práticas: Como "Falar" com o Copilot

A forma como escreves os teus comentários (Prompt Engineering In-Code) muda completamente a qualidade do código gerado:

### ❌ O que NÃO fazer (Genérico)
```javascript
// cria um form de contato
function Form() { ... }
```
*(O Copilot vai gerar um form genérico B2C, provavelmente com o botão "Agendar Visita".)*

### ✅ O que FAZER (Contexto B2B + Stack)
```typescript
// [Next.js Client Component] Formulário de Lead B2B para o DL Commander.
// Capta Nome, Condomínio e Telefone.
// Utiliza Server Actions para enviar ao Supabase.
// O botão de submit deve convidar o síndico para a 'Avaliação Técnica'.
export default function LeadForm() {
  // ... Copilot vai assumir aqui com alta precisão
}
```

### ✅ Dicas de DevSecOps In-Code
Sempre inicie scripts de banco de dados ou funções de autenticação com barreiras explícitas:
```typescript
// WARNING: Função de servidor (Server Action).
// Validar se usuário está autenticado no Supabase antes de prosseguir.
// Recuperar dados com RLS ativo usando createServerClient.
```
*(Isto força o Copilot a envolver o seu código em blocos `try/catch` seguros e validação de sessão, evitando vazamentos de chaves ou bypass de segurança.)*

---
**Status da Implantação:** Ficheiros `.cursorrules` e `.github/copilot-instructions.md` criados e aplicados com sucesso ao repositório.
