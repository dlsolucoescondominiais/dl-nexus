const { Client } = require('pg');
require('dotenv').config();

async function checkTables() {
    const client = new Client({
        host: process.env.SUPABASE_DB_HOST,
        port: 5432,
        user: 'postgres',
        password: process.env.SUPABASE_DB_PASSWORD,
        database: 'postgres',
        ssl: { rejectUnauthorized: false }
    });

    try {
        console.log('[*] Conectando ao Supabase para verificar tabelas...');
        await client.connect();
        console.log('[+] Conexão bem-sucedida!');

        const res = await client.query(`
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        `);

        console.log('\n[+] Tabelas encontradas no schema "public":');
        res.rows.forEach(row => {
            console.log(` - ${row.table_name}`);
        });

    } catch (err) {
        console.error('[-] Erro ao verificar tabelas:', err);
    } finally {
        await client.end();
        console.log('[*] Conexão encerrada.');
    }
}

checkTables();
