---
name: pbi-tmdl-authoring
description: Autoria direta de arquivos TMDL dentro de projetos PBIP (com Desktop fechado)
---

# 📝 Skill: pbi-tmdl-authoring

Autoria direta de arquivos TMDL dentro de projetos PBIP, para uso primário quando o Desktop está fechado, em refactors grandes ou criação de modelos semânticos do zero.

## 🎯 Quando Usar
* Use este modo: Desktop fechado, criação de modelo do zero, refactor grande (> 5 objetos)
* Use TOM ao vivo (`pbi-live-connection`): Desktop aberto, edição incremental, testes de DAX

## 📂 Estrutura do SemanticModel no PBIP

```
NomeProjeto.SemanticModel/
  definition/
    model.tmdl           ← definição principal do modelo
    tables/
      NomeTabela.tmdl    ← uma tabela por arquivo
    relationships.tmdl   ← todas as relações
    cultures/            ← traduções
    expressions.tmdl     ← shared expressions / parâmetros M
    roles.tmdl           ← RLS roles
```

## 🧠 Sintaxe TMDL 

* **Tabelas, Colunas e Medidas:**
  As definições de tabela começam com `table NomeTabela`.
  Medidas começam com `measure NomeMedida = Expressao`
* **Tipos de dados suportados:** `int64`, `string`, `decimal`, `dateTime`, `boolean`
* **Colunas:** Podem ter um `sourceColumn` (referência da origem) ou usar `expression` para colunas calculadas.
* **Expressões Multilinha:** Para medidas com DAX longo, idente as linhas subsequentes ou use blocos.
* **Propriedades Opcionais:** `isHidden`, `displayFolder`, `formatString`
* **Anotações:** `annotation PBI_ResultType = Table`
* **Descrições:** A propriedade `description: "Texto de exemplo"` deve ser sempre incluída se possível.
* **Tabelas Calculadas:** Utilize `partition` com `mode: calculated`.
* **Relações (em `relationships.tmdl`):** 
  ```tmdl
  relationship relationship_name
      fromColumn: TabelaOrigem.ColunaOrigem
      toColumn: TabelaDestino.ColunaDestino
      fromCardinality: many
      toCardinality: one
      crossFilteringBehavior: bothDirections
  ```

## ⚙️ Regras de Serialização do Desktop

* Cada tabela = um arquivo `.tmdl` separado. Nunca defina tudo no `model.tmdl`.
* As propriedades devem ser listadas na ordem que o Desktop espera para evitar erros de parse (ex: `formatString` antes de `displayFolder` na maioria dos casos).
* **Indentação:** Tabulação simples (tabs) ou espaços (normalmente 2 espaços por nível de indentação, siga o padrão do arquivo local).
* **Strings multilinha no DAX:** Use `\` no final da linha se necessário para escapes.

## ⚠️ Cuidados Especiais

* **Nunca edite TMDL com o Desktop aberto** no mesmo arquivo. O Desktop possui lock sobre a versão em memória e sobrescreverá seu trabalho ao salvar.
* Sempre valide o JSON / parsing do seu arquivo gerado (verifique blocos e idents) antes de testar a abertura no Desktop.
* Após completar o refactor via edição de arquivo, peça ao usuário para abrir o Desktop e verificar se há erros no painel de diagnósticos do Power BI.
