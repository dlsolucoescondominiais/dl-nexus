const fs = require('fs');

const indexHtml = fs.readFileSync('index.html', 'utf8');

const headerMatch = indexHtml.match(/(<!DOCTYPE html>[\s\S]*?)<section class="hero">/) || indexHtml.match(/(<!DOCTYPE html>[\s\S]*?)<main>/);
const header = headerMatch ? headerMatch[1] : '';

const footerMatch = indexHtml.match(/(<footer class="footer">[\s\S]*?<\/html>)/);
const footer = footerMatch ? footerMatch[1] : '';

const createPage = (filename, title, content) => {
  let pageHeader = header.replace(/<title>.*?<\/title>/, '<title>' + title + '</title>');
  
  const customStyles = `
    <style>
      .inner-heading {
        color: var(--dl-blue-dark);
      }
      [data-theme="dark"] .inner-heading {
        color: #f7f9fb;
      }
      .inner-content a {
        color: var(--dl-blue-light);
        text-decoration: underline;
      }
      [data-theme="dark"] .inner-content a {
        color: var(--dl-gold);
      }
    </style>
  `;
  
  pageHeader = pageHeader.replace('</head>', customStyles + '\n</head>');

  const fullPage = pageHeader + '\n<main class="inner-content" style="padding: 120px 20px 60px 20px; max-width: 1000px; margin: auto; min-height: 70vh;">\n' + content + '\n</main>\n' + footer;
  fs.writeFileSync(filename, fullPage, 'utf8');
};

const text = fs.readFileSync('user_texts.txt', 'utf8');

// The text contains lines from user_texts.txt. Let's filter out the XML tags
const paragraphs = text.split('\n')
  .filter(l => l.trim().length > 0 && !l.includes('<'))
  .map(l => `<p style="font-size: 1.1rem; line-height: 1.8; margin-bottom: 20px;">${l.trim()}</p>`)
  .join('\n');

const content = `<h1 class="inner-heading" style="font-size: 2.5rem; margin-bottom: 30px; font-weight: 700;">A Empresa & O Fundador</h1>\n` + paragraphs;

createPage('o-fundador.html', 'O Fundador | DL Soluções Condominiais', content);
createPage('quem-somos.html', 'Quem Somos | DL Soluções Condominiais', content);

console.log('Fixed Fundador and Quem Somos.');
