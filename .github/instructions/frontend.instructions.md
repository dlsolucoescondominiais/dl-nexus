---
description: "Regras específicas para componentes React/Next.js da DL Soluções"
applyTo: "frontend/**/*.{tsx,ts,jsx,js},frontend_react_dl/**/*.{tsx,ts,jsx,js}"
---

# Instruções: Frontend DL Soluções (Next.js + Tailwind)

## Componentes React

- Sempre usar **Server Components** por defeito no App Router
- Marcar `"use client"` apenas quando necessário (hooks de state/effect, event handlers)
- Props sempre tipadas com interface TypeScript — nunca `any` ou `object`
- Desestruturar props no parâmetro da função, não dentro do corpo

```tsx
// ✅ CORRETO
interface LeadFormProps {
  serviceType: 'solar' | 'cftv' | 'automacao' | 'eletrica';
  onSubmit: (data: LeadPayload) => Promise<void>;
}

export function LeadForm({ serviceType, onSubmit }: LeadFormProps) { ... }

// ❌ ERRADO
export function LeadForm(props: any) { ... }
```

## Tailwind CSS

- Sempre usar as cores customizadas do design system DL (definidas em `tailwind.config.ts`)
- Paleta DL: `dl-blue` (azul técnico), `dl-orange` (laranja CTA), `dl-dark` (fundo escuro)
- Nunca usar cores hardcoded inline (`style={{ color: '#ff6600' }}`)
- Responsividade: mobile-first (`base → sm → md → lg → xl`)

## Copy e UX

- CTAs primários: sempre `"Solicitar Avaliação Técnica"` com `id="cta-primary"`
- CTAs secundários: `"Ver Projetos Executados"` ou `"Consultar Especialista"`
- Formulários: campo obrigatório `tipo_condominio` (Residencial/Comercial/Misto)
- Sempre incluir badge CREA-RJ próximo a qualquer formulário de contacto
- Loading states: sempre com skeleton loader, nunca spinner simples

## Acessibilidade

- `aria-label` obrigatório em botões que contêm apenas ícones
- Contraste mínimo WCAG AA (4.5:1) para texto sobre fundos coloridos
- `alt` descritivo em todas as imagens (descrever o serviço técnico, não "imagem")

## Performance

- Imagens: sempre `next/image` com `priority` nos primeiros elementos da viewport
- Fontes: sempre `next/font` — nunca `<link>` manual para Google Fonts
- Bundle: lazy load componentes pesados com `dynamic(() => import(...))`
