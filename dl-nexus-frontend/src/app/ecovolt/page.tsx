"use client";
import React from 'react';
import {
  Zap, Settings, Activity, ShieldCheck, Sun, Leaf, Battery, Search,
  Menu, Download, Bell, User, Plus, Home as HomeIcon, Video, AlertTriangle
} from 'lucide-react';

export default function EcoVoltSolarDashboard() {
  return (
    <div className="flex min-h-screen bg-[#060e20] text-[#dae2fd] font-sans overflow-hidden">

      {/* Sidebar - DL Nexus Standard */}
      <aside className="w-64 flex flex-col justify-between border-r border-[#434655]/30 bg-[#0b1326] p-6 relative z-20">
        <div>
          <div className="flex items-center gap-3 mb-10">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-[#3fe56c] to-[#174f26] flex items-center justify-center shadow-[0_0_15px_rgba(63,229,108,0.3)]">
              <Sun className="w-5 h-5 text-white" />
            </div>
            <h1 className="font-bold text-xl tracking-tight">DL <span className="text-[#3fe56c]">Nexus</span></h1>
          </div>
          <nav className="space-y-1">
            <NavItem icon={<HomeIcon className="w-5 h-5" />} label="Visão Geral" />
            <NavItem icon={<ShieldCheck className="w-5 h-5" />} label="DL Commander" />
            <NavItem icon={<Video className="w-5 h-5" />} label="DL Guardião" />
            <NavItem icon={<Zap className="w-5 h-5" />} label="DL Volt" />
            <NavItem icon={<Leaf className="w-5 h-5" />} label="DL EcoVolt Solar" active />
            <NavItem icon={<Battery className="w-5 h-5" />} label="DL VoltCharge" />
            <NavItem icon={<AlertTriangle className="w-5 h-5" />} label="DL Alerta" />
          </nav>
        </div>
        <div className="pt-6 border-t border-[#434655]/30 flex flex-col gap-2">
           <NavItem icon={<Settings className="w-5 h-5" />} label="Configurações" />
           <div className="flex items-center gap-3 mt-4 px-3 py-2 bg-[#171f33] rounded-lg">
             <div className="w-8 h-8 rounded-full bg-blue-500/20 flex items-center justify-center border border-blue-500/50">
                <User className="w-4 h-4 text-blue-400" />
             </div>
             <div>
                <p className="text-xs font-bold text-white">Roberto Técnico</p>
                <p className="text-[10px] text-[#c3c6d7] uppercase tracking-wider">Engenharia N3</p>
             </div>
           </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col h-screen overflow-y-auto">

        {/* Header */}
        <header className="h-20 border-b border-[#434655]/20 bg-[#0b1326]/80 backdrop-blur-md sticky top-0 z-10 flex items-center justify-between px-8">
          <div className="flex items-center gap-4">
            <button className="md:hidden p-2 text-[#c3c6d7] hover:text-white transition-colors">
              <Menu className="w-6 h-6" />
            </button>
            <div className="flex flex-col">
              <span className="text-[10px] font-bold tracking-widest text-[#c3c6d7] uppercase">Módulo Ativo</span>
              <h2 className="text-xl font-bold font-space flex items-center gap-2">
                <Leaf className="w-5 h-5 text-[#3fe56c]" />
                Painel EcoVolt Solar
              </h2>
            </div>
          </div>

          <div className="flex items-center gap-6">
            <div className="relative hidden md:block">
              <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-[#c3c6d7]" />
              <input type="text" placeholder="Buscar telemetria..." className="pl-9 pr-4 py-2 bg-[#131b2e] border border-[#434655]/30 rounded-lg text-sm focus:outline-none focus:border-[#3fe56c]/50 text-white w-64 transition-all" />
            </div>

            <div className="flex items-center gap-4">
              <button className="relative p-2 text-[#c3c6d7] hover:text-white transition-colors">
                <Bell className="w-5 h-5" />
                <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full shadow-[0_0_8px_rgba(239,68,68,0.6)]"></span>
              </button>
              <div className="h-6 w-px bg-[#434655]/30"></div>
              <div className="flex flex-col items-end">
                <span className="text-sm font-bold">Condomínio Prime</span>
                <span className="text-[10px] text-[#3fe56c] font-bold flex items-center gap-1">
                  <div className="w-1.5 h-1.5 bg-[#3fe56c] rounded-full animate-pulse"></div>
                  ONLINE
                </span>
              </div>
            </div>
          </div>
        </header>

        {/* Dashboard Content */}
        <div className="p-8 space-y-6">

          {/* Top KPIs */}
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
            <KpiCard title="Eficiência do Sistema" value="98.4%" icon={<Activity className="w-6 h-6 text-[#3fe56c]" />} trend="+2.1%" trendUp />
            <KpiCard title="Geração Hoje" value="142.5 kWh" icon={<Sun className="w-6 h-6 text-yellow-400" />} trend="Pico: 12h" />
            <KpiCard title="Reserva Baterias" value="84%" icon={<Battery className="w-6 h-6 text-blue-400" />} trend="Estável" />
            <KpiCard title="Economia Mensal" value="R$ 4.250" icon={<Zap className="w-6 h-6 text-[#3fe56c]" />} trend="Fechamento Próx." />
          </div>

          <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
            {/* Chart Area */}
            <div className="xl:col-span-2 bg-[#131b2e]/50 backdrop-blur-sm border border-[#434655]/20 rounded-xl p-6">
               <div className="flex justify-between items-center mb-6">
                 <h3 className="font-bold text-lg font-space">Curva de Geração Solar</h3>
                 <div className="flex bg-[#0b1326] rounded-lg p-1 border border-[#434655]/20">
                    <button className="px-3 py-1 rounded-md text-xs font-bold bg-[#3fe56c]/20 text-[#3fe56c]">HOJE</button>
                    <button className="px-3 py-1 rounded-md text-xs font-bold text-[#c3c6d7] hover:text-white">7D</button>
                 </div>
               </div>
               <div className="h-64 flex items-end justify-between gap-2 border-b border-l border-[#434655]/30 pb-2 pl-2 relative">
                  {/* Fake Chart Bars for visual prototype */}
                  {[40, 55, 75, 90, 100, 85, 60, 45, 20].map((h, i) => (
                    <div key={i} className="w-full bg-gradient-to-t from-[#3fe56c]/20 to-[#3fe56c]/80 rounded-t-sm hover:from-[#3fe56c]/40 hover:to-[#3fe56c] transition-colors cursor-pointer relative group" style={{ height: `${h}%` }}>
                       <div className="opacity-0 group-hover:opacity-100 absolute -top-8 left-1/2 -translate-x-1/2 bg-black text-white text-xs py-1 px-2 rounded font-mono pointer-events-none transition-opacity">
                         {h}kW
                       </div>
                    </div>
                  ))}
               </div>
               <div className="flex justify-between mt-2 text-xs font-mono text-[#c3c6d7] px-2">
                 <span>08:00</span><span>10:00</span><span>12:00</span><span>14:00</span><span>16:00</span><span>18:00</span>
               </div>
            </div>

            {/* Energy Flow Visualization */}
            <div className="bg-[#131b2e]/50 backdrop-blur-sm border border-[#434655]/20 rounded-xl p-6 flex flex-col items-center">
               <h3 className="font-bold text-lg font-space self-start mb-6">Fluxo do Inversor (SCADA)</h3>

               <div className="flex flex-col items-center justify-between flex-1 w-full gap-8 relative py-4">

                  {/* Flow Lines */}
                  <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none opacity-30">
                     <div className="w-px h-16 bg-dashed border-l-2 border-dashed border-[#3fe56c] animate-pulse"></div>
                     <div className="w-px h-16 mt-16 bg-dashed border-l-2 border-dashed border-blue-400"></div>
                  </div>

                  <div className="z-10 bg-[#0b1326] p-3 rounded-xl border border-[#434655]/50 flex items-center gap-3 w-4/5 shadow-lg">
                     <div className="bg-[#3fe56c]/20 p-2 rounded-lg"><Sun className="w-5 h-5 text-[#3fe56c]" /></div>
                     <div><p className="text-[10px] text-[#c3c6d7] uppercase font-bold">Arranjo Solar (MPPT)</p><p className="font-mono text-sm">415V / 38A</p></div>
                  </div>

                  <div className="z-10 bg-[#174f26] p-4 rounded-xl border border-[#3fe56c] flex items-center gap-3 shadow-[0_0_20px_rgba(63,229,108,0.2)]">
                     <Settings className="w-8 h-8 text-[#3fe56c] animate-[spin_4s_linear_infinite]" />
                     <div className="text-center">
                       <p className="text-[10px] text-white uppercase font-bold">Inversor Central</p>
                       <p className="font-mono text-lg font-bold text-[#3fe56c]">15.2 kW</p>
                     </div>
                  </div>

                  <div className="z-10 flex w-full justify-between px-4">
                     <div className="bg-[#0b1326] p-3 rounded-xl border border-[#434655]/50 flex flex-col items-center gap-1 shadow-lg w-[45%]">
                        <Battery className="w-5 h-5 text-blue-400" />
                        <p className="text-[10px] text-[#c3c6d7] uppercase font-bold mt-1">Bateria</p>
                        <p className="font-mono text-xs">84% (+2kW)</p>
                     </div>
                     <div className="bg-[#0b1326] p-3 rounded-xl border border-[#434655]/50 flex flex-col items-center gap-1 shadow-lg w-[45%]">
                        <HomeIcon className="w-5 h-5 text-yellow-500" />
                        <p className="text-[10px] text-[#c3c6d7] uppercase font-bold mt-1">Consumo</p>
                        <p className="font-mono text-xs">13.2 kW</p>
                     </div>
                  </div>
               </div>
            </div>
          </div>

          {/* Logs Table */}
          <div className="bg-[#131b2e]/50 backdrop-blur-sm border border-[#434655]/20 rounded-xl overflow-hidden">
             <div className="p-5 border-b border-[#434655]/30 flex justify-between items-center">
               <h3 className="font-bold text-lg font-space">Logs Operacionais (Eventos)</h3>
               <button className="flex items-center gap-2 text-xs font-bold text-[#3fe56c] hover:text-[#174f26] transition-colors">
                  <Download className="w-4 h-4" /> EXPORTAR
               </button>
             </div>
             <table className="w-full text-left">
               <thead>
                 <tr className="text-[10px] uppercase tracking-widest text-[#c3c6d7] bg-[#0b1326]">
                   <th className="px-6 py-3 font-bold">Data/Hora</th>
                   <th className="px-6 py-3 font-bold">Evento</th>
                   <th className="px-6 py-3 font-bold">Componente</th>
                   <th className="px-6 py-3 font-bold">Status</th>
                 </tr>
               </thead>
               <tbody className="divide-y divide-[#434655]/20 text-sm">
                 <LogRow time="Hoje, 14:22" event="Otimização MPPT Completa" comp="Inversor B" status="RESOLVIDO" color="bg-[#3fe56c]" />
                 <LogRow time="Hoje, 11:45" event="Alerta Térmico (48°C)" comp="String A1" status="ATENÇÃO" color="bg-yellow-500" text="text-yellow-500" bg="bg-yellow-500/10" />
                 <LogRow time="Ontem, 18:10" event="Transição para Bateria" comp="Array Central" status="INFO" color="bg-blue-500" text="text-blue-400" bg="bg-blue-500/10" />
               </tbody>
             </table>
          </div>

        </div>
      </main>

      {/* Floating OS Button */}
      <button className="fixed bottom-8 right-8 w-14 h-14 bg-[#3fe56c] hover:bg-[#174f26] rounded-xl flex items-center justify-center shadow-[0_10px_30px_rgba(63,229,108,0.3)] transition-all hover:scale-105 active:scale-95 group z-50">
         <Plus className="w-6 h-6 text-[#0b1326] group-hover:text-white transition-colors group-hover:rotate-90 duration-300" />
      </button>

    </div>
  );
}

function NavItem({ icon, label, active = false }: { icon: React.ReactNode, label: string, active?: boolean }) {
  return (
    <a href="#" className={`flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-bold transition-all ${active ? 'bg-[#131b2e] text-white border border-[#434655]/50 shadow-sm' : 'text-[#c3c6d7] hover:bg-[#131b2e]/50 hover:text-white'}`}>
      <span className={active ? 'text-[#3fe56c]' : ''}>{icon}</span>
      {label}
    </a>
  )
}

function KpiCard({ title, value, icon, trend, trendUp = false }: { title: string, value: string, icon: React.ReactNode, trend: string, trendUp?: boolean }) {
  return (
    <div className="bg-[#131b2e]/50 backdrop-blur-sm border border-[#434655]/20 p-5 rounded-xl hover:bg-[#131b2e] transition-colors">
      <div className="flex justify-between items-start mb-2">
        <p className="text-[11px] uppercase tracking-widest text-[#c3c6d7] font-bold">{title}</p>
        <div className="p-2 bg-[#0b1326] rounded-lg border border-[#434655]/30">{icon}</div>
      </div>
      <h4 className="text-3xl font-space font-extrabold text-white mb-1">{value}</h4>
      <p className={`text-xs font-bold ${trendUp ? 'text-[#3fe56c]' : 'text-[#c3c6d7]'}`}>{trend}</p>
    </div>
  )
}

function LogRow({ time, event, comp, status, color, text = "text-[#3fe56c]", bg = "bg-[#3fe56c]/10" }: any) {
  return (
    <tr className="hover:bg-[#131b2e] transition-colors group">
      <td className="px-6 py-4 font-mono text-xs text-[#c3c6d7]">{time}</td>
      <td className="px-6 py-4 flex items-center gap-2 font-medium">
        <div className={`w-2 h-2 rounded-full ${color}`}></div>
        {event}
      </td>
      <td className="px-6 py-4 text-[#c3c6d7]">{comp}</td>
      <td className="px-6 py-4">
        <span className={`px-2 py-1 rounded text-[10px] font-black tracking-wider ${bg} ${text}`}>
          {status}
        </span>
      </td>
    </tr>
  )
}
