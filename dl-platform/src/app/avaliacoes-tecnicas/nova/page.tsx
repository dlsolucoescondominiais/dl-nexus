export default function NovaAvaliacaoTecnica() {
  return (
    <div className="max-w-4xl mx-auto">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900">Nova Avaliação Técnica</h1>
        <p className="text-slate-500 mt-2">Registre uma nova solicitação de atendimento</p>
      </header>

      <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-6">
        <form className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Cliente</label>
              <select className="w-full border border-slate-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
                <option value="">Selecione ou crie um cliente...</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Local de Atendimento</label>
              <select className="w-full border border-slate-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
                <option value="">Selecione um local...</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Serviço de Interesse</label>
              <select className="w-full border border-slate-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
                <option value="">Selecione o serviço...</option>
                <option value="DL Guardião">DL Guardião - CFTV</option>
                <option value="DL Fortress">DL Fortress - Controle de Acesso</option>
                <option value="DL Acqua">DL Acqua - Automação de Bombas</option>
                <option value="Gatekeeper">Gatekeeper - Portões</option>
                <option value="DL Volt">DL Volt - Elétrica</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Origem do Lead</label>
              <select className="w-full border border-slate-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
                <option value="site">Site DL</option>
                <option value="whatsapp">WhatsApp</option>
                <option value="indicacao">Indicação</option>
                <option value="outros">Outros</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Descrição Inicial (Motivo do contato)</label>
            <textarea
              rows={4}
              className="w-full border border-slate-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Descreva o que o cliente solicitou..."
            ></textarea>
          </div>

          <div className="pt-4 border-t border-slate-100 flex justify-end gap-3">
            <button type="button" className="px-4 py-2 text-slate-600 hover:bg-slate-50 rounded-md font-medium transition-colors">
              Cancelar
            </button>
            <button type="button" className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md font-medium transition-colors">
              Salvar Avaliação
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
