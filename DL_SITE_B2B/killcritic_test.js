/**
 * KILLCRITIC Validation Suite — Fortress v1
 * Testa TODOS os arquivos HTML gerados contra as regras KILLCRITIC.
 */
const fs = require('fs');
const path = require('path');

const FILES = [
  'index.html',
  'a-empresa.html',
  'o-fundador.html',
  'politica-privacidade.html',
  'politica-cookies.html',
  'termos-de-uso.html',
  'lgpd-gdpr.html',
  'politica-atendimento.html',
  'portifolio.html',
  'quem-somos.html'
];

const FORBIDDEN_TERMS = [
  { term: 'Condfy', rule: 'KILLCRITIC #1: Uso do termo "Condfy" é PROIBIDO. Use "Fortress".' },
  { term: 'condfy', rule: 'KILLCRITIC #1: Uso do termo "condfy" é PROIBIDO. Use "Fortress".' },
  { term: 'visita técnica', rule: 'KILLCRITIC #2: Uso do termo "visita técnica" é PROIBIDO. Use "Avaliação Técnica".' },
  { term: 'Visita Técnica', rule: 'KILLCRITIC #2: Uso do termo "Visita Técnica" é PROIBIDO. Use "Avaliação Técnica".' },
  { term: 'visita tecnica', rule: 'KILLCRITIC #2: Uso do termo "visita tecnica" é PROIBIDO. Use "Avaliação Técnica".' },
];

// Phone numbers that should NOT appear visually
const FORBIDDEN_PHONES = [
  '21992698612',
  '21968907139',
  '21964742458',
  '992698612',
  '968907139',
  '964742458',
];

// Check for B2B in visible text (not in HTML comments or meta)
const B2B_REGEX = />([^<]*B2B[^<]*)</gi;

const REQUIRED_PATTERNS = [
  { pattern: 'n8n.dlsolucoescondominiais.com.br', desc: 'Webhook n8n routing' },
  { pattern: 'dataLayer', desc: 'DataLayer present (telemetry)' },
  { pattern: 'GTM-', desc: 'GTM placeholder present' },
  { pattern: 'PIXEL-', desc: 'Meta Pixel placeholder present' },
  { pattern: 'Avaliação Técnica', desc: 'CTA uses "Avaliação Técnica"' },
];

let totalErrors = 0;
let totalWarnings = 0;
let totalPassed = 0;

console.log('');
console.log('╔══════════════════════════════════════════════════════════╗');
console.log('║         KILLCRITIC VALIDATION SUITE — Fortress v1       ║');
console.log('╠══════════════════════════════════════════════════════════╣');
console.log('');

for (const file of FILES) {
  const filePath = path.join(__dirname, file);
  
  if (!fs.existsSync(filePath)) {
    console.log(`❌ ERRO: Arquivo ${file} não encontrado!`);
    totalErrors++;
    continue;
  }

  const content = fs.readFileSync(filePath, 'utf8');
  let fileErrors = 0;
  let filePassed = 0;

  console.log(`📄 Analisando: ${file}`);
  console.log('─'.repeat(50));

  // Test forbidden terms
  for (const { term, rule } of FORBIDDEN_TERMS) {
    if (content.includes(term)) {
      console.log(`   ❌ FALHA: ${rule}`);
      fileErrors++;
    } else {
      filePassed++;
    }
  }

  // Test forbidden phone numbers
  for (const phone of FORBIDDEN_PHONES) {
    if (content.includes(phone)) {
      console.log(`   ❌ FALHA: KILLCRITIC #5: Número de telefone ${phone} exposto no texto!`);
      fileErrors++;
    } else {
      filePassed++;
    }
  }

  // Test B2B in visible text (only on index.html and inner pages, not in meta/comments)
  const b2bMatches = content.match(B2B_REGEX);
  if (b2bMatches) {
    console.log(`   ❌ FALHA: KILLCRITIC #4: Termo "B2B" encontrado na interface visível: ${b2bMatches[0]}`);
    fileErrors++;
  } else {
    filePassed++;
  }

  // Required patterns (only check on index.html)
  if (file === 'index.html') {
    for (const { pattern, desc } of REQUIRED_PATTERNS) {
      if (content.includes(pattern)) {
        console.log(`   ✅ OK: ${desc}`);
        filePassed++;
      } else {
        console.log(`   ⚠️  AVISO: ${desc} — NÃO encontrado!`);
        totalWarnings++;
      }
    }

    // Check dark mode toggle exists
    if (content.includes('theme-toggle')) {
      console.log(`   ✅ OK: Toggle Dark/Light Mode presente`);
      filePassed++;
    } else {
      console.log(`   ❌ FALHA: Toggle Dark/Light Mode NÃO encontrado!`);
      fileErrors++;
    }

    // Check cookie banner exists
    if (content.includes('cookie-banner')) {
      console.log(`   ✅ OK: Banner de Cookies presente`);
      filePassed++;
    } else {
      console.log(`   ❌ FALHA: Banner de Cookies NÃO encontrado!`);
      fileErrors++;
    }

    // Check WhatsApp float exists
    if (content.includes('wa-float')) {
      console.log(`   ✅ OK: WhatsApp flutuante presente`);
      filePassed++;
    } else {
      console.log(`   ❌ FALHA: WhatsApp flutuante NÃO encontrado!`);
      fileErrors++;
    }

    // Check geo block
    if (content.includes('Atendemos todos os bairros')) {
      console.log(`   ✅ OK: Bloco SEO Geográfico presente`);
      filePassed++;
    } else {
      console.log(`   ⚠️  AVISO: Bloco SEO Geográfico não encontrado`);
      totalWarnings++;
    }

    // Check gastronomia
    if (content.includes('Mult') && content.includes('Grill')) {
      console.log(`   ✅ OK: Seção Gastronomia (Mult•Grill) presente`);
      filePassed++;
    } else {
      console.log(`   ⚠️  AVISO: Seção Gastronomia não encontrada`);
      totalWarnings++;
    }

    // Check hero H1
    if (content.includes('Soluções técnicas para condomínios em todos os bairros do Rio de Janeiro')) {
      console.log(`   ✅ OK: H1 correto no Hero`);
      filePassed++;
    } else {
      console.log(`   ❌ FALHA: H1 do Hero não corresponde ao texto especificado!`);
      fileErrors++;
    }

    // Check Meta CAPI
    if (content.includes('dlMetaCAPI')) {
      console.log(`   ✅ OK: Meta Conversions API (Server-Side) presente`);
      filePassed++;
    } else {
      console.log(`   ⚠️  AVISO: Meta Conversions API não encontrada`);
      totalWarnings++;
    }

    // Check scroll tracking
    if (content.includes('scroll_depth')) {
      console.log(`   ✅ OK: Scroll depth tracking presente`);
      filePassed++;
    } else {
      console.log(`   ⚠️  AVISO: Scroll depth tracking não encontrado`);
      totalWarnings++;
    }
  }

  // Check UTF-8 encoding
  if (content.includes('charset="UTF-8"') || content.includes("charset='UTF-8'") || content.includes('charset=UTF-8')) {
    filePassed++;
  } else {
    console.log(`   ⚠️  AVISO: charset UTF-8 não explícito`);
    totalWarnings++;
  }

  // Check footer present
  if (content.includes('<footer')) {
    filePassed++;
  } else {
    console.log(`   ❌ FALHA: Footer não encontrado em ${file}!`);
    fileErrors++;
  }

  totalErrors += fileErrors;
  totalPassed += filePassed;

  if (fileErrors === 0) {
    console.log(`   ✅ ${file}: TODAS AS REGRAS KILLCRITIC VALIDADAS`);
  }
  console.log('');
}

console.log('╠══════════════════════════════════════════════════════════╣');
console.log(`║  RESULTADO FINAL                                        ║`);
console.log(`║  ✅ Testes aprovados: ${String(totalPassed).padStart(3)}                                ║`);
console.log(`║  ⚠️  Avisos: ${String(totalWarnings).padStart(3)}                                       ║`);
console.log(`║  ❌ Erros: ${String(totalErrors).padStart(3)}                                         ║`);
console.log('╠══════════════════════════════════════════════════════════╣');

if (totalErrors === 0) {
  console.log('║  🏆 KILLCRITIC: APROVADO — Zero violações detectadas!   ║');
} else {
  console.log('║  🚨 KILLCRITIC: REPROVADO — Corrija os erros acima!     ║');
}

console.log('╚══════════════════════════════════════════════════════════╝');
console.log('');

process.exit(totalErrors > 0 ? 1 : 0);
