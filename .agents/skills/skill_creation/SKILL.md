---
name: Criação de Skills
description: Guia padronizado para criar novas skills no workspace, incluindo estrutura de pastas, formato do SKILL.md e boas práticas.
---

# Skill de Criação de Skills

Use este guia sempre que precisar criar uma nova skill para o agente.

---

## 1. O Que É Uma Skill?

Uma skill é um **conjunto de instruções, scripts e recursos** que ampliam as capacidades do agente para tarefas especializadas. Cada skill fica em sua própria pasta dentro de `.agents/skills/`.

---

## 2. Estrutura de Pastas

Crie a seguinte estrutura para cada nova skill:

```
.agents/skills/<nome_da_skill>/
├── SKILL.md          # (obrigatório) Instruções principais
├── scripts/          # (opcional) Scripts auxiliares (.py, .sh, .ps1, etc.)
├── examples/         # (opcional) Exemplos de uso e referências
└── resources/        # (opcional) Templates, assets, arquivos adicionais
```

### Regras de nomenclatura
- Use **snake_case** para o nome da pasta (ex: `gerar_proposta`, `postar_instagram`).
- Não use espaços, acentos ou caracteres especiais no nome da pasta.

---

## 3. Formato do SKILL.md

O arquivo `SKILL.md` deve seguir este template:

```markdown
---
name: Nome Legível da Skill
description: Uma frase curta descrevendo o que a skill faz.
---

# Nome da Skill

Descrição detalhada do objetivo da skill.

## Pré-requisitos

- Lista de dependências (bibliotecas, APIs, credenciais, etc.)
- Variáveis de ambiente necessárias (referência ao `.env`)

## Instruções Passo a Passo

1. Primeiro passo
2. Segundo passo
3. ...

## Exemplos de Uso

Mostre cenários reais de quando e como usar esta skill.

## Notas e Cuidados

- Limitações conhecidas
- Erros comuns e como evitá-los
```

### Campos do Frontmatter YAML
| Campo         | Obrigatório | Descrição                                    |
|---------------|:-----------:|----------------------------------------------|
| `name`        | ✅          | Nome legível da skill                        |
| `description` | ✅          | Frase curta (aparece em listagens e buscas)  |

---

## 4. Checklist para Criar uma Nova Skill

- [ ] Definir o **objetivo claro** da skill (o que ela resolve?)
- [ ] Criar a pasta em `.agents/skills/<nome_da_skill>/`
- [ ] Escrever o `SKILL.md` seguindo o template acima
- [ ] Adicionar scripts em `scripts/` se necessário
- [ ] Adicionar exemplos em `examples/` se aplicável
- [ ] Testar a skill manualmente pelo menos uma vez
- [ ] Verificar que o `SKILL.md` é encontrável pelo agente (busca por `SKILL.md`)

---

## 5. Boas Práticas

1. **Seja específico** — Instruções vagas geram resultados ruins. Escreva cada passo de forma que qualquer pessoa consiga seguir.
2. **Documente dependências** — Se a skill precisa de uma API key ou biblioteca, liste tudo nos pré-requisitos.
3. **Use o `.env` para segredos** — Nunca coloque senhas ou chaves diretamente no `SKILL.md`.
4. **Mantenha atualizado** — Quando a skill mudar, atualize o `SKILL.md` junto.
5. **Uma skill = uma responsabilidade** — Não misture coisas diferentes na mesma skill.

---

## 6. Exemplo Rápido: Criando a Skill "gerar_proposta"

```powershell
# Criar a estrutura
mkdir .agents/skills/gerar_proposta
mkdir .agents/skills/gerar_proposta/scripts
mkdir .agents/skills/gerar_proposta/resources
```

Depois, crie o `SKILL.md` dentro da pasta com as instruções específicas de como gerar uma proposta comercial para a DL Soluções Condominiais.