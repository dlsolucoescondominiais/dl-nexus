# Tutorial de Desconexão: Expulsando o Vercel do seu GitHub

Para revogar definitivamente as permissões do Vercel e desvinculá-lo do seu repositório GitHub, siga os 3 passos abaixo:

### Passo 1: Acessar Aplicações no GitHub
1. Abra o GitHub e faça login na sua conta.
2. Clique na sua foto de perfil no canto superior direito e selecione **Settings** (Configurações).
3. No menu lateral esquerdo, role para baixo e clique em **Applications** (Aplicações) na seção *Integrations*.

### Passo 2: Revogar o Vercel nas Installed GitHub Apps
1. Na página *Applications*, certifique-se de estar na aba **Installed GitHub Apps**.
2. Encontre o **Vercel** na lista.
3. Clique em **Configure** (Configurar) ao lado do Vercel.
4. Role até o final da página (seção *Danger zone*) e clique no botão vermelho **Uninstall** ou **Suspend** (Desinstalar/Suspender).

### Passo 3: Revogar o Vercel nas Authorized OAuth Apps
1. Volte para a página principal de *Applications* (Settings > Applications).
2. Clique na aba **Authorized OAuth Apps**.
3. Encontre o **Vercel** na lista de aplicativos autorizados.
4. Clique nos três pontinhos (`...`) ao lado direito e selecione **Revoke** (Revogar permissão).

Pronto! O bot do Vercel foi expulso do seu GitHub. As implantações antigas vão parar de ser atualizadas e seu repositório estará limpo para focarmos 100% no Cloudflare Pages.
