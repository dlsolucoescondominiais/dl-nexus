const fs = require('fs');
const logContent = fs.readFileSync('C:\\\\Users\\\\Diogo\\\\.gemini\\\\antigravity\\\\brain\\\\3b4ceb74-1036-4f32-9997-edd8f661952c\\\\.system_generated\\\\logs\\\\transcript.jsonl', 'utf8');
const lines = logContent.split('\n');

for (let i = lines.length - 1; i >= 0; i--) {
  if (lines[i].includes('<!DOCTYPE html>') && lines[i].includes('Falar com Comercial')) {
    try {
      const obj = JSON.parse(lines[i]);
      if (obj.tool_calls) {
        for (const call of obj.tool_calls) {
          if (call.name === 'write_to_file' && call.args && call.args.CodeContent) {
             const content = call.args.CodeContent;
             if (content.length > 20000) {
                 fs.writeFileSync('index.html', content);
                 console.log("Restored " + content.length + " bytes.");
                 process.exit(0);
             }
          }
        }
      }
    } catch(e) {}
  }
}
console.log("Not found.");
