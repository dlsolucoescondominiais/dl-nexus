const fs = require('fs');
const indexHtml = fs.readFileSync('index.html', 'utf8');

// Use indexOf-based approach instead of regex (more reliable across Node versions)
const heroIdx = indexHtml.indexOf('<section class="hero"');
const footerIdx = indexHtml.indexOf('<footer class="footer"');

if (heroIdx === -1) {
  console.log('ERROR: <section class="hero"> not found!');
  process.exit(1);
}

const header = indexHtml.substring(0, heroIdx);
const footer = indexHtml.substring(footerIdx);

console.log('Header length:', header.length);
console.log('Footer length:', footer.length);
console.log('Header starts with:', header.substring(0, 50));
console.log('Header has charset:', header.includes('charset'));

// Write test page
const testPage = header + '\n<main><h1>Test</h1></main>\n' + footer;
fs.writeFileSync('_test_page.html', testPage, 'utf8');
console.log('Test page written. Check _test_page.html');
