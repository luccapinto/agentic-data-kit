---
description: Executa validação completa de qualidade de um projeto PBIP.
name: validate-pbi
---

**Contexto:** {{selection}}

# 🔎 Workflow: /validate-pbi

**Comando:** `/validate-pbi [caminho/do/projeto.pbip]`

O workflow que atua como checkpoint primário de sanidade de um projeto PBIP. Responde à pergunta "Meu modelo está saudável?" executando todas as verificações de qualidade do modelo semântico. 

Se o caminho não for especificado, utiliza o projeto na pasta atual. Se houver mais de um, o agente pergunta.

## 🔄 Passos do Fluxo

### 1. Orientação Inicial
Usa `pbi-pbip-structure` para assegurar que estamos num diretório de projeto PBIP válido. Em caso negativo, informa o erro e interrompe o fluxo.

### 2. Escolha do Modo de Conexão
Analisa o ambiente:
* **Desktop Aberto:** (Recomendado) Valida via TOM Localmente (`pbi-live-connection`). A validação em tempo de execução via TOM inclui erros do próprio Engine DAX.
* **Desktop Fechado:** Valida apenas por parsing de texto através dos arquivos TMDL (Cobertura parcial, não resolve referências quebradas).

### 3. Quality Rules Pipeline
Executa o playbook nativo `pbi-quality-rules` (`.agent/skills/pbi-quality-rules/pbi-quality-rules.yaml`) no projeto. Anota todas as ocorrências de classificação: Warning e Error.

### 4. Avaliação Adicional de Estrutura
- **Cobertura de Docs:** Calcula métricas simples (Quantidade de Tabelas/Medidas vs Quantidade de Descriptions preenchidos).
- **Relações e Tipologia:** Identifica "islands" (Tabelas sem relações), direções Bidirecionais desaconselhadas e tipos de junções não convencionais (many-to-many).

### 5. Apresentação (Output do Agente)

Gera um relatório markdown curto:

```markdown
# Relatório de Validação — [NomeProjeto]
**Data:** [Data de Hoje] | **Modo:** [TOM ao vivo / Arquivos TMDL]

## Resumo
| Categoria | Erros | Warnings |
|-----------|-------|----------|
| Nomeação  | 0     | 3        |
| DAX       | 1     | 2        |
| Modelo    | 0     | 1        |
| Docs      | 0     | 8        |

## Erros (corrigir antes de publicar)
- [DAX_001] Medida "Turnover %" — expressão vazia

## Warnings
- [NAMING_004] 3 medidas sem displayFolder: "Headcount", "Ativos"

## Cobertura de Documentação
- Tabelas: 5/7 com descrição (71%)
- Medidas: 12/20 com descrição (60%)

## Relações
- 1 relação bidirecional encontrada: Fatos ↔ DimTempo — revisar se necessário
```

### 6. Sugestão de Reparos
Após exibir o relatório, o agente automaticamente sugere arrumar todos os **Errors**. Ele questiona se o usuário quer arrumar os **Warnings**, ou se prefere atuar nas Descriptions que faltam.
