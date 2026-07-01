import Link from 'next/link';

export default function Orcamentos() {
  return (
    <div className="max-w-6xl mx-auto">
      <header className="mb-8 flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">Orçamentos</h1>
          <p className="text-slate-500 mt-2">Gerencie as propostas comerciais</p>
        </div>
        <Link
          href="/orcamentos/novo"
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md font-medium transition-colors"
        >
          Novo Orçamento
        </Link>
      </header>

      <div className="bg-white rounded-xl shadow-sm border border-slate-100 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead className="bg-slate-50 text-slate-600 font-medium border-b border-slate-100">
              <tr>
                <th className="px-6 py-4">Código</th>
                <th className="px-6 py-4">Cliente / Local</th>
                <th className="px-6 py-4">Serviço</th>
                <th className="px-6 py-4">Status</th>
                <th className="px-6 py-4">Valor Total</th>
                <th className="px-6 py-4">Ações</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {/* Mock data for MVP */}
              <tr className="hover:bg-slate-50">
                <td className="px-6 py-4 font-medium text-slate-900">ORC-2023-001</td>
                <td className="px-6 py-4">
                  <p className="font-medium text-slate-900">Condomínio Alpha</p>
                  <p className="text-slate-500 text-xs">condominio</p>
                </td>
                <td className="px-6 py-4">DL Guardião</td>
                <td className="px-6 py-4">
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                    Em Preparo
                  </span>
                </td>
                <td className="px-6 py-4">R$ 12.500,00</td>
                <td className="px-6 py-4">
                  <button className="text-blue-600 hover:text-blue-800 font-medium">Editar</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
