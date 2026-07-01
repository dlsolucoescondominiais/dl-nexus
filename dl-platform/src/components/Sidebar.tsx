"use client";

import Link from 'next/link';
import { Home, FileText, ClipboardList, Users, Settings } from 'lucide-react';

export default function Sidebar() {
  return (
    <aside className="w-64 bg-slate-900 text-slate-300 flex flex-col">
      <div className="h-16 flex items-center px-6 border-b border-slate-800">
        <h1 className="text-xl font-bold text-white tracking-tight">DL Platform</h1>
      </div>

      <nav className="flex-1 px-4 py-6 space-y-2">
        <Link href="/" className="flex items-center gap-3 px-3 py-2 rounded-md hover:bg-slate-800 hover:text-white transition-colors">
          <Home size={20} />
          <span>Início</span>
        </Link>

        <Link href="/avaliacoes-tecnicas/nova" className="flex items-center gap-3 px-3 py-2 rounded-md hover:bg-slate-800 hover:text-white transition-colors">
          <ClipboardList size={20} />
          <span>Avaliação Técnica</span>
        </Link>

        <Link href="/orcamentos" className="flex items-center gap-3 px-3 py-2 rounded-md hover:bg-slate-800 hover:text-white transition-colors">
          <FileText size={20} />
          <span>Orçamentos</span>
        </Link>

        <Link href="/clientes" className="flex items-center gap-3 px-3 py-2 rounded-md hover:bg-slate-800 hover:text-white transition-colors opacity-50 cursor-not-allowed" onClick={(e) => e.preventDefault()}>
          <Users size={20} />
          <span>Clientes (Em breve)</span>
        </Link>
      </nav>

      <div className="p-4 border-t border-slate-800">
        <button className="flex items-center gap-3 px-3 py-2 w-full text-left rounded-md hover:bg-slate-800 hover:text-white transition-colors opacity-50 cursor-not-allowed">
          <Settings size={20} />
          <span>Configurações</span>
        </button>
      </div>
    </aside>
  );
}
