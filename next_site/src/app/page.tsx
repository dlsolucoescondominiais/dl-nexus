import HeroSection from '@/components/HeroSection';
import RiskCalculator from '@/components/RiskCalculator';
import SmartPortfolio from '@/components/SmartPortfolio';

export default function Home() {
  return (
    <div className="min-h-screen bg-slate-950 font-sans selection:bg-amber-500/30 selection:text-amber-200">
      <main>
        <HeroSection />
        <RiskCalculator />
        <SmartPortfolio />
      </main>

      <footer className="bg-slate-950 py-12 border-t border-slate-900 text-center">
        <div className="container mx-auto px-4">
          <p className="text-slate-500 text-sm">
            &copy; {new Date().getFullYear()} DL Soluções Condominiais. Engenharia e Tecnologia para Condomínios e Indústrias no RJ.<br/>
            Responsável Técnico CREA-RJ.
          </p>
        </div>
      </footer>
    </div>
  );
}
