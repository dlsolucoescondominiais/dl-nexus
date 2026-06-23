const fs = require('fs');

const extract = (file) => {
  const html = fs.readFileSync(file, 'utf8');
  const start = html.indexOf('<div class="entry-content');
  if (start === -1) return 'NOT FOUND';
  let content = html.substring(start);
  const end = content.indexOf('</div><!-- .entry-content -->');
  if (end !== -1) {
    content = content.substring(0, end);
  }
  return content.replace(/<[^>]+>/g, '\n').replace(/&nbsp;/g, ' ').replace(/\n+/g, '\n\n');
};

const f1 = extract('C:/Users/Diogo/.gemini/antigravity/brain/3b4ceb74-1036-4f32-9997-edd8f661952c/.system_generated/steps/385/content.md');
const f2 = extract('C:/Users/Diogo/.gemini/antigravity/brain/3b4ceb74-1036-4f32-9997-edd8f661952c/.system_generated/steps/386/content.md');
const f3 = extract('C:/Users/Diogo/.gemini/antigravity/brain/3b4ceb74-1036-4f32-9997-edd8f661952c/.system_generated/steps/387/content.md');

fs.writeFileSync('D:/AntiGravity/projeto_01/DL_SITE_B2B/content_fundador.txt', f1, 'utf8');
fs.writeFileSync('D:/AntiGravity/projeto_01/DL_SITE_B2B/content_lgpd.txt', f2, 'utf8');
fs.writeFileSync('D:/AntiGravity/projeto_01/DL_SITE_B2B/content_politica.txt', f3, 'utf8');

console.log('Saved texts.');
