# 🌐 DL Nexus - Interface Operacional (Camada 1)

Este é o frontend React da **DL Soluções Condominiais**. Ele conecta você (Técnico/Engenheiro de Vendas) e os Síndicos (Clientes) diretamente ao cérebro do sistema: **Supabase + n8n + IA**.

---

## 🛠️ Passo a Passo para Inicializar a Integração

A interface UI do Stitch gerou a casca, mas as entranhas agora estão vivas e respiram os dados do banco Supabase em tempo real.

### 1. Requisitos de Instalação

Abra o terminal na pasta raiz do frontend (`cd frontend`) e instale o pacote oficial do Supabase. Opcionalmente instale o `react-router-dom` para as rotas que criei.

```bash
npm install @supabase/supabase-js
npm install react-router-dom
```

Se precisar de Tailwind CSS (já embutido nos estilos do Dashboard):
```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### 2. Configure a Conexão Segura (.env)

Crie um arquivo chamado `.env` na pasta raiz do frontend (`frontend/.env`) contendo suas chaves do Supabase.

```env
# URL e Chave Pública do DL Nexus (Supabase)
# Nunca coloque a SERVICE_ROLE KEY aqui, apenas a ANON_KEY.
VITE_SUPABASE_URL=https://nejdtvkpiclagsnfljsz.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhb... (SUA CHAVE ANONIMA AQUI)

# URL da API do Motor Antigravity (IA / Automação via HostGator)
VITE_API_BASE_URL=https://api.dlsolucoescondominiais.com.br
```

*(Nota: Se usar Next.js, use `NEXT_PUBLIC_` no prefixo)*

### 3. Como a Mágica Acontece (O Fluxo de Dados)

Nossos 3 principais componentes desenvolvidos na pasta `src/components/`:

- **Login.tsx**: A porta de entrada. Usa o `supabase.auth.signInWithPassword`. Se o usuário for da empresa (Técnico), vai para o Dashboard. Se for cliente, vai pro Portal do Síndico.
- **Dashboard.tsx**: A Visão de Comando. Mostra o pipeline de vendas em *Tempo Real*. Usa `supabase.channel` para escutar novos leads que a "Aninha" (n8n) insere no banco. Sem recarregar a tela, ela atualiza sozinha.
- **Checklist.tsx**: O Módulo Commander do seu celular. Após a Avaliação Técnica, você aperta "Salvar", e o sistema insere o Checklist JSONB no banco, atualiza o Lead para "Avaliado" e acorda a IA de Orçamento para gerar a Proposta Automática.

### 4. Rodando o Projeto

Abra o terminal e execute: `npm run start` ou script dev equivalente.

Abra o navegador na porta padrão (ex: `localhost:5173`) e veja a automação B2B ganhar vida.
