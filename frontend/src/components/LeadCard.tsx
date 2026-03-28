import React from 'react';
import { Link } from 'react-router-dom';
import { Lead } from '../pages/Dashboard';

interface LeadCardProps {
  lead: Lead;
}

export function LeadCard({ lead }: LeadCardProps) {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'novo': return 'bg-blue-100 text-blue-800';
      case 'triado': return 'bg-purple-100 text-purple-800';
      case 'em_contato': return 'bg-yellow-100 text-yellow-800';
      case 'fechado': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
      <div className="flex justify-between items-start mb-4">
        <h3 className="font-manrope text-xl font-bold">{lead.nome_condominio || lead.nome_contato}</h3>
        <span className={`px-2 py-1 rounded-full text-xs font-semibold ${getStatusColor(lead.status)}`}>
          {lead.status.replace('_', ' ').toUpperCase()}
        </span>
      </div>
      <p className="text-sm text-gray-600 mb-2 font-inter">Contato: {lead.nome_contato}</p>
      <p className="text-sm text-gray-600 mb-4 font-inter">Serviço: {lead.tipo_servico || 'A definir'}</p>
      <div className="flex gap-2">
        <Link to={`/lead/${lead.id}`} className="flex-1 bg-gray-100 text-center py-2 rounded-md hover:bg-gray-200 text-sm font-medium transition-colors">
          Detalhes
        </Link>
        <Link to={`/checklist/${lead.id}`} className="flex-1 bg-blue-600 text-white text-center py-2 rounded-md hover:bg-blue-700 text-sm font-medium transition-colors">
          Checklist Técnico
        </Link>
      </div>
    </div>
  );
}
