"use client";
import React, { useState } from 'react';
import { Send, Zap, Shield, Sun, FileText, CheckCircle } from 'lucide-react';

export default function Home() {
  const [formData, setFormData] = useState({
    nome: '',
    nome_condominio: '',
    telefone: '',
    email: '',
    tipo_imovel: 'Condomínio',
    num_unidades: '',
    tipo_servico: 'Redes',
    mensagem: ''
  });
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus('loading');

    try {
      // Aqui você vai colocar a URL do seu Webhook do n8n!
      // Ex: https://n8n.dlsolucoescondominiais.com.br/webhook/receber-lead
      const response = await fetch('/api/webhook-proxy', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });

      if (response.ok) {
        setStatus('success');
      } else {
        setStatus('error');
      }
    } catch (error) {
      setStatus('error');
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-900">
      {/* Header */}
      <header className="bg-blue-900 text-white py-6 shadow-md">
        <div className="container mx-auto px-4 flex justify-between items-center">
          <div className="flex items-center gap-2">
            <Shield className="w-8 h-8 text-blue-300" />
            <h1 className="text-2xl font-bold tracking-tight">DL Soluções Condominiais</h1>
          </div>
          <nav className="hidden md:flex gap-6 font-medium text-blue-100">
            <a href="#" className="hover:text-white transition-colors">Serviços</a>
            <a href="#" className="hover:text-white transition-colors">Portfólio</a>
            <a href="#" className="hover:text-white transition-colors">Sobre nós</a>
          </nav>
        </div>
      </header>

      <main className="container mx-auto px-4 py-12 grid md:grid-cols-2 gap-12 items-start">
        {/* Lado Esquerdo - Info */}
        <div className="space-y-8">
          <div>
            <h2 className="text-4xl font-extrabold text-slate-900 leading-tight mb-4">
              Modernização e Segurança para o seu Condomínio
            </h2>
            <p className="text-lg text-slate-600">
              Especialistas em Redes, Energia Solar, CFTV e Elétrica.
              Garantimos eficiência operacional (OPEX) e valorização patrimonial (CAPEX) com tecnologia de ponta.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100 flex flex-col items-center text-center">
              <div className="bg-blue-100 p-3 rounded-full mb-4">
                <Zap className="w-6 h-6 text-blue-600" />
              </div>
              <h3 className="font-bold text-slate-800">Elétrica & Redes</h3>
              <p className="text-sm text-slate-500 mt-2">Infraestrutura robusta para dados e energia.</p>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100 flex flex-col items-center text-center">
              <div className="bg-yellow-100 p-3 rounded-full mb-4">
                <Sun className="w-6 h-6 text-yellow-600" />
              </div>
              <h3 className="font-bold text-slate-800">Energia Solar</h3>
              <p className="text-sm text-slate-500 mt-2">Redução drástica nos custos operacionais.</p>
            </div>
          </div>
        </div>

        {/* Lado Direito - Formulário que envia pro n8n */}
        <div className="bg-white p-8 rounded-2xl shadow-xl border border-slate-100 relative overflow-hidden">
          <div className="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-blue-600 to-blue-400"></div>

          <h3 className="text-2xl font-bold mb-2 flex items-center gap-2">
            <FileText className="w-6 h-6 text-blue-600" />
            Solicite um Orçamento
          </h3>
          <p className="text-slate-500 mb-6 text-sm">
            Nossa Inteligência Artificial (Diego) fará a triagem inicial para agilizar seu atendimento.
          </p>

          {status === 'success' ? (
            <div className="bg-green-50 border border-green-200 rounded-lg p-6 text-center space-y-4">
              <CheckCircle className="w-12 h-12 text-green-500 mx-auto" />
              <h4 className="text-lg font-bold text-green-800">Solicitação Recebida!</h4>
              <p className="text-green-700">
                Nosso sistema processou seus dados. Você receberá um e-mail em breve com os próximos passos.
              </p>
              <button
                onClick={() => setStatus('idle')}
                className="text-sm text-green-600 hover:text-green-800 font-medium"
              >
                Enviar nova solicitação
              </button>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-1">
                  <label className="text-sm font-medium text-slate-700">Seu Nome *</label>
                  <input required name="nome" onChange={handleChange} className="w-full p-3 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-all" placeholder="Ex: João Síndico" />
                </div>
                <div className="space-y-1">
                  <label className="text-sm font-medium text-slate-700">Condomínio/Colégio *</label>
                  <input required name="nome_condominio" onChange={handleChange} className="w-full p-3 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-all" placeholder="Ex: Condomínio Flores" />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-1">
                  <label className="text-sm font-medium text-slate-700">Telefone *</label>
                  <input required name="telefone" onChange={handleChange} className="w-full p-3 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-all" placeholder="(11) 99999-9999" />
                </div>
                <div className="space-y-1">
                  <label className="text-sm font-medium text-slate-700">E-mail *</label>
                  <input required type="email" name="email" onChange={handleChange} className="w-full p-3 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-all" placeholder="joao@email.com" />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-1">
                  <label className="text-sm font-medium text-slate-700">Tipo de Imóvel</label>
                  <select name="tipo_imovel" onChange={handleChange} className="w-full p-3 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none bg-white">
                    <option>Condomínio Residencial</option>
                    <option>Condomínio Comercial</option>
                    <option>Colégio/Instituição</option>
                    <option>Outros</option>
                  </select>
                </div>
                <div className="space-y-1">
                  <label className="text-sm font-medium text-slate-700">Unidades (Aprox.)</label>
                  <input type="number" name="num_unidades" onChange={handleChange} className="w-full p-3 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-all" placeholder="Ex: 120" />
                </div>
              </div>

              <div className="space-y-1">
                <label className="text-sm font-medium text-slate-700">Qual serviço você precisa?</label>
                <select name="tipo_servico" onChange={handleChange} className="w-full p-3 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none bg-white">
                  <option>Redes e Infraestrutura de TI</option>
                  <option>Energia Solar Fotovoltaica</option>
                  <option>Elétrica e Cabeamento</option>
                  <option>Segurança Eletrônica (CFTV)</option>
                  <option>Projeto Integrado</option>
                </select>
              </div>

              <div className="space-y-1">
                <label className="text-sm font-medium text-slate-700">Detalhes adicionais</label>
                <textarea name="mensagem" onChange={handleChange} rows={3} className="w-full p-3 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-all resize-none" placeholder="Descreva brevemente sua necessidade..."></textarea>
              </div>

              <button
                type="submit"
                disabled={status === 'loading'}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-4 rounded-lg flex items-center justify-center gap-2 transition-colors disabled:opacity-70 disabled:cursor-not-allowed mt-4"
              >
                {status === 'loading' ? (
                  <div className="w-6 h-6 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                ) : (
                  <>
                    <Send className="w-5 h-5" />
                    Enviar Solicitação
                  </>
                )}
              </button>
            </form>
          )}
        </div>
      </main>
    </div>
  );
}
