const fs = require('fs');

const pages = ['index.html', 'portifolio.html', 'a-empresa.html', 'o-fundador.html', 'lgpd-gdpr.html', 'politica-privacidade.html'];

const cssVariables = \
    /* LIGHT MODE */
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
    /* DARK MODE */
    --dl-bg: #071827;
    --dl-bg-alt: #0b1f33;
    --dl-text: #f7f9fb;
    --dl-text-muted: #d8e0e8;
    --dl-surface: #123a5f;
    --dl-border: #1d5d8f;
    --shadow-soft: 0 16px 40px rgba(0, 0, 0, 0.4);
  }\;

const jsToggle = \
<script>
  const toggleBtn = document.getElementById('theme-toggle');
  if (toggleBtn) {
    const currentTheme = localStorage.getItem('theme') || 'light';
    if (currentTheme === 'dark') document.documentElement.setAttribute('data-theme', 'dark');

    toggleBtn.addEventListener('click', () => {
      const theme = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', theme);
      localStorage.setItem('theme', theme);
    });
  }
</script>
</body>\;

const toggleBtnHtml = \<div class="header-actions">
        <button class="theme-toggle" id="theme-toggle" aria-label="Alternar Tema Claro/Escuro" style="background:none;border:none;cursor:pointer;font-size:1.5rem;margin-right:15px;color:var(--dl-text);">??</button>
        <a\;

pages.forEach(page => {
  if (!fs.existsSync(page)) return;
  let html = fs.readFileSync(page, 'utf8');
  
  // Inject CSS variables
  if (!html.includes('[data-theme="dark"]')) {
    html = html.replace(/:root\s*\{[^}]+\}/, ':root {' + cssVariables);
  }
  
  // Update body styles
  if (!html.includes('transition: background')) {
    html = html.replace(/color:\s*var\(--dl-gray-800\);/g, 'color: var(--dl-text);');
    html = html.replace(/background:\s*var\(--dl-gray-50\);/g, 'background: var(--dl-bg);\n      transition: background 0.3s ease, color 0.3s ease;');
    
    // Replace remaining gray variables
    html = html.replace(/var\(--dl-gray-800\)/g, 'var(--dl-text)');
    html = html.replace(/var\(--dl-gray-50\)/g, 'var(--dl-bg)');
    html = html.replace(/var\(--dl-white\)/g, 'var(--dl-surface)');
    html = html.replace(/var\(--dl-gray-200\)/g, 'var(--dl-border)');
    html = html.replace(/var\(--dl-gray-600\)/g, 'var(--dl-text-muted)');
    html = html.replace(/var\(--dl-gray-100\)/g, 'var(--dl-bg-alt)');
  }
  
  // Inject Toggle button in Header
  if (!html.includes('id="theme-toggle"')) {
    html = html.replace('<div class="header-actions">\\n        <a', toggleBtnHtml);
    html = html.replace('<div class="header-actions">\\r\\n        <a', toggleBtnHtml);
  }

  // Inject Script
  if (!html.includes('theme-toggle')) {
    html = html.replace('</body>', jsToggle);
  }
  
  fs.writeFileSync(page, html);
});
