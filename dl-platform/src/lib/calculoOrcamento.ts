import { OrcamentoItem } from '../types';

export interface ResumoCalculo {
  totalCustos: number;
  totalVendaItens: number;
  valorImpostos: number;
  valorMargem: number;
  valorTotal: number;
}

export function calcularResumoOrcamento(
  itens: OrcamentoItem[],
  margemPercentualBase: number = 30,
  impostoPercentualBase: number = 15
): ResumoCalculo {
  let totalCustos = 0;
  let totalVendaItens = 0;

  // Calcula os totais baseados nos itens
  itens.forEach((item) => {
    // Se o item é um desconto ou imposto tratado como item, ignora no custo base
    if (item.tipo_item === 'desconto' || item.tipo_item === 'imposto') {
      return;
    }

    // Subtotal custo = custo unitário * quantidade
    const subCusto = item.custo_unitario * item.quantidade;
    totalCustos += subCusto;

    // Subtotal venda = preço unitário * quantidade
    // Se preco_unitario for 0, podemos calcular baseado na margem,
    // mas aqui assumimos que os itens já tem o preço de venda definido
    // ou se não tiverem, a margem global os define depois.
    const subVenda = item.preco_unitario * item.quantidade;
    totalVendaItens += subVenda > 0 ? subVenda : subCusto;
  });

  // Se o total de venda for igual ao custo, aplicamos a margem global
  // Na prática, um orçamentista pode definir a margem global sobre o custo total

  // Cálculo básico:
  // Valor de Venda Sem Imposto = Custo / (1 - Margem%)
  // Cuidado: margem de 30% significa que o lucro é 30% da venda

  const margemDecimal = margemPercentualBase / 100;
  const impostoDecimal = impostoPercentualBase / 100;

  // Valor base de venda garantindo a margem sobre o custo
  // Ex: Custo 100, Margem 30% -> Venda 142.85 (Lucro 42.85 é 30% de 142.85)
  // Mas por simplicidade do MVP, vamos usar markup: Venda = Custo * (1 + Margem)
  const vendaBaseCalculada = totalCustos * (1 + margemDecimal);

  // Se os itens somados já dão um valor maior, usamos o valor dos itens
  let baseParaImposto = Math.max(vendaBaseCalculada, totalVendaItens);

  // Adiciona imposto por dentro (Gross-up)
  // Total = Base / (1 - Imposto)
  let valorTotal = baseParaImposto / (1 - impostoDecimal);

  let valorImpostos = valorTotal - baseParaImposto;
  let valorMargem = baseParaImposto - totalCustos;

  // Processar itens de desconto explícitos, se houver
  itens.forEach(item => {
    if (item.tipo_item === 'desconto') {
      valorTotal -= (item.preco_unitario * item.quantidade);
    }
  });

  return {
    totalCustos: Number(totalCustos.toFixed(2)),
    totalVendaItens: Number(totalVendaItens.toFixed(2)),
    valorImpostos: Number(valorImpostos.toFixed(2)),
    valorMargem: Number(valorMargem.toFixed(2)),
    valorTotal: Number(valorTotal.toFixed(2))
  };
}
