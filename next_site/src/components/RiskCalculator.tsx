"use client";

import React, { useState } from 'react';
import { Zap, AlertTriangle, ShieldCheck, Sun } from 'lucide-react';

export default function RiskCalculator() {
  const [activeTab, setActiveTab] = useState<'solar' | 'eletrica'>('solar');

  // Solar state
  const [billValue, setBillValue] = useState<number | ''>('');

  // Eletrica state
  const [q1, setQ1] = useState<boolean | null>(null);
  const [q2, setQ2] = useState<boolean | null>(null);
  const [q3, setQ3] = useState<boolean | null>(null);

  const calculateSolarSavings = (monthlyBill: number) => {
    // Basic rough estimate: 90% savings over 20 years, ignoring inflation for simplicity here
    // or add a 5% inflation YoY. Let's do a simple one:
    const yearly = monthlyBill * 12;
    const savingsPercentage = 0.90;
    const total20Years = yearly * 20 * savingsPercentage;
    return total20Years;
  };

  const hasRisk = q1 === true || q2 === true || q3 === true;
  const isComplete = q1 !== null && q2 !== null && q3 !== null;

  return (
    <section className="py-20 bg-slate-900 border-y border-slate-800" id="calculadora">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 max-w-4xl">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
            Análise de Viabilidade & Risco
          </h2>
          <p className="text-slate-400 max-w-2xl mx-auto">
            Descubra o potencial de economia com energia solar ou avalie os riscos estruturais da sua rede elétrica atual.
          </p>
        </div>

        <div className="bg-slate-950 rounded-2xl border border-slate-800 overflow-hidden shadow-2xl">
          {/* Tabs */}
          <div className="flex border-b border-slate-800">
            <button
              onClick={() => setActiveTab('solar')}
              className={`flex-1 py-4 px-6 flex items-center justify-center gap-2 text-sm font-semibold transition-colors ${
                activeTab === 'solar'
                  ? 'bg-slate-900 text-amber-500 border-b-2 border-amber-500'
                  : 'text-slate-400 hover:text-slate-300 hover:bg-slate-900/50'
              }`}
            >
              <Sun size={18} />
              Simulador Solar
            </button>
            <button
              onClick={() => setActiveTab('eletrica')}
              className={`flex-1 py-4 px-6 flex items-center justify-center gap-2 text-sm font-semibold transition-colors ${
                activeTab === 'eletrica'
                  ? 'bg-slate-900 text-red-500 border-b-2 border-red-500'
                  : 'text-slate-400 hover:text-slate-300 hover:bg-slate-900/50'
              }`}
            >
              <AlertTriangle size={18} />
              Risco Elétrico
            </button>
          </div>

          <div className="p-6 md:p-8">
            {activeTab === 'solar' && (
              <div className="space-y-6 animate-in fade-in duration-300">
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">
                    Valor médio da conta de luz (R$)
                  </label>
                  <div className="relative">
                    <span className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500">R$</span>
                    <input
                      type="number"
                      value={billValue}
                      onChange={(e) => setBillValue(e.target.value ? Number(e.target.value) : '')}
                      placeholder="Ex: 2500"
                      className="w-full bg-slate-900 border border-slate-700 rounded-lg py-3 pl-12 pr-4 text-white placeholder-slate-600 focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500 transition-colors"
                    />
                  </div>
                </div>

                {billValue && billValue > 0 && (
                  <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
                    <div className="flex items-center gap-4 mb-2">
                      <div className="p-3 bg-amber-500/10 rounded-lg">
                        <Zap className="text-amber-500" size={24} />
                      </div>
                      <div>
                        <p className="text-sm text-slate-400">Economia estimada em 20 anos</p>
                        <p className="text-3xl font-bold text-amber-500">
                          {new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(calculateSolarSavings(Number(billValue)))}
                        </p>
                      </div>
                    </div>
                    <p className="text-xs text-slate-500 mt-4">
                      *Cálculo referencial considerando economia de 90% na tarifa de energia, sem considerar inflação ou custos de manutenção.
                    </p>
                  </div>
                )}
              </div>
            )}

            {activeTab === 'eletrica' && (
              <div className="space-y-6 animate-in fade-in duration-300">
                <div className="space-y-4">
                  <div className="flex items-start justify-between p-4 bg-slate-900 rounded-lg border border-slate-800">
                    <span className="text-slate-300">A fiação principal do condomínio tem mais de 15 anos?</span>
                    <div className="flex gap-2 ml-4">
                      <button onClick={() => setQ1(true)} className={`px-4 py-1 rounded text-sm font-medium transition-colors ${q1 === true ? 'bg-red-500/20 text-red-500 border border-red-500/50' : 'bg-slate-800 text-slate-400 hover:bg-slate-700'}`}>Sim</button>
                      <button onClick={() => setQ1(false)} className={`px-4 py-1 rounded text-sm font-medium transition-colors ${q1 === false ? 'bg-emerald-500/20 text-emerald-500 border border-emerald-500/50' : 'bg-slate-800 text-slate-400 hover:bg-slate-700'}`}>Não</button>
                    </div>
                  </div>

                  <div className="flex items-start justify-between p-4 bg-slate-900 rounded-lg border border-slate-800">
                    <span className="text-slate-300">Existem fios expostos ou uso de canaletas plásticas em áreas comuns?</span>
                    <div className="flex gap-2 ml-4">
                      <button onClick={() => setQ2(true)} className={`px-4 py-1 rounded text-sm font-medium transition-colors ${q2 === true ? 'bg-red-500/20 text-red-500 border border-red-500/50' : 'bg-slate-800 text-slate-400 hover:bg-slate-700'}`}>Sim</button>
                      <button onClick={() => setQ2(false)} className={`px-4 py-1 rounded text-sm font-medium transition-colors ${q2 === false ? 'bg-emerald-500/20 text-emerald-500 border border-emerald-500/50' : 'bg-slate-800 text-slate-400 hover:bg-slate-700'}`}>Não</button>
                    </div>
                  </div>

                  <div className="flex items-start justify-between p-4 bg-slate-900 rounded-lg border border-slate-800">
                    <span className="text-slate-300">Ocorrem quedas de disjuntor frequentes ou superaquecimento no quadro?</span>
                    <div className="flex gap-2 ml-4">
                      <button onClick={() => setQ3(true)} className={`px-4 py-1 rounded text-sm font-medium transition-colors ${q3 === true ? 'bg-red-500/20 text-red-500 border border-red-500/50' : 'bg-slate-800 text-slate-400 hover:bg-slate-700'}`}>Sim</button>
                      <button onClick={() => setQ3(false)} className={`px-4 py-1 rounded text-sm font-medium transition-colors ${q3 === false ? 'bg-emerald-500/20 text-emerald-500 border border-emerald-500/50' : 'bg-slate-800 text-slate-400 hover:bg-slate-700'}`}>Não</button>
                    </div>
                  </div>
                </div>

                {isComplete && (
                  <div className="mt-6 animate-in slide-in-from-bottom-4 duration-500">
                    {hasRisk ? (
                      <div className="bg-red-950/40 border border-red-900 rounded-xl p-6 text-center">
                        <AlertTriangle className="mx-auto text-red-500 mb-3" size={32} />
                        <h4 className="text-lg font-bold text-red-500 mb-2">ALTO RISCO DE INCÊNDIO / FALHA</h4>
                        <p className="text-red-200/70 text-sm mb-6 max-w-md mx-auto">
                          As condições indicam uma infraestrutura fora das normas NBR 5410. Recomendamos intervenção imediata para proteger os condôminos e o patrimônio.
                        </p>
                        <a
                          href="https://wa.me/5521999999999?text=Fiz o teste de risco e preciso de uma Avaliação Técnica urgente."
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-flex items-center justify-center px-6 py-3 text-sm font-bold text-white bg-red-600 hover:bg-red-500 rounded-lg transition-colors"
                        >
                          Solicitar Avaliação Técnica Urgente
                        </a>
                      </div>
                    ) : (
                      <div className="bg-emerald-950/40 border border-emerald-900 rounded-xl p-6 text-center">
                        <ShieldCheck className="mx-auto text-emerald-500 mb-3" size={32} />
                        <h4 className="text-lg font-bold text-emerald-500 mb-2">Infraestrutura Aparentemente Segura</h4>
                        <p className="text-emerald-200/70 text-sm mb-6 max-w-md mx-auto">
                          Pelas suas respostas, não identificamos sinais críticos imediatos. Continue com as manutenções preventivas anuais.
                        </p>
                        <a
                          href="https://wa.me/5521999999999?text=Gostaria de agendar uma Avaliação Técnica preventiva."
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-flex items-center justify-center px-6 py-3 text-sm font-bold text-emerald-950 bg-emerald-500 hover:bg-emerald-400 rounded-lg transition-colors"
                        >
                          Agendar Avaliação Técnica Preventiva
                        </a>
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
