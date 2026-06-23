const fs = require('fs');
const lines = fs.readFileSync('C:\\\\Users\\\\Diogo\\\\.gemini\\\\antigravity\\\\brain\\\\3b4ceb74-1036-4f32-9997-edd8f661952c\\\\.system_generated\\\\logs\\\\transcript.jsonl', 'utf8').split('\n');
const prefix = "html";
const delim = String.fromCharCode(96) + String.fromCharCode(96) + String.fromCharCode(96);
for (const line of lines) {
  if (!line) continue;
  try {
    const obj = JSON.parse(line);
    if (obj.content && obj.content.includes('Segue o index.html completo corrigido')) {
      const parts = obj.content.split(delim + prefix);
      if (parts.length > 1) {
        const codeBlock = parts[1].split(delim);
        const htmlCode = codeBlock[0].trim();
        fs.writeFileSync('index.html', htmlCode);
      }
    }
  } catch(e) {}
}
