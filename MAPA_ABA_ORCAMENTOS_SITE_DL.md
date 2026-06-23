# Mapa da Aba "Orçamentos" no Site DL

**Data:** 2026-06-21
**Objetivo:** Definir a experiência do usuário ao acessar a aba de orçamentos no site, segmentando por perfil antes de exibir campos específicos.

---

## 1. Estrutura da Aba

A aba "Orçamentos" substitui o formulário genérico por uma experiência segmentada. O usuário primeiro escolhe seu perfil, e o formulário se adapta.

```
[Aba Orçamentos]
  │
  ├── Sou Síndico / Condomínio
  ├── Sou Pessoa Física
  ├── Sou PJ Escola
  ├── Sou PJ Restaurante
  ├── Sou PJ Lanchonete
  ├── Sou PJ Confeitaria
  └── Sou PJ Empresa / Comércio
```

---

## 2. Perfil: Síndico / Condomínio (`condominio`)

**Linguagem pública:** "Soluções técnicas para proteção patrimonial e modernização condominial."

### Catálogo de Serviços
- DL Guardião (CFTV e Segurança)
- DL Fortress (Controle de Acesso)
- DL Acqua (Automação de Bombas)
- DL Gatekeeper (Automação de Portões)
- DL Volt (Elétrica Predial)
- DL VoltCharge (Carregadores EV)
- DL EcoVolt (Energia Solar)
- DL Alerta (Prevenção de Incêndio)
- DL Partner (Contrato de Manutenção)

### Campos Específicos
- `numero_unidades` (recomendado — obrigatório para rateio)
- `numero_blocos`
- `cnpj` (recomendado)
- `responsavel_aprovacao` (síndico ou administradora)

---

## 3. Perfil: Pessoa Física (`pessoa_fisica`)

**Linguagem pública:** "Soluções técnicas residenciais de energia, backup e segurança."

### Catálogo de Serviços
- Energia Solar Residencial
- Sistema Solar com Baterias
- Backup de Energia:
  - 8 horas (TV, geladeira, iluminação)
  - 12 horas (TV, geladeira, portões, CFTV)
  - 24 horas (casa completa, ar-condicionado)
- Segurança Eletrônica Residencial (CFTV, alarme, sensores)
- Elétrica Técnica Residencial (quadros, disjuntores, fiação)

### Campos Específicos
- `cpf` (opcional no primeiro contato)
- `tipo_imovel` (casa, apartamento, chácara)
- `area_telhado_m2` (para dimensionamento solar)
- `conta_energia_media` (para cálculo de retorno)

---

## 4. Perfil: PJ Escola (`escola`)

**Linguagem pública:** "Segurança e infraestrutura técnica para instituições de ensino."

### Catálogo de Serviços
- CFTV (câmeras internas e externas)
- Controle de acesso (portaria, catracas)
- Elétrica predial
- Alarme e sensores
- Automação de iluminação
- Energia solar

### Campos Específicos
- `cnpj` (recomendado)
- `numero_salas`
- `numero_andares`

---

## 5. Perfil: PJ Restaurante (`restaurante`)

**Linguagem pública:** "Manutenção e infraestrutura elétrica para restaurantes."

### Catálogo de Serviços
- DL Express (Suporte Rápido)
- Mult•Grill (reparo e manutenção de grills)
- Chapas industriais (instalação, reparo, regulagem)
- Grills e churrasqueiras profissionais
- Fritadeiras industriais (elétrica e gás)
- Elétrica (quadros, fiação, tomadas de potência)
- CFTV
- Controle de acesso
- Manutenção preventiva

### Campos Específicos
- `cnpj` (recomendado)
- `equipamentos_atuais` (lista aberta)
- `voltagem_disponivel` (127V, 220V, trifásico)

---

## 6. Perfil: PJ Lanchonete (`lanchonete`)

**Linguagem pública:** "Soluções elétricas e de equipamentos para lanchonetes."

### Catálogo de Serviços
(Mesmo catálogo do Restaurante, adaptado para escala menor)
- DL Express
- Mult•Grill
- Chapas
- Fritadeiras
- Elétrica (quadros, tomadas de potência)
- CFTV
- Manutenção preventiva

### Campos Específicos
- `cnpj` (recomendado)
- `equipamentos_atuais`

---

## 7. Perfil: PJ Confeitaria (`confeitaria`)

**Linguagem pública:** "Infraestrutura elétrica e manutenção para confeitarias."

### Catálogo de Serviços
- DL Express
- Elétrica especializada (quadros, disjuntores, fiação para fornos)
- Tomadas de potência (fornos, batedeiras industriais, câmaras frias)
- Manutenção preventiva
- CFTV

### Campos Específicos
- `cnpj` (recomendado)
- `equipamentos_atuais`
- `potencia_total_kw`

---

## 8. Perfil: PJ Empresa / Comércio (`empresa`)

**Linguagem pública:** "Soluções técnicas corporativas de segurança, energia e infraestrutura."

### Catálogo de Serviços
- CFTV
- Controle de acesso
- Elétrica predial
- Automação
- Energia solar
- DL Partner (Contrato de manutenção)

### Campos Específicos
- `cnpj` (recomendado)
- `numero_funcionarios`
- `area_total_m2`

---

## 9. Campos Comuns a Todos os Perfis

Estes campos aparecem em TODOS os formulários, independente do perfil:

- `nome` *
- `whatsapp` *
- `email` *
- `nome_empresa_ou_condominio` *
- `endereco_completo` *
- `bairro` *
- `cidade` *
- `cep`
- `servico_interesse` * (filtrado pelo catálogo do perfil)
- `urgencia` *
- `descricao` *
- `melhor_horario`
- `tipo_orcamento` (Novo, Adequação, Manutenção)
- `upload_imagem` (evidência visual)
- `upload_video` (evidência visual)
- `aceite_contato` *
- `aceite_lgpd` *

(*) = obrigatório

---

## 10. Implementação Técnica

O formulário será um **único HTML** com lógica JavaScript que:
1. Exibe os 7 cards de perfil.
2. Ao selecionar, revela os campos comuns + campos específicos daquele perfil.
3. Filtra o `<select>` de `servico_interesse` pelo catálogo do perfil.
4. Injeta o `tipo_cliente` automaticamente no payload.
5. Envia para `/webhook-test/orcamento-v2` (homologação) ou `/webhook/orcamento-v2` (produção futura).

O formulário atual (`#dl-contact-form` no `index.html`) permanece como fallback.
