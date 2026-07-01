export default function Home() {
  return (
    <div className="max-w-6xl mx-auto">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900">Dashboard Executivo</h1>
        <p className="text-slate-500 mt-2">Visão geral do Projeto de Referência - DL Platform</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <div className="bg-white p-5 rounded-xl shadow-sm border border-slate-100 flex flex-col justify-between">
          <h3 className="text-sm font-medium text-slate-500 mb-1">Cliente / Projeto</h3>
          <p className="text-xl font-bold text-slate-900 truncate">Edifício Rony</p>
        </div>
        <div className="bg-white p-5 rounded-xl shadow-sm border border-slate-100 flex flex-col justify-between">
          <h3 className="text-sm font-medium text-slate-500 mb-1">Valor do Projeto</h3>
          <p className="text-xl font-bold text-blue-600">R$ 298.000,00</p>
        </div>
        <div className="bg-white p-5 rounded-xl shadow-sm border border-slate-100 flex flex-col justify-between">
          <h3 className="text-sm font-medium text-slate-500 mb-1">Margem Projetada</h3>
          <p className="text-xl font-bold text-emerald-600">24%</p>
          <span className="text-xs text-slate-400 mt-1">Lucro: R$ 71.520,00</span>
        </div>
        <div className="bg-white p-5 rounded-xl shadow-sm border border-slate-100 flex flex-col justify-between">
          <h3 className="text-sm font-medium text-slate-500 mb-1">Status</h3>
          <div className="flex items-center gap-2 mt-1">
            <span className="w-2.5 h-2.5 bg-yellow-400 rounded-full"></span>
            <p className="font-semibold text-slate-700">Em elaboração</p>
          </div>
          <span className="text-xs text-slate-400 mt-1">Probabilidade: 75%</span>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-6 mb-8">
         <h2 className="text-lg font-semibold text-slate-900 mb-4 border-b pb-2">Composição Financeira</h2>
         <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div className="space-y-4">
               <div>
                  <div className="flex justify-between text-sm mb-1">
                     <span className="font-medium text-slate-700">Materiais</span>
                     <span className="font-medium text-slate-900">R$ 121.500</span>
                  </div>
                  <div className="w-full bg-slate-100 rounded-full h-2">
                     <div className="bg-blue-500 h-2 rounded-full" style={{ width: '40%' }}></div>
                  </div>
               </div>
               <div>
                  <div className="flex justify-between text-sm mb-1">
                     <span className="font-medium text-slate-700">Mão de Obra</span>
                     <span className="font-medium text-slate-900">R$ 96.000</span>
                  </div>
                  <div className="w-full bg-slate-100 rounded-full h-2">
                     <div className="bg-indigo-500 h-2 rounded-full" style={{ width: '32%' }}></div>
                  </div>
               </div>
               <div>
                  <div className="flex justify-between text-sm mb-1">
                     <span className="font-medium text-slate-700">BDI (Impostos/Garantia/Lucro)</span>
                     <span className="font-medium text-slate-900">R$ 54.000</span>
                  </div>
                  <div className="w-full bg-slate-100 rounded-full h-2">
                     <div className="bg-emerald-500 h-2 rounded-full" style={{ width: '18%' }}></div>
                  </div>
               </div>
               <div>
                  <div className="flex justify-between text-sm mb-1">
                     <span className="font-medium text-slate-700">Custos Indiretos</span>
                     <span className="font-medium text-slate-900">R$ 26.500</span>
                  </div>
                  <div className="w-full bg-slate-100 rounded-full h-2">
                     <div className="bg-amber-500 h-2 rounded-full" style={{ width: '10%' }}></div>
                  </div>
               </div>
            </div>

            <div className="bg-slate-50 p-4 rounded-lg flex flex-col justify-center items-center text-center">
               <p className="text-sm text-slate-500 mb-2">Valor Final do Projeto</p>
               <p className="text-4xl font-bold text-slate-900 mb-2">R$ 298.000</p>
               <p className="text-xs text-slate-400">Execução: 12 meses | Manutenção: 36 meses</p>
            </div>
         </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl shadow-sm border border-slate-100 overflow-hidden">
          <div className="px-6 py-4 border-b border-slate-100">
            <h2 className="text-lg font-semibold text-slate-900">Oportunidades de Venda (IA)</h2>
          </div>
          <div className="p-6">
            <div className="bg-blue-50 border border-blue-100 text-blue-800 p-4 rounded-lg text-sm mb-4">
              <strong>Sugestão DL Intelligence:</strong> "Após análise técnica realizada pela equipe da DL, foram identificadas oportunidades de modernização da infraestrutura elétrica, reorganização dos sistemas de distribuição e preparação tecnológica..."
            </div>
            <button className="text-sm bg-blue-600 text-white px-4 py-2 rounded font-medium hover:bg-blue-700 w-full transition-colors">
               Gerar Proposta com IA
            </button>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-slate-100 overflow-hidden">
          <div className="px-6 py-4 border-b border-slate-100">
            <h2 className="text-lg font-semibold text-slate-900">Fotos & Diagnóstico</h2>
          </div>
          <div className="p-6">
            <div className="flex gap-4 mb-4 items-start">
               <div className="w-20 h-20 bg-slate-200 rounded object-cover flex-shrink-0 flex items-center justify-center text-slate-400 text-xs">Foto 32</div>
               <div className="text-sm space-y-1">
                  <p><span className="font-semibold text-red-600">Alto Risco:</span> Cabos expostos (NBR 5410).</p>
                  <p><span className="font-semibold">Solução:</span> Eletrocalha galvanizada 100x50.</p>
                  <p><span className="font-semibold text-slate-500">Custo est.:</span> R$ 2.840,00</p>
               </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
