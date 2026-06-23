const fs = require('fs');

const css = \
:root {
  --dl-bg: #f7f9fb;
  --dl-bg-alt: #eef2f6;
  --dl-text: #253444;
  --dl-text-muted: #5b6b7c;
  --dl-surface: #ffffff;
  --dl-border: #d8e0e8;
  --dl-blue-dark: #0b1f33;
  --dl-blue: #123a5f;
  --dl-blue-light: #1d5d8f;
  --dl-gold: #d9a441;
  --dl-danger: #b42318;
  --dl-success: #087443;
  --shadow-soft: 0 16px 40px rgba(11, 31, 51, 0.12);
  --radius-lg: 22px;
  --radius-md: 14px;
  --max-width: 1180px;
}

[data-theme="dark"] {
  --dl-bg: #071827;
  --dl-bg-alt: #0b1f33;
  --dl-text: #f7f9fb;
  --dl-text-muted: #d8e0e8;
  --dl-surface: #123a5f;
  --dl-border: #1d5d8f;
  --shadow-soft: 0 16px 40px rgba(0, 0, 0, 0.4);
}

* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  font-family: 'Inter', Arial, sans-serif;
  color: var(--dl-text);
  background: var(--dl-bg);
  line-height: 1.6;
  transition: background 0.3s ease, color 0.3s ease;
}
a { color: inherit; text-decoration: none; }
.container { width: min(100% - 32px, var(--max-width)); margin-inline: auto; }

/* HEADER */
.header {
  background: var(--dl-surface);
  border-bottom: 1px solid var(--dl-border);
  position: sticky;
  top: 0;
  z-index: 100;
  padding: 15px 0;
}
.header-inner { display: flex; align-items: center; justify-content: space-between; }
.logo { font-size: 1.5rem; font-weight: 700; color: var(--dl-blue-dark); display: flex; align-items: center; gap: 10px; }
.nav-links { display: flex; gap: 20px; }
.nav-links a { font-weight: 500; color: var(--dl-text); transition: color 0.2s; }
.nav-links a:hover { color: var(--dl-gold); }
.header-actions { display: flex; align-items: center; gap: 15px; }
.theme-toggle { background: none; border: none; font-size: 1.5rem; cursor: pointer; color: var(--dl-text); }
.btn {
  display: inline-flex; align-items: center; justify-content: center;
  padding: 12px 24px; border-radius: var(--radius-md); font-weight: 600;
  transition: all 0.3s ease; cursor: pointer; border: none;
}
.btn-primary { background: var(--dl-gold); color: var(--dl-blue-dark); }
.btn-primary:hover { filter: brightness(1.1); transform: translateY(-2px); }
.btn-secondary { background: var(--dl-blue); color: #fff; }
.btn-secondary:hover { background: var(--dl-blue-dark); }

/* HERO */
.hero {
  padding: 80px 0; text-align: center;
  background: linear-gradient(180deg, var(--dl-bg), var(--dl-bg-alt));
}
.hero h1 { font-size: 3rem; color: var(--dl-blue-dark); margin-bottom: 20px; }
.hero p { font-size: 1.2rem; color: var(--dl-text-muted); max-width: 800px; margin: 0 auto 40px; }

/* CARDS */
.features { padding: 80px 0; }
.features-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; }
.card {
  background: var(--dl-surface); border: 1px solid var(--dl-border);
  border-radius: var(--radius-lg); padding: 30px;
  box-shadow: var(--shadow-soft); transition: transform 0.3s;
}
.card:hover { transform: translateY(-5px); }
.card h3 { color: var(--dl-blue-dark); margin-top: 0; }

/* FOOTER */
.footer { background: var(--dl-surface); border-top: 1px solid var(--dl-border); padding: 40px 0; text-align: center; margin-top: 50px;}
.footer-links { display: flex; justify-content: center; gap: 20px; margin-bottom: 20px; }
.footer p { color: var(--dl-text-muted); font-size: 0.9rem; }
\;

const waSvg = \<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512" style="width:18px;height:18px;margin-right:8px;fill:currentColor;"><path d="M380.9 97.1C339 55.1 283.2 32 223.9 32c-122.4 0-222 99.6-222 222 0 39.1 10.2 77.3 29.6 111L0 480l117.7-30.9c32.4 17.7 68.9 27 106.1 27h.1c122.3 0 224.1-99.6 224.1-222 0-59.3-25.2-115-67.1-157zM223.9 413.4c-33 0-65.5-8.9-94-25.7l-6.7-4-69.8 18.3L72 334.2l-4.4-7c-18.5-29.4-28.2-63.3-28.2-98.2 0-101.7 82.8-184.5 184.6-184.5 49.3 0 95.6 19.2 130.4 54.1 34.8 34.9 56.2 81.2 56.1 130.5 0 101.8-84.9 184.6-186.6 184.6zm101.2-138.2c-5.5-2.8-32.8-16.2-37.9-18-5.1-1.9-8.8-2.8-12.5 2.8-3.7 5.6-14.3 18-17.6 21.8-3.2 3.7-6.5 4.2-12 1.4-32.6-16.3-54-29.1-75.5-66-5.7-9.8 5.7-9.1 16.3-30.3 1.8-3.7.9-6.9-.5-9.7-1.4-2.8-12.5-30.1-17.1-41.2-4.5-10.8-9.1-9.3-12.5-9.5-3.2-.2-6.9-.2-10.6-.2-3.7 0-9.7 1.4-14.8 6.9-5.1 5.6-19.4 19-19.4 46.3 0 27.3 19.9 53.7 22.6 57.4 2.8 3.7 39.1 59.7 94.8 83.8 35.2 15.2 49 16.5 66.6 13.9 10.7-1.6 32.8-13.4 37.4-26.4 4.6-13 4.6-24.1 3.2-26.4-1.3-2.5-5-3.9-10.5-6.6z"/></svg>\;

const html = \<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DL Soluções Condominiais</title>
  <style>\</style>
</head>
<body>

  <header class="header">
    <div class="container header-inner">
      <a href="index.html" class="logo">
        DL Soluções
      </a>
      <nav class="nav-links">
        <a href="portifolio.html">Portfólio</a>
        <a href="a-empresa.html">A Empresa</a>
        <a href="o-fundador.html">O Fundador</a>
      </nav>
      <div class="header-actions">
        <button class="theme-toggle" id="theme-toggle" aria-label="Alternar Tema Claro/Escuro">??</button>
        <a href="https://wa.me/5521968782196?text=Quero%20solicitar%20uma%20Avalia%C3%A7%C3%A3o%20el%C3%A9trica" class="btn btn-primary">\ Solicitar Avaliação</a>
      </div>
    </div>
  </header>

  <section class="hero">
    <div class="container">
      <h1>Engenharia e Tecnologia para o seu Condomínio</h1>
      <p>CFTV IP, Controle de Acesso Facial, Automação Predial, Instalações Elétricas e Usinas Solares no Rio de Janeiro.</p>
      <a href="https://wa.me/5521992698612?text=Vi%20um%20anuncio%20da%20DL%20e%20quero%20saber%20mais" class="btn btn-secondary" style="font-size: 1.1rem;">\ Falar com um Engenheiro Agora</a>
    </div>
  </section>

  <section class="features">
    <div class="container">
      <div class="features-grid">
        <article class="card">
          <h3>Suporte Operacional</h3>
          <p>Atendimento exclusivo para condomínios com contrato ativo de manutenção.</p>
          <br>
          <a class="btn btn-secondary" href="https://wa.me/5521964742458?text=Sou%20cliente%20da%20DL%20e%20preciso%20de%20suporte" style="width: 100%;">\ Falar com o Suporte</a>
        </article>
        
        <article class="card">
          <h3>Comercial (Projetos e Obras)</h3>
          <p>Canal para novos orçamentos, infraestrutura elétrica e sistemas de CFTV.</p>
          <br>
          <a class="btn btn-primary" href="https://wa.me/5521968782196?text=Quero%20solicitar%20uma%20Avalia%C3%A7%C3%A3o%20el%C3%A9trica" style="width: 100%;">\ Falar com Comercial</a>
        </article>

        <article class="card">
          <h3>Plantão Comercial Express</h3>
          <p>Canal imediato para novas solicitações e avaliação técnica expressa para o seu condomínio.</p>
          <br>
          <a class="btn btn-primary" href="https://wa.me/5521992698612?text=Vi%20um%20anuncio%20da%20DL%20e%20quero%20saber%20mais" style="width: 100%;">\ Solicitar Orçamento via WhatsApp</a>
        </article>
      </div>
    </div>
  </section>

  <footer class="footer">
    <div class="container">
      <div class="footer-links">
        <a href="lgpd-gdpr.html">LGPD / GDPR</a>
        <a href="politica-privacidade.html">Política de Privacidade</a>
      </div>
      <p>&copy; 2025 DL Soluções Condominiais LTDA - CNPJ 36.354.697/0001-46. Todos os direitos reservados.</p>
    </div>
  </footer>

  <script>
    const toggleBtn = document.getElementById('theme-toggle');
    const currentTheme = localStorage.getItem('theme') || 'light';
    if (currentTheme === 'dark') document.documentElement.setAttribute('data-theme', 'dark');

    toggleBtn.addEventListener('click', () => {
      const theme = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', theme);
      localStorage.setItem('theme', theme);
    });
  </script>
</body>
</html>\;

fs.writeFileSync('index.html', html);
