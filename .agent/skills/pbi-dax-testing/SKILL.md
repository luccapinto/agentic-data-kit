---
name: pbi-dax-testing
description: Testes e validação de medidas DAX contra o modelo ao vivo usando ADOMD.NET
---

# 🧪 Skill: pbi-dax-testing

Esta skill é a sua forma de verificar se o resultado DAX gerado e injetado pelo `pbi-live-connection` faz sentido. Rodar estes testes sistematicamente garante que a medida se comporta de maneira previsível.

## 📊 Categorias de Testes DAX

Como validar os resultados no PBI via script PowerShell com ADOMD:

### 1. Sanidade Básica
Verifica se a medida retorna algo diferente de erro ou BLANK de forma incorreta no geral.
```dax
EVALUATE ROW("resultado", [NomeDaMedida])
```

### 2. Granularidade
Verifica se os resultados agrupados por uma dimensão ou tabela específica fazem sentido.
```dax
EVALUATE
SUMMARIZECOLUMNS(
    Tabela[Coluna],
    "Medida", [NomeDaMedida]
)
ORDER BY [Medida] DESC
```

### 3. Integridade Referencial
Valida chaves de relacionamento, ajudando a detectar registros órfãos.
```dax
EVALUATE
FILTER(
    Tabela,
    ISBLANK(RELATED(TabelaRelacionada[Chave]))
)
```

### 4. Non-blank
Quantos registros existem vs quantos estão em branco (ajuda em testes de cardinalidade/nulos).
```dax
EVALUATE
ROW(
    "total_linhas", COUNTROWS(Tabela),
    "linhas_nulas", COUNTROWS(FILTER(Tabela, ISBLANK(Tabela[Coluna])))
)
```

### 5. Consistência de Total
Sempre teste se a agregação pela dimensão A tem um total que bate com o somatório geral. Problemas no Contexto de Filtro ou de Transição (`CALCULATE`) frequentemente mostram subtotais bons, mas o Grande Total inconsistente ou errado.

## 🔄 Fluxo de Teste DAX Integrado

1. **Agente Edita:** Você edita ou adiciona a medida via TOM (pbi-live-connection).
2. **Definir Teste:** Decida rapidamente qual tipo de teste faz sentido. É uma soma? Count? Use a categoria 1 e 2.
3. **Gerar Query ADOMD:** Monte a Query DAX na estrutura de teste do PowerShell contra `localhost:<porta>`.
4. **Validar:**
   - O número parece razoável?
   - Tem nulos inesperados (BLANKs)?
   - Deu falha no parse do ADOMD? (Isso indicaria erro sintático).
5. **Ações Consequentes:**
   - **Falha:** Mostrar o erro ou comportamento pro usuário.
   - **Sucesso:** Informar o usuário e sugerir salvamento (`Ctrl+S`).

## ⚠️ Limites desta Skill
* **Valores de Negócio:** Você não sabe de antemão se 500k de vendas mensais é alto ou baixo; foca em coerência matemática e de infraestrutura.
* **Inteligência de Tempo:** Os resultados dessas funções (YTD, SAMEPERIODLASTYEAR) dependem fundamentalmente da tabela de calendário e das faturas/períodos de dados na base — avise o usuário que você está dependente dos dados carregados.
* **Revisão Humana:** Esteja ciente que o usuário ainda precisa realizar QA de negócio.
