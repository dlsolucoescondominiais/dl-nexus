const { Client } = require('pg');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

async function runMigration() {
    const client = new Client({
        host: process.env.SUPABASE_DB_HOST,
        port: 5432,
        user: 'postgres',
        password: process.env.SUPABASE_DB_PASSWORD,
        database: 'postgres',
        ssl: { rejectUnauthorized: false }
    });

    try {
        console.log('[*] Conectando ao Supabase (DB: postgres)...');
        await client.connect();
        console.log('[+] Conexão bem-sucedida!');

        const sqlPath = path.join(__dirname, 'backend', 'supabase', 'MIGRATIONS_DL_NEXUS_V7_SOCIAL.sql');
        console.log(`[*] Lendo arquivo de migração: ${sqlPath}`);
        const sql = fs.readFileSync(sqlPath, 'utf8');

        console.log('[*] Executando schema de Publicações Sociais (V7)...');
        await client.query(sql);
        console.log('[+] Schema de Publicações Sociais sincronizado com sucesso no Supabase!');
    } catch (err) {
        console.error('[-] Erro durante a migração:', err);
    } finally {
        await client.end();
        console.log('[*] Conexão encerrada.');
    }
}

runMigration();
