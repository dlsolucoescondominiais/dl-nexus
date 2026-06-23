const fs = require('fs');
const { Client } = require('pg');

const sql = fs.readFileSync('add_dry_run.sql', 'utf8');

const client = new Client({
  host: 'db.nejdtvkpiclagsnfljsz.supabase.co',
  port: 5432,
  user: 'postgres',
  password: process.env.SUPABASE_DB_PASSWORD || 'your_db_password',
  database: 'postgres'
});

async function run() {
  try {
    await client.connect();
    console.log('Connected to DB');
    await client.query(sql);
    console.log('SQL executed successfully');
  } catch (err) {
    console.error('Error executing SQL:', err);
  } finally {
    await client.end();
  }
}

run();
