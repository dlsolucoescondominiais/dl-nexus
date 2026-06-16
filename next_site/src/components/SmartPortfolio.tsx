"use client";

import React, { useState, useEffect } from 'react';
import { supabase } from '@/lib/supabase';
import { MapPin, CheckCircle, XCircle } from 'lucide-react';

interface Project {
  id: string;
  title: string;
  region: string;
  type: string;
  before_desc: string;
  after_desc: string;
  image_url?: string;
}

const mockProjects: Project[] = [
  {
    id: '1',
    title: 'Retrofit Elétrico Condomínio Master',
    region: 'Zona Sul',
    type: 'Elétrica',
    before_desc: 'Fiação subdimensionada e uso de canaletas plásticas aparentes, com risco de incêndio.',
    after_desc: 'Infraestrutura em eletrodutos galvanizados, quadros certificados e cabeamento antichama.'
  },
  {
    id: '2',
    title: 'Usina Solar Industrial 50kWp',
    region: 'Zona Oeste',
    type: 'Solar',
    before_desc: 'Custo energético elevado (R$ 8.000/mês) e telhado subutilizado.',
    after_desc: 'Instalação de painéis monocristalinos com redução de 92% na fatura mensal.'
  },
  {
    id: '3',
    title: 'Automação e CFTV IP',
    region: 'Zona Norte',
    type: 'Segurança',
    before_desc: 'Câmeras analógicas com baixa resolução e pontos cegos na portaria.',
    after_desc: 'Sistema IP Full HD, reconhecimento facial e no-break para 12h de autonomia.'
  },
  {
    id: '4',
    title: 'Adequação PC de Luz (Light)',
    region: 'Sudoeste',
    type: 'Elétrica',
    before_desc: 'Centro de medição em madeira, corroído e fora do padrão atual da concessionária.',
    after_desc: 'Novo PC em caixas de policarbonato com barramento de cobre e DPS instalado.'
  }
];

const regions = ['Todas', 'Zona Sul', 'Zona Oeste', 'Zona Norte', 'Sudoeste'];
const types = ['Todos', 'Elétrica', 'Solar', 'Segurança'];

export default function SmartPortfolio() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeRegion, setActiveRegion] = useState('Todas');
  const [activeType, setActiveType] = useState('Todos');

  useEffect(() => {
    async function fetchProjects() {
      try {
        const { data, error } = await supabase.from('portfolio_projects').select('*');
        if (error || !data || data.length === 0) {
          throw new Error('Fallback to mock');
        }
        setProjects(data);
      } catch {
        setProjects(mockProjects);
      } finally {
        setLoading(false);
      }
    }
    fetchProjects();
  }, []);

  const filteredProjects = projects.filter(p => {
    const matchRegion = activeRegion === 'Todas' || p.region === activeRegion;
    const matchType = activeType === 'Todos' || p.type === activeType;
    return matchRegion && matchType;
  });

  return (
    <section className="py-24 bg-slate-950" id="portfolio">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 max-w-7xl">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-5xl font-bold text-white mb-6 tracking-tight">
            Casos Reais. <span className="text-amber-500">Resultados Medíveis.</span>
          </h2>
          <p className="text-lg text-slate-400 max-w-2xl mx-auto">
            Explore projetos de engenharia executados com rigor técnico no Rio de Janeiro. De retrofits elétricos a usinas solares de alta performance.
          </p>
        </div>

        {/* Filters */}
        <div className="flex flex-col md:flex-row gap-6 mb-12 justify-center">
          <div className="flex flex-wrap gap-2 justify-center">
            {regions.map(r => (
              <button
                key={r}
                onClick={() => setActiveRegion(r)}
                className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
                  activeRegion === r
                    ? 'bg-amber-500 text-slate-900'
                    : 'bg-slate-900 text-slate-300 hover:bg-slate-800'
                }`}
              >
                {r}
              </button>
            ))}
          </div>
          <div className="w-px bg-slate-800 hidden md:block"></div>
          <div className="flex flex-wrap gap-2 justify-center">
            {types.map(t => (
              <button
                key={t}
                onClick={() => setActiveType(t)}
                className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
                  activeType === t
                    ? 'bg-slate-700 text-white'
                    : 'bg-slate-900 text-slate-300 hover:bg-slate-800'
                }`}
              >
                {t}
              </button>
            ))}
          </div>
        </div>

        {/* Grid */}
        {loading ? (
          <div className="flex justify-center py-20">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-amber-500"></div>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {filteredProjects.map(project => (
              <div key={project.id} className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden group hover:border-slate-600 transition-colors">
                <div className="p-6 md:p-8">
                  <div className="flex justify-between items-start mb-6">
                    <div>
                      <h3 className="text-xl font-bold text-white mb-2">{project.title}</h3>
                      <div className="flex items-center gap-2 text-sm text-slate-400">
                        <MapPin size={14} className="text-amber-500" />
                        <span>{project.region}</span>
                        <span className="w-1 h-1 rounded-full bg-slate-700"></span>
                        <span className="px-2 py-0.5 rounded text-xs bg-slate-800 border border-slate-700">{project.type}</span>
                      </div>
                    </div>
                  </div>

                  <div className="space-y-4">
                    {/* Before */}
                    <div className="flex gap-4 p-4 rounded-xl bg-red-950/20 border border-red-900/30">
                      <div className="mt-1">
                        <XCircle size={20} className="text-red-500" />
                      </div>
                      <div>
                        <p className="text-xs font-bold uppercase text-red-500/80 tracking-wider mb-1">Cenário Anterior (Risco)</p>
                        <p className="text-sm text-slate-300">{project.before_desc}</p>
                      </div>
                    </div>

                    {/* After */}
                    <div className="flex gap-4 p-4 rounded-xl bg-emerald-950/20 border border-emerald-900/30">
                      <div className="mt-1">
                        <CheckCircle size={20} className="text-emerald-500" />
                      </div>
                      <div>
                        <p className="text-xs font-bold uppercase text-emerald-500/80 tracking-wider mb-1">Solução DL (Padrão Industrial)</p>
                        <p className="text-sm text-slate-300">{project.after_desc}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}

            {filteredProjects.length === 0 && (
              <div className="col-span-full py-12 text-center text-slate-500">
                Nenhum projeto encontrado para os filtros selecionados.
              </div>
            )}
          </div>
        )}
      </div>
    </section>
  );
}
