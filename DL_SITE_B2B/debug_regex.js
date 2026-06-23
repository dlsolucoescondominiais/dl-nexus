const fs = require('fs');
const h = fs.readFileSync('index.html', 'utf8');
console.log('Has hero section:', h.includes('class="hero"'));
console.log('indexOf hero:', h.indexOf('class="hero"'));

// Test the regex
const m = h.match(/(<!DOCTYPE html>[\s\S]*?)<section class="hero"/);
console.log('Header regex match:', m ? 'YES (' + m[1].length + ' chars)' : 'NO');

const f = h.match(/(<footer class="footer"[\s\S]*?<\/html>)/);
console.log('Footer regex match:', f ? 'YES (' + f[1].length + ' chars)' : 'NO');
