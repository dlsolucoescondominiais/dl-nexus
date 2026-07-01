export default function NovoOrcamento() {
  return (
    <div className="max-w-6xl mx-auto">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900">Novo Orçamento</h1>
        <p className="text-slate-500 mt-2">Construa a proposta detalhada baseada na Avaliação Técnica</p>
      </header>

      <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-6 mb-8">
        <h2 className="text-lg font-semibold text-slate-900 mb-4 border-b pb-2">Selecione a Avaliação Técnica</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <select className="w-full border border-slate-300 rounded-md px-3 py-2">
            <option>Avaliação #102 - Condomínio Alpha (DL Guardião)</option>
          </select>
          <button className="bg-slate-100 text-slate-700 hover:bg-slate-200 px-4 py-2 rounded-md font-medium transition-colors">
            Importar Fotos e Escopo da Avaliação
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-6">
            <h2 className="text-lg font-semibold text-slate-900 mb-4 border-b pb-2 flex justify-between items-center">
              Composição de Custos
              <span className="text-sm font-normal text-slate-500 bg-slate-100 px-2 py-1 rounded">Visualização Interna</span>
            </h2>

            <div className="space-y-6">
               {/* Materiais */}
               <div>
                  <h3 className="text-md font-medium text-slate-800 mb-3 flex items-center gap-2">
                     <span className="w-2 h-2 bg-blue-500 rounded-full"></span> Materiais
                  </h3>
                  <div className="bg-slate-50 border border-slate-200 rounded-lg p-4 space-y-3">
                     <div className="grid grid-cols-12 gap-2 text-xs font-semibold text-slate-500 uppercase">
                        <div className="col-span-5">Descrição</div>
                        <div className="col-span-2 text-center">Qtd</div>
                        <div className="col-span-2 text-right">Custo Un.</div>
                        <div className="col-span-2 text-right">Subtotal</div>
                        <div className="col-span-1"></div>
                     </div>
                     <div className="grid grid-cols-12 gap-2 items-center bg-white border border-slate-200 p-2 rounded">
                        <input type="text" className="col-span-5 border-0 focus:ring-0 text-sm p-1" defaultValue="Infraestrutura elétrica (eletrocalhas)" />
                        <input type="number" className="col-span-2 border border-slate-200 rounded text-center text-sm p-1" defaultValue="1" />
                        <input type="text" className="col-span-2 border border-slate-200 rounded text-right text-sm p-1" defaultValue="52000.00" />
                        <div className="col-span-2 text-right text-sm font-medium">R$ 52.000</div>
                        <button className="col-span-1 text-red-500 text-center hover:text-red-700">x</button>
                     </div>
                     <button className="text-sm text-blue-600 font-medium hover:text-blue-800">+ Adicionar Material</button>
                  </div>
               </div>

               {/* Mão de Obra */}
               <div>
                  <h3 className="text-md font-medium text-slate-800 mb-3 flex items-center gap-2">
                     <span className="w-2 h-2 bg-indigo-500 rounded-full"></span> Mão de Obra
                  </h3>
                  <div className="bg-slate-50 border border-slate-200 rounded-lg p-4 space-y-3">
                     <div className="grid grid-cols-12 gap-2 items-center bg-white border border-slate-200 p-2 rounded">
                        <input type="text" className="col-span-5 border-0 focus:ring-0 text-sm p-1" defaultValue="Equipe Técnica (Gestão e Eletricistas)" />
                        <input type="number" className="col-span-2 border border-slate-200 rounded text-center text-sm p-1" defaultValue="1" />
                        <input type="text" className="col-span-2 border border-slate-200 rounded text-right text-sm p-1" defaultValue="96000.00" />
                        <div className="col-span-2 text-right text-sm font-medium">R$ 96.000</div>
                        <button className="col-span-1 text-red-500 text-center hover:text-red-700">x</button>
                     </div>
                     <button className="text-sm text-blue-600 font-medium hover:text-blue-800">+ Adicionar Mão de Obra</button>
                  </div>
               </div>

               {/* Custos Indiretos */}
               <div>
                  <h3 className="text-md font-medium text-slate-800 mb-3 flex items-center gap-2">
                     <span className="w-2 h-2 bg-amber-500 rounded-full"></span> Custos Indiretos (Logística, EPI, Seguros)
                  </h3>
                  <div className="bg-slate-50 border border-slate-200 rounded-lg p-4 space-y-3">
                     <div className="grid grid-cols-12 gap-2 items-center bg-white border border-slate-200 p-2 rounded">
                        <input type="text" className="col-span-5 border-0 focus:ring-0 text-sm p-1" defaultValue="Custos Operacionais" />
                        <input type="number" className="col-span-2 border border-slate-200 rounded text-center text-sm p-1" defaultValue="1" />
                        <input type="text" className="col-span-2 border border-slate-200 rounded text-right text-sm p-1" defaultValue="26500.00" />
                        <div className="col-span-2 text-right text-sm font-medium">R$ 26.500</div>
                        <button className="col-span-1 text-red-500 text-center hover:text-red-700">x</button>
                     </div>
                     <button className="text-sm text-blue-600 font-medium hover:text-blue-800">+ Adicionar Custo Indireto</button>
                  </div>
               </div>
            </div>
          </div>
        </div>

        <div className="lg:col-span-1">
          <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-6 sticky top-6">
            <h2 className="text-lg font-semibold text-slate-900 mb-4 border-b pb-2">BDI e Fechamento</h2>

            <div className="space-y-4 text-sm mb-6">
               <div className="bg-slate-50 p-3 rounded border border-slate-200">
                  <div className="flex justify-between items-center mb-2">
                     <span className="text-slate-700 font-medium">Custos Diretos e Indiretos</span>
                     <span className="font-bold text-slate-900">R$ 244.000</span>
                  </div>
               </div>

              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-slate-600">Margem de Lucro (%)</span>
                  <input type="number" className="w-20 border border-slate-300 rounded px-2 py-1 text-right font-medium text-emerald-600" defaultValue="24" />
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-slate-600">Impostos (%)</span>
                  <input type="number" className="w-20 border border-slate-300 rounded px-2 py-1 text-right" defaultValue="12" />
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-slate-600">Reserva de Garantia (%)</span>
                  <input type="number" className="w-20 border border-slate-300 rounded px-2 py-1 text-right" defaultValue="5" />
                </div>
              </div>

              <div className="bg-blue-50 border border-blue-100 p-4 rounded-lg mt-4 text-center">
                 <p className="text-xs text-blue-600 font-semibold uppercase mb-1">Preço Final Sugerido</p>
                 <p className="text-3xl font-bold text-blue-900">R$ 298.000</p>
                 <p className="text-xs text-blue-700 mt-2">BDI Total: R$ 54.000</p>
              </div>
            </div>

            <div className="space-y-3">
               <button type="button" className="w-full bg-slate-900 hover:bg-slate-800 text-white py-2.5 rounded-md font-medium transition-colors">
                  Gerar Proposta Cliente (PDF)
               </button>
               <button type="button" className="w-full bg-white border border-slate-300 text-slate-700 hover:bg-slate-50 py-2.5 rounded-md font-medium transition-colors">
                  Salvar Rascunho
               </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
