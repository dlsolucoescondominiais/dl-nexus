export interface UsuarioPerfil {
  id: string;
  nome: string;
  cargo?: string;
  email: string;
  ativo: boolean;
  criado_em: string;
}

export interface Cliente {
  id: string;
  nome: string;
  cnpj_cpf?: string;
  telefone?: string;
  email?: string;
  criado_em: string;
}

export type TipoLocal = 'condominio' | 'empresa' | 'colegio' | 'restaurante' | 'lanchonete' | 'administradora' | 'outro';

export interface LocalAtendimento {
  id: string;
  cliente_id: string;
  tipo_local: TipoLocal;
  nome: string;
  cnpj_cpf?: string;
  endereco?: string;
  bairro?: string;
  cidade?: string;
  uf?: string;
  responsavel_nome?: string;
  responsavel_telefone?: string;
  responsavel_email?: string;
  criado_em: string;
}

export interface ServicoCatalogo {
  id: string;
  nome: string;
  descricao?: string;
  ativo: boolean;
  criado_em: string;
}

export type StatusAvaliacao = 'novo' | 'em_triagem' | 'agendada' | 'em_analise' | 'aguardando_cliente' | 'orcamento_em_preparo' | 'orcamento_enviado' | 'aprovado' | 'recusado' | 'cancelado';

export interface AvaliacaoTecnica {
  id: string;
  cliente_id?: string;
  local_id?: string;
  servico_id?: string;
  origem_lead?: string;
  canal_entrada?: string;
  status: StatusAvaliacao;
  prioridade: string;
  descricao_inicial?: string;
  observacoes_tecnicas?: string;
  url_pasta_drive?: string;
  data_agendada?: string;
  data_realizada?: string;
  responsavel_tecnico?: string;
  criado_em: string;
}

export interface Orcamento {
  id: string;
  avaliacao_tecnica_id?: string;
  cliente_id?: string;
  local_id?: string;
  codigo_orcamento?: string;
  titulo: string;
  status: string;
  validade_dias: number;
  prazo_execucao?: string;
  garantia?: string;
  observacoes_cliente?: string;
  observacoes_internas?: string;
  valor_material: number;
  valor_mao_obra: number;
  valor_deslocamento: number;
  valor_avaliacao_tecnica: number;
  valor_custos_indiretos: number;
  valor_impostos: number;
  margem_percentual: number;
  desconto_percentual: number;
  valor_total: number;
  forma_pagamento?: string;
  versao_cliente_html?: string;
  versao_interna_html?: string;
  pdf_url?: string;
  criado_em: string;
  atualizado_em: string;
}

export type TipoItemOrcamento = 'material' | 'mao_obra' | 'deslocamento' | 'avaliacao_tecnica' | 'imposto' | 'desconto' | 'custo_indireto' | 'equipamento' | 'servico';

export interface OrcamentoItem {
  id: string;
  orcamento_id: string;
  tipo_item: TipoItemOrcamento;
  categoria?: string;
  descricao: string;
  quantidade: number;
  unidade?: string;
  custo_unitario: number;
  preco_unitario: number;
  subtotal_custo: number;
  subtotal_venda: number;
  fornecedor?: string;
  observacao_interna?: string;
  visivel_cliente: boolean;
  criado_em: string;
}
