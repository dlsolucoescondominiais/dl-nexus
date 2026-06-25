const fs = require('fs');
const path = require('path');

// 1. Carregar os payloads de teste
const payloadsDir = path.join(__dirname, 'DL_NEXUS_V3_LOCAL', '04_PAYLOADS_TESTE');
const files = [
    'PAYLOAD_EXEMPLO_CONDOMINIO_SOLAR_BACKUP.json',
    'PAYLOAD_EXEMPLO_RESIDENCIA_SOLAR_BACKUP.json',
    'PAYLOAD_EXEMPLO_LABORATORIO_SOLAR_BACKUP.json',
    'PAYLOAD_EXEMPLO_RESTAURANTE_SOLAR_BACKUP.json'
];

console.log('=== INICIANDO SIMULAÇÃO TÉCNICA LOCAL DOS WORKFLOWS (FASE 3) ===\n');

files.forEach(file => {
    const filePath = path.join(payloadsDir, file);
    if (!fs.existsSync(filePath)) {
        console.error(`[-] Arquivo não encontrado: ${file}`);
        return;
    }

    const payload = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    console.log(`[*] Processando cenário: "${payload.cliente.nome}" (${file})`);

    // --- WORKFLOW 202: CALCULAR CARGAS E SIMULTANEIDADE ---
    const cargas = payload.cargas_criticas || [];
    let potencia_total_w = 0;
    let potencia_simultanea_w = 0;
    let energia_diaria_wh = 0;
    let tem_motor_bloqueante = false;
    const pendencias_cargas = [];

    cargas.forEach(c => {
        const p = Number(c.potencia_w) || 0;
        const q = Number(c.quantidade) || 1;
        const h = Number(c.horas_uso_diario) || 0;
        const isSimultanea = c.simultanea !== false;
        const isMotor = !!c.motor;

        potencia_total_w += p * q;
        if (isSimultanea) {
            potencia_simultanea_w += p * q;
        }
        energia_diaria_wh += p * q * h;

        if (isMotor) {
            const p_partida = c.pico_partida || {};
            if (c.nome_carga.toLowerCase().includes('elevador')) {
                tem_motor_bloqueante = true;
                pendencias_cargas.push(`Elevador Social/Serviço '${c.nome_carga}' requer projeto de partida e análise de engenharia dedicada.`);
            } else if (!p_partida.tipo_partida || p_partida.tipo_partida === 'desconhecido' || !p_partida.corrente_partida_a) {
                tem_motor_bloqueante = true;
                pendencias_cargas.push(`Motor/Bomba '${c.nome_carga}' sem dados de pico de partida definidos.`);
            }
        }
    });

    const energia_critica_diaria_kwh = Number((energia_diaria_wh / 1000).toFixed(3));
    const potencia_critica_total_kw = Number((potencia_total_w / 1000).toFixed(3));
    const potencia_critica_simultanea_kw = Number((potencia_simultanea_w / 1000).toFixed(3));

    const dimensionamento_backup_calculado = {
        energia_critica_diaria_kwh,
        potencia_critica_total_kw,
        potencia_critica_simultanea_kw,
        tem_motor_bloqueante,
        pendencias_cargas
    };

    // --- WORKFLOW 203: DIMENSIONAR BANCO DE BATERIAS ---
    const dod = 0.80;
    const eficiencia = 0.85;
    const margem_tecnica = 0.25;

    const bateria_util_kwh = energia_critica_diaria_kwh;
    const bateria_nominal_kwh = Number((bateria_util_kwh / (dod * eficiencia) * (1 + margem_tecnica)).toFixed(3));
    const bateria_capacidade_descarga_kw = Number((bateria_nominal_kwh * 0.5).toFixed(3));
    const pendencias_baterias = [];

    if (bateria_capacidade_descarga_kw < potencia_critica_simultanea_kw) {
        pendencias_baterias.push(`A potência de descarga contínua do banco (${bateria_capacidade_descarga_kw} kW) é menor que a carga simultânea crítica (${potencia_critica_simultanea_kw} kW). Risco de sobrecarga.`);
    }

    dimensionamento_backup_calculado.bateria_util_kwh = bateria_util_kwh;
    dimensionamento_backup_calculado.bateria_nominal_kwh = bateria_nominal_kwh;
    dimensionamento_backup_calculado.bateria_capacidade_descarga_kw = bateria_capacidade_descarga_kw;
    dimensionamento_backup_calculado.paramentos_calculo = {
        dod_permitido: dod,
        eficiencia_sistema: eficiencia,
        margem_tecnica: margem_tecnica
    };
    dimensionamento_backup_calculado.pendencias_baterias = pendencias_baterias;

    // --- WORKFLOW 204: DIMENSIONAR INVERSOR HIBRIDO ---
    const potencia_inversor_minima_kw = Number((potencia_critica_simultanea_kw * (1 + margem_tecnica)).toFixed(3));
    let inversor_sugerido = 'Cascata/Múltiplos Inversores Híbridos (Requer Avaliação Técnica)';
    let compatibilidade_valida = true;
    const pendencias_inversor = [];
    const fase = payload.dados_eletricos.tipo_ligacao || 'trifasico';

    if (fase === 'monofasico' || fase === 'bifasico') {
        if (potencia_inversor_minima_kw <= 5.0) {
            inversor_sugerido = 'SolaX X1-Hybrid 5.0-D';
        } else {
            compatibilidade_valida = false;
            pendencias_inversor.push(`Potência de backup calculada (${potencia_inversor_minima_kw} kW) excede limite monofásico/bifásico padrão de 5 kW.`);
        }
    } else if (fase === 'trifasico') {
        if (potencia_inversor_minima_kw <= 10.0) {
            inversor_sugerido = 'SolaX X3-Hybrid 10.0-D';
        } else if (potencia_inversor_minima_kw <= 15.0) {
            inversor_sugerido = 'SolaX X3-Hybrid 15.0-D';
        } else {
            inversor_sugerido = 'Múltiplos Inversores SolaX X3 Híbridos em Cascata';
            pendencias_inversor.push(`Potência calculada (${potencia_inversor_minima_kw} kW) requer múltiplos inversores integrados em paralelo.`);
        }
    }

    dimensionamento_backup_calculado.potencia_inversor_minima_kw = potencia_inversor_minima_kw;
    dimensionamento_backup_calculado.inversor_sugerido = inversor_sugerido;
    dimensionamento_backup_calculado.compatibilidade_valida = compatibilidade_valida;
    dimensionamento_backup_calculado.pendencias_inversor = pendencias_inversor;

    // --- WORKFLOW 205: CALCULAR ARRANJO FOTOVOLTAICO ---
    const consumo = payload.dados_conta.consumo_mensal_kwh || 0;
    const geracao_mensal_estimada_por_kwp = 115;
    const sistema_solar_kwp_preliminar = Number((consumo / geracao_mensal_estimada_por_kwp).toFixed(2));
    const geracao_mensal_estimada_kwh = Math.round(sistema_solar_kwp_preliminar * geracao_mensal_estimada_por_kwp);

    const dimensionamento_solar_calculado = {
        sistema_solar_kwp_preliminar,
        geracao_mensal_estimada_kwh,
        irradiacao_regiao_kwh_m2_dia: 4.86
    };

    // --- WORKFLOW 207: AUDITAR REGRAS KILLCRITIC ---
    const motivos_bloqueio = [];
    const pendencias_criticas = [];
    let status_killcritic = 'APROVADO';
    let risco_killcritic = 'baixo';

    // LEVEL 1: VALIDATION
    if (!payload.protocolo || !/^ECO-[0-9]{8}-[0-9]{4}$/.test(payload.protocolo)) {
        motivos_bloqueio.push('Protocolo inválido ou fora do padrão (ECO-YYYYMMDD-XXXX).');
    }
    if (!payload.cliente.nome || !payload.cliente.tipo_cliente || !payload.cliente.responsavel || !payload.cliente.whatsapp || !payload.cliente.email) {
        motivos_bloqueio.push('Dados cadastrais de cliente incompletos.');
    }
    if (!payload.dados_eletricos.tensao || !payload.dados_eletricos.tipo_ligacao || !payload.dados_eletricos.disjuntor_geral || !payload.dados_eletricos.padrao_entrada) {
        motivos_bloqueio.push('Dados elétricos básicos incompletos.');
    }
    if (!payload.dados_conta.consumo_mensal_kwh || !payload.dados_conta.valor_medio_conta || !payload.dados_conta.concessionaria) {
        motivos_bloqueio.push('Dados da conta de energia incompletos.');
    }

    // LEVEL 2: MATH & TECHNICAL LOGIC
    if (dimensionamento_backup_calculado.tem_motor_bloqueante) {
        status_killcritic = 'BLOQUEADO';
        risco_killcritic = 'alto';
        (dimensionamento_backup_calculado.pendencias_cargas || []).forEach(p => motivos_bloqueio.push(p));
    }

    cargas.forEach(c => {
        const nome = c.nome_carga.toLowerCase();
        if (nome.includes('elevador') || nome.includes('incendio') || nome.includes('recalque') || nome.includes('ar condicionado central')) {
            status_killcritic = 'BLOQUEADO';
            risco_killcritic = 'alto';
            motivos_bloqueio.push(`Carga de alta potência/indução '${c.nome_carga}' incluída. Não é permitido sem projeto dedicado.`);
        }
        if (payload.cliente.tipo_cliente === 'restaurante') {
            if (nome.includes('fritadeira') || nome.includes('chapa') || nome.includes('forno') || nome.includes('resistencia')) {
                status_killcritic = 'BLOQUEADO';
                risco_killcritic = 'alto';
                motivos_bloqueio.push(`Carga térmica de cozinha comercial '${c.nome_carga}' incluída no backup preliminar.`);
            }
        }
    });

    if (bateria_nominal_kwh <= 0) {
        motivos_bloqueio.push('Capacidade nominal do banco de baterias calculado é zero.');
    }

    // LEVEL 3: CONSOLIDATION
    if (motivos_bloqueio.length > 0) {
        status_killcritic = 'BLOQUEADO';
        risco_killcritic = 'alto';
        pendencias_criticas.push('Necessário agendar Avaliação Técnica presencial para sanar bloqueios de engenharia.');
    } else {
        status_killcritic = 'APROVADO_COM_RESSALVAS';
        risco_killcritic = 'medio';
        pendencias_criticas.push('Confirmar local físico de instalação e ventilação adequada do inversor e baterias.');
        pendencias_criticas.push('Validar custos reais de importação de equipamentos com a Corsolar.');
    }

    const status_orcamento = (status_killcritic === 'BLOQUEADO') ? 'bloqueado_killcritic' : 'aprovado_para_proposta';

    // Exibir resultados
    console.log(`  > Energia Crítica Diária: ${energia_critica_diaria_kwh} kWh/dia`);
    console.log(`  > Bateria Nominal Mínima: ${bateria_nominal_kwh} kWh`);
    console.log(`  > Potência Simultânea: ${potencia_critica_simultanea_kw} kW`);
    console.log(`  > Potência Inversor Mínima: ${potencia_inversor_minima_kw} kW`);
    console.log(`  > Inversor Sugerido: ${inversor_sugerido}`);
    console.log(`  > Solar Preliminar: ${sistema_solar_kwp_preliminar} kWp`);
    console.log(`  > Status KILLCRITIC: ${status_killcritic} (Risco: ${risco_killcritic})`);
    console.log(`  > Status Orçamento: ${status_orcamento}`);
    if (motivos_bloqueio.length > 0) {
        console.log(`  > Motivos de Bloqueio:`);
        motivos_bloqueio.forEach(m => console.log(`    - ${m}`));
    }
    console.log(`  > Pendências Críticas:`);
    pendencias_criticas.forEach(p => console.log(`    - ${p}`));
    console.log('\n--------------------------------------------------\n');
});

console.log('[+] Simulação finalizada.');
