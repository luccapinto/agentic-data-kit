---
name: pbi-dashboard-documentation
description: Geração automatizada de documentação Markdown estruturada lendo TMDL e PBIR.
---

# 📚 Skill: pbi-dashboard-documentation

Ensina o agente a gerar documentação estruturada do dashboard a partir dos arquivos.

## 🎯 Por que isso existe
Dashboards corporativos precisam de catalogação clara. Você usa essa skill para gerar `DASHBOARD_DOC.md` na raiz do projeto. O conteúdo extraído automaticamente incluirá o Data Dictionary, o inventário de DAX, os relacionamentos e um mapa que conecta qual visual usa qual medida.

## 📝 Especificação e Estrutura do Documento

O arquivo `DASHBOARD_DOC.md` gerado por esta skill possuirá a seguinte topologia:

### 1. Visão Geral
* Título, Data de Geração e metadados.
* Contagem (totais) de: Tabelas, Medidas, Páginas, e Visuais (lendo os metadados do parser).

### 2. Data Dictionary (Tabelas e Colunas)
Para cada `.tmdl` encontrado em `tables/`:
```markdown
## Tabela: NomeTabela
> Descrição da tabela (proveniente da propriedade `description`)

| Coluna | Tipo | Oculta | Descrição |
|--------|------|--------|-----------|
| ID | int64 | Não | Chave primária |
```

### 3. Inventário de Medidas
```markdown
## Medidas — NomeTabela

### [Medida] NomeDaMedida
**Pasta:** NomeDaPasta | **Formato:** #,##0
**Descrição:** Texto da descrição (se existir, caso contrário "[sem descrição]").
**Expressão DAX:**
` ` `dax
CALCULATE( SUM(Tabela[Coluna]) )
` ` `
```

### 4. Mapa Visual → Medida → Coluna
Leitura do `.Report/definition/pages/*/visuals/*/visual.json`:
Extrai `projections` para linkar.

```markdown
## Página: Resumo
### Visual: Título do Visual (barChart)
- **Eixo X:** Tabela[Coluna]
- **Eixo Y:** [MedidaX]
```

### 5. Relacionamentos
Leitura de `relationships.tmdl`:
```markdown
| De | Para | Cardinalidade | Direção |
|----|------|---------------|---------|
| Vendas[ID] | Dim[ID] | *:1 | Single |
```

## ⚙️ Estratégia de Parsing
* **TMDL:** Como não há parser nativo limpo para JSON, as variáveis serão extraídas através de parsing de bloco (Regex ou lógica em shell/powershell sobre arquivos de texto indentado).
* **PBIR:** Como os visuais são JSON puro (`Get-Content | ConvertFrom-Json`), é fácil iterar sob os fields, values e categories nas projecções.

## ⚠️ Limitações Documentadas
* Medidas ou Tabelas sem `description` mostrarão tag `[sem descrição]`. Sugira ao usuário rodar validação e preencher posteriormente.
* Visuais customizados (3rd party) ou aqueles sem um container title visível são identificados apenas pelo seu GUID na doc. Ignorar eventuais discrepâncias de schema graciosamente.
