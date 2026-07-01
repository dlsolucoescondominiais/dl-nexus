import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  try {
    const data = await request.json();

    // Autenticação básica via Header (para o n8n enviar um token pre-shared)
    const authHeader = request.headers.get('authorization');
    const expectedToken = process.env.N8N_WEBHOOK_SECRET;

    if (!expectedToken) {
       console.error('CRITICAL: N8N_WEBHOOK_SECRET is not configured in environment.');
       return NextResponse.json({ error: 'Server configuration error' }, { status: 500 });
    }

    if (authHeader !== `Bearer ${expectedToken}`) {
      return NextResponse.json({ error: 'Não autorizado' }, { status: 401 });
    }

    // Estrutura esperada do n8n:
    // {
    //   "action": "criar_avaliacao_tecnica",
    //   "payload": {
    //     "cliente": { "nome": "...", "cnpj_cpf": "..." },
    //     "local": { "nome": "...", "tipo_local": "..." },
    //     "avaliacao": { "descricao_inicial": "..." }
    //   }
    // }

    const { action, payload } = data;

    if (!action || !payload) {
      return NextResponse.json({ error: 'Payload inválido' }, { status: 400 });
    }

    if (action === 'criar_avaliacao_tecnica') {
      // No futuro, isso inserirá no Supabase:
      // 1. Criar/Buscar Cliente
      // 2. Criar/Buscar Local
      // 3. Criar Avaliação Técnica

      console.log('Recebido webhook do n8n para criar avaliação técnica:', payload);

      return NextResponse.json({
        success: true,
        message: 'Avaliação técnica recebida com sucesso',
        // id_gerado: fakeId
      }, { status: 201 });
    }

    return NextResponse.json({ error: 'Ação não suportada' }, { status: 400 });

  } catch (error) {
    console.error('Erro no webhook:', error);
    return NextResponse.json({ error: 'Erro interno no servidor' }, { status: 500 });
  }
}
