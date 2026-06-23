const fs = require('fs');
let html = fs.readFileSync('old_index.txt', 'utf8');

// Inject CSS variables for Dark/Light mode
const cssVariables =     /* LIGHT MODE */
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
    };

html = html.replace(/:root\s*\{[^}]+\}/, :root {\n);

// Update colors to use the new variables
html = html.replace(/color:\s*var\(--dl-gray-800\);/g, 'color: var(--dl-text);');
html = html.replace(/background:\s*var\(--dl-gray-50\);/g, 'background: var(--dl-bg);');
html = html.replace(/background:\s*var\(--dl-white\);/g, 'background: var(--dl-surface);');
html = html.replace(/border: 1px solid var\(--dl-gray-200\);/g, 'border: 1px solid var(--dl-border);');
html = html.replace(/border-bottom: 1px solid var\(--dl-gray-200\);/g, 'border-bottom: 1px solid var(--dl-border);');
html = html.replace(/color:\s*var\(--dl-gray-600\);/g, 'color: var(--dl-text-muted);');
html = html.replace(/background: linear-gradient\(180deg, var\(--dl-gray-50\), var\(--dl-gray-100\)\);/g, 'background: linear-gradient(180deg, var(--dl-bg), var(--dl-bg-alt));');

// Inject the theme toggle button in header
const toggleBtn = <button class="theme-toggle" id="theme-toggle" aria-label="Alternar Tema" style="background:none;border:none;cursor:pointer;font-size:1.5rem;margin-right:15px;color:var(--dl-text);">??</button>;
html = html.replace('<div class="header-actions">', <div class="header-actions">\n        );

// Replace Meta card with Plantão Comercial Express
html = html.replace('<h3>Atendimento via Meta/Redes</h3>', '<h3>Plantão Comercial Express</h3>');
html = html.replace('<p>Canal dedicado a solicitações originadas em campanhas do Instagram ou Facebook.</p>', '<p>Canal imediato para novas solicitações e avaliação técnica expressa para o seu condomínio.</p>');
html = html.replace('Atendimento Meta', 'Solicitar Orçamento via WhatsApp');

// Insert WhatsApp SVGs into the three contact buttons
const waSvg = <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512" style="width:16px;height:16px;vertical-align:middle;margin-right:8px;fill:currentColor;"><path d="M380.9 97.1C339 55.1 283.2 32 223.9 32c-122.4 0-222 99.6-222 222 0 39.1 10.2 77.3 29.6 111L0 480l117.7-30.9c32.4 17.7 68.9 27 106.1 27h.1c122.3 0 224.1-99.6 224.1-222 0-59.3-25.2-115-67.1-157zM223.9 413.4c-33 0-65.5-8.9-94-25.7l-6.7-4-69.8 18.3L72 334.2l-4.4-7c-18.5-29.4-28.2-63.3-28.2-98.2 0-101.7 82.8-184.5 184.6-184.5 49.3 0 95.6 19.2 130.4 54.1 34.8 34.9 56.2 81.2 56.1 130.5 0 101.8-84.9 184.6-186.6 184.6zm101.2-138.2c-5.5-2.8-32.8-16.2-37.9-18-5.1-1.9-8.8-2.8-12.5 2.8-3.7 5.6-14.3 18-17.6 21.8-3.2 3.7-6.5 4.2-12 1.4-32.6-16.3-54-29.1-75.5-66-5.7-9.8 5.7-9.1 16.3-30.3 1.8-3.7.9-6.9-.5-9.7-1.4-2.8-12.5-30.1-17.1-41.2-4.5-10.8-9.1-9.3-12.5-9.5-3.2-.2-6.9-.2-10.6-.2-3.7 0-9.7 1.4-14.8 6.9-5.1 5.6-19.4 19-19.4 46.3 0 27.3 19.9 53.7 22.6 57.4 2.8 3.7 39.1 59.7 94.8 83.8 35.2 15.2 49 16.5 66.6 13.9 10.7-1.6 32.8-13.4 37.4-26.4 4.6-13 4.6-24.1 3.2-26.4-1.3-2.5-5-3.9-10.5-6.6z"/></svg>;
html = html.replace('Falar com o Suporte', \\ Falar com o Suporte\);
html = html.replace('Falar com Comercial', \\ Falar com Comercial\);
html = html.replace('Solicitar Orçamento via WhatsApp', \\ Solicitar Orçamento via WhatsApp\);
html = html.replace('Solicitar avaliação elétrica', \\ Solicitar avaliação elétrica\);

// Inject Dark/Light mode JS at the end of body
const js = \
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
\;
html = html.replace('</body>', \\</body>\);

fs.writeFileSync('index.html', html);
