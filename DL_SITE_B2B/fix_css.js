const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

// The original CSS for dark mode headings:
// .section-title { color: var(--dl-blue-dark); } -> we need them white in dark mode.
html = html.replace('</style>', `
  [data-theme="dark"] .hero h1,
  [data-theme="dark"] .hero p,
  [data-theme="dark"] .section-title,
  [data-theme="dark"] h1,
  [data-theme="dark"] h2,
  [data-theme="dark"] h3 {
    color: var(--dl-white) !important;
  }
</style>`);

fs.writeFileSync('index.html', html);
console.log('Fixed CSS.');
