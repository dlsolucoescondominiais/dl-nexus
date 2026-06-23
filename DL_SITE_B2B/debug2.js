const fs = require('fs');
const h = fs.readFileSync('index.html', 'utf8');

const m = h.match(/(<!DOCTYPE html>[\s\S]*?)<section class="hero"/);
if (m) {
  console.log('Header length:', m[1].length);
  console.log('First 100 chars:', m[1].substring(0, 100));
  console.log('Last 100 chars:', m[1].substring(m[1].length - 100));
} else {
  console.log('NO MATCH');
  // Try alternative
  const idx = h.indexOf('<section class="hero"');
  console.log('indexOf hero:', idx);
  console.log('Before hero:', h.substring(Math.max(0, idx-50), idx));
}
