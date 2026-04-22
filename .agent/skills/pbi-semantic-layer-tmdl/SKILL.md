---
name: pbi-semantic-layer-tmdl
description: Edição de arquivos TMDL e regras arquiteturais do SemanticModel no formato PBIP (offline)
---

# 📝 Skill: pbi-semantic-layer-tmdl

Ensina a orientação espacial dentro do `.SemanticModel` e a sintaxe TMDL para criar ou editar modelos do zero quando o Desktop está **FECHADO**.

## 🎯 Quando Usar
* Use este modo para qualquer edição no modelo semântico (medidas, tabelas, relações).
* **MANDATÓRIO:** O Power BI Desktop deve estar **FECHADO** antes de salvar as alterações nos arquivos TMDL para evitar corrupção de arquivos ou perda de trabalho (o Desktop mantém o modelo em memória e sobrescreve o disco ao salvar).

## 📂 Arquitetura do `.SemanticModel`

A estrutura obrigatória dentro do projeto PBIP segue:
```
NomeProjeto.SemanticModel/
  definition/
    model.tmdl           ← Definição principal (listagem de todas as tabelas)
    tables/
      NomeTabela.tmdl    ← UMA tabela por arquivo (Regra de Ouro!)
    relationships.tmdl   ← Todas as relações do modelo
    cultures/            ← Traduções
    expressions.tmdl     ← Expressões compartilhadas e parâmetros M
    roles.tmdl           ← Regras de RLS
```

* **O que você DEVE editar:** Arquivos `.tmdl`.
* **O que você NÃO DEVE editar:** Arquivos em `.pbi/` (ex: `localSettings.json`, `cache.abf`).

## 🧠 Sintaxe TMDL (Referência para LLMs)

Para garantir compatibilidade e sucesso ao escrever o código, siga o formato abaixo.

### 1. Declaração de Tabela e Medida
* As definições começam com `table NomeTabela`.
* Medidas começam com `measure NomeMedida = Expressao DAX`
* Descrições usam a propriedade `description: "Texto"`.

```tmdl
table 'Vendas'
    description: "Fato principal de vendas."
    
    measure 'Total Vendas' = SUM(Vendas[Valor])
        formatString: "R$ #,##0.00"
        displayFolder: "Metricas Financeiras"
        
    column 'Valor'
        dataType: decimal
        sourceColumn: "BaseValor"
```

### 2. Relacionamentos (`relationships.tmdl`)
```tmdl
relationship 'Vendas_Para_DimData'
    fromColumn: Vendas.DataId
    toColumn: DimData.DataId
    fromCardinality: many
    toCardinality: one
    crossFilteringBehavior: bothDirections
```

## ⚙️ Regras Estritas de Serialização

1. **Cada tabela = um arquivo `.tmdl` separado.** Nunca defina todas as tabelas dentro de `model.tmdl`.
2. As propriedades devem ser listadas na ordem correta: `dataType` e `sourceColumn` primeiro, depois propriedades cosméticas.
3. **Indentação:** Use tabulação simples (tabs) ou espaços alinhados com o resto do arquivo.
4. **Strings multilinha no DAX:** Use `\` no final da linha se precisar quebrar longos blocos sem perder a sintaxe.

## ⚠️ Checklist e Protocolo de Verificação

### Antes de Salvar
1. O Power BI Desktop está completamente fechado?

### Após Salvar (Verificação Pós-Edição)
1. Peça ao usuário para abrir o arquivo `.pbip` no Power BI Desktop.
2. Aguarde o carregamento completo (até que o painel "Campos" seja populado).
3. Peça ao usuário para abrir **Exibir → Diagnóstico** e reportar qualquer erro ou aviso exibido no topo.
4. **Validação de Medidas:** Para cada medida criada ou modificada, peça ao usuário para arrastá-la para um visual de **Cartão** (Card) e confirmar se o valor retornado está correto ou se exibe um erro (ícone de exclamação vermelho).
5. Se houver erro: Releia o TMDL editado, identifique o problema de sintaxe ou referência e proponha a correção.

> [!TIP]
> Este protocolo garante que o modelo permaneça íntegro sem a necessidade de uma conexão live instável.
