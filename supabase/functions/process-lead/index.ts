import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const SUPABASE_URL = Deno.env.get('SUPABASE_URL') ?? ''
const SUPABASE_SERVICE_ROLE_KEY = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''
// Em produção, você deve colocar a chave da OpenAI nas variáveis de ambiente do Supabase Edge Functions
const OPENAI_API_KEY = Deno.env.get('OPENAI_API_KEY') ?? ''

// URL do novo Webhook do n8n para disparo de e-mail (Coloque o endereço real do seu n8n aqui)
// Exemplo: http://seu-ip:5678/webhook/lead-triado
const N8N_WEBHOOK_URL = Deno.env.get('N8N_WEBHOOK_URL') ?? 'http://SEU_IP_N8N:5678/webhook/lead-triado'

const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

const SYSTEM_PROMPT = `
Você é a Aninha e o Diego, agentes de inteligência artificial da DL Soluções Condominiais.
Sua missão é atuar como Triagem e Coordenação de Leads.
O foco principal da empresa é a conversão para contratos de receita recorrente através dos planos "DL Partner" (Basic, Master, Premium).

Estrutura de Roteamento de E-mails (DL Nexus):
Baseado na intenção do cliente, você deve classificar para qual e-mail este lead deve ser encaminhado:
- orcamento@dlsolucoescondominiais.com.br : Pedidos de orçamento, avaliação técnica para serviços, projetos novos (Máquina de Vendas).
- suporte@dlsolucoescondominiais.com.br : Dúvidas técnicas sobre obras em andamento, envio de plantas, chamados de emergência ou coordenação de visitas técnicas (Operação e Atendimento).
- sac@dlsolucoescondominiais.com.br : Gestão de garantias, dúvidas contratuais após obra concluída, atritos com administradoras (Pós-Venda).
- vagaconsultor@dlsolucoescondominiais.com.br : Envio de currículos, portfólios, eletricistas ou consultores buscando vagas (Recrutamento/RH).
- contato@dlsolucoescondominiais.com.br : Assuntos gerais ou não classificados.
- diogo@dlsolucoescondominiais.com.br : Assuntos de altíssimo nível, parcerias B2B estratégicas ou laudos técnicos.

Serviços e Portfólio de Implantação (CAPEX):
1. DL Guardião™ e Observer™: CFTV IP, Segurança Pública, Integração com 190.
2. Eixo DL Volt™: Retrofit de PC de Luz, Elétrica, Mobilidade (CVE/Carregadores).
3. DL EcoVolt Solar™: Energia Solar Híbrida e Backup.
4. DL Gatekeeper™: Automação de Portões via Smartphone.
5. DL Commander™: Automação e painéis elétricos para bombas.
6. Consultoria: DL Praxis Elétrica, DL Energia, DL Praxis, DL Sustentia.

Módulos DL Partner (OPEX / Recorrente):
Você DEVE SEMPRE sugerir o atrelamento de um plano DL Partner para garantir a gestão contínua, manutenção e SLA.

Regras de Triagem:
- Analise a mensagem do cliente (lead) e classifique em qual serviço primário se encaixa (se for um pedido de serviço).
- Determine o e-mail correto de encaminhamento (email_encaminhamento) seguindo as regras da Estrutura de Roteamento.
- Crie uma breve estratégia de abordagem recomendada focando no serviço principal E na introdução do DL Partner apropriado pelo tamanho do condomínio.
- Retorne apenas um JSON válido no seguinte formato exato (sem formatação markdown como \`\`\`json):
{
  "tipo_servico": "Nome do Serviço Primário (Ex: DL Volt / Recrutamento / Dúvida)",
  "estrategia_abordagem": "Estratégia detalhada...",
  "email_encaminhamento": "O email exato escolhido da lista acima"
}
`

serve(async (req) => {
  try {
    const payload = await req.json()
    // payload é o payload do webhook do database
    const lead = payload.record

    // Se o lead não for novo, ignora para não rodar em loop
    if (lead.status !== 'novo') {
        return new Response(JSON.stringify({ message: 'Lead already processed' }), { headers: { 'Content-Type': 'application/json' } })
    }

    if (!OPENAI_API_KEY) {
        console.error("OPENAI_API_KEY não configurada")
        return new Response(JSON.stringify({ error: "API Key não configurada" }), { status: 500 })
    }

    const mensagemLead = `O Lead ${lead.nome_contato} do condomínio ${lead.nome_condominio || 'Desconhecido'} (${lead.num_unidades || 'Tamanho não informado'} unidades) mandou a seguinte mensagem: "${lead.mensagem || lead.tipo_servico || 'Sem mensagem. Apenas entrou em contato.'}"`

    // Chama a OpenAI API para analisar o lead
    const aiResponse = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${OPENAI_API_KEY}`,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            model: 'gpt-4o', // Ou gpt-3.5-turbo, etc.
            messages: [
                { role: 'system', content: SYSTEM_PROMPT },
                { role: 'user', content: mensagemLead }
            ],
            temperature: 0.2
        })
    })

    if (!aiResponse.ok) {
        const err = await aiResponse.text()
        console.error("Erro na OpenAI", err)
        throw new Error("Erro ao chamar IA")
    }

    const aiData = await aiResponse.json()
    const content = aiData.choices[0].message.content

    let analise;
    try {
        analise = JSON.parse(content)
    } catch (e) {
        console.error("Erro ao fazer parse do JSON da IA:", content)
        analise = {
            tipo_servico: "Desconhecido",
            estrategia_abordagem: "A IA não conseguiu classificar corretamente: " + content,
            email_encaminhamento: "contato@dlsolucoescondominiais.com.br"
        }
    }

    const leadAtualizado = {
        ...lead,
        tipo_servico: analise.tipo_servico,
        mensagem: `[Triagem IA]:\nEstratégia: ${analise.estrategia_abordagem}\nEncaminhar para: ${analise.email_encaminhamento}\n\n[Mensagem Original]:\n${lead.mensagem}`,
        status: 'triado',
        email_encaminhamento: analise.email_encaminhamento
    }

    // Atualiza o lead no Supabase
    const { error: updateError } = await supabase
        .from('leads')
        .update({
            tipo_servico: leadAtualizado.tipo_servico,
            mensagem: leadAtualizado.mensagem,
            status: leadAtualizado.status,
            email_encaminhamento: leadAtualizado.email_encaminhamento
        })
        .eq('id', lead.id)

    if (updateError) {
        console.error("Erro ao atualizar lead:", updateError)
        throw updateError
    }

    // Após atualizar com sucesso, notifica o n8n para enviar o e-mail
    try {
        const n8nResponse = await fetch(N8N_WEBHOOK_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                event: 'lead_triado',
                lead: leadAtualizado
            })
        });

        if (!n8nResponse.ok) {
             console.error("Erro ao enviar webhook para o n8n:", await n8nResponse.text());
        } else {
             console.log("n8n notificado com sucesso!");
        }
    } catch(err) {
        console.error("Erro de conexão com o n8n:", err);
    }

    return new Response(
      JSON.stringify({ message: 'Lead triado com sucesso!', analise }),
      { headers: { "Content-Type": "application/json" } },
    )
  } catch (error) {
    console.error(error)
    return new Response(JSON.stringify({ error: error.message }), {
      headers: { "Content-Type": "application/json" },
      status: 400,
    })
  }
})
