import { Request, Response } from 'express';
// Arquivo de fallback em TypeScript (para Deploy no Render/Vercel)
// Isso garantiria que a porta de entrada não dependesse só do n8n

export async function webhookHandler(req: Request, res: Response) {
  try {
    const payload = req.body;
    console.log("Meta API Webhook recebido diretamente:", payload);

    // Fallback: Se o n8n e o python estiverem fora, apenas confirmamos recebimento
    // para a Meta não enfileirar (ou guardamos em fila Redis/Supabase)

    // ... insert into supabase messages_whatsapp ...

    res.status(200).json({ status: 'ok', source: 'ts_fallback' });
  } catch (err) {
    console.error("Webhook Falhou:", err);
    res.status(500).json({ error: "Internal Server Error" });
  }
}
