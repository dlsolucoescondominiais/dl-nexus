import React from 'react';
import { ShieldAlert, Zap, ArrowRight } from 'lucide-react';

export default function HeroSection() {
  return (
    <section className="relative bg-slate-950 text-slate-100 overflow-hidden py-24 lg:py-32">
      {/* Background patterns for industrial feel */}
      <div className="absolute inset-0 z-0 opacity-10" style={{
        backgroundImage: `radial-gradient(circle at 2px 2px, rgba(255,255,255,0.15) 1px, transparent 0)`,
        backgroundSize: '32px 32px'
      }} />

      <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative z-10 max-w-6xl">
        <div className="flex flex-col items-center text-center max-w-4xl mx-auto">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900 border border-slate-800 text-amber-500 font-mono text-sm font-semibold tracking-wide uppercase mb-8">
            <ShieldAlert size={16} />
            <span className="tracking-widest text-xs">Proteção NBR 5410 & NR-10</span>
          </div>

          {/* Main Headline */}
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-extrabold tracking-tight text-white leading-tight mb-6">
            Engenharia de Infraestrutura e Energia Solar que{' '}
            <span className="text-amber-500 block sm:inline mt-2 sm:mt-0">
              blinda seu patrimônio
            </span>{' '}
            contra riscos e falhas.
          </h1>

          {/* Authority Subheadline */}
          <p className="text-lg md:text-xl text-slate-400 mb-10 max-w-3xl leading-relaxed">
            Projetos executados e assinados por <strong className="text-slate-200">Tecnólogo Especialista (CREA-RJ)</strong>. Conformidade absoluta com normas técnicas para segurança de condomínios e indústrias.
          </p>

          {/* CTA */}
          <div className="flex flex-col sm:flex-row gap-4 w-full sm:w-auto">
            <a
              href="https://wa.me/5521999999999?text=Olá, gostaria de solicitar uma Avaliação Técnica."
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center justify-center px-8 py-4 text-base font-bold text-slate-950 bg-amber-500 hover:bg-amber-400 rounded-lg transition-all duration-300 transform hover:-translate-y-1 hover:shadow-[0_0_20px_rgba(245,158,11,0.4)]"
            >
              <Zap className="mr-2 h-5 w-5" />
              Solicitar Avaliação Técnica
            </a>
            <a
              href="#portfolio"
              className="inline-flex items-center justify-center px-8 py-4 text-base font-medium text-white border border-slate-700 hover:border-slate-500 hover:bg-slate-800 rounded-lg transition-all duration-300"
            >
              Ver Casos Reais
              <ArrowRight className="ml-2 h-5 w-5" />
            </a>
          </div>

          {/* Trust indicators */}
          <div className="mt-16 pt-8 border-t border-slate-800/60 w-full">
            <p className="text-sm text-slate-500 uppercase tracking-widest mb-6 font-semibold">Tecnologia e Padrão Industrial</p>
            <div className="flex flex-wrap justify-center gap-6 md:gap-12 opacity-60 grayscale">
              {/* Placeholders for partner/tech logos if any, just text for now */}
              <span className="font-mono text-xl font-bold">CREA-RJ</span>
              <span className="font-mono text-xl font-bold">ABNT NBR</span>
              <span className="font-mono text-xl font-bold">WEG Solar</span>
              <span className="font-mono text-xl font-bold">Eletrodutos Galvanizados</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
