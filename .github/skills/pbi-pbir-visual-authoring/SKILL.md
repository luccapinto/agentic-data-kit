---
name: pbi-pbir-visual-authoring
description: Edição direta de arquivos de visuais (visual.json) e páginas (page.json) do PBIR
---

# 📊 Skill: pbi-pbir-visual-authoring

O formato PBIR (Power BI Report) descreve de forma agnóstica o visual em JSON aberto. Você pode criar e modificar diretamente esses arquivos `.json` na estrutura PBIP.
**Pré-condição vital:** O Power BI Desktop deve estar fechado para a edição desses arquivos ocorrer sem corromper ou ser sobreposta pela UI ativa.

## 🔧 Estrutura de um `visual.json`

O arquivo padrão base define o tipo, posicionamento e consultas do visual:

```json
{
  "name": "<guid>",
  "position": {
    "x": 0, "y": 0,
    "width": 400, "height": 300,
    "tabOrder": 0
  },
  "visual": {
    "visualType": "barChart",
    "query": {
      "queryState": {
        "Category": { "projections": [...] },
        "Y": { "projections": [...] }
      }
    },
    "visualContainerObjects": {
      "title": [{ "properties": { "text": { "expr": { "Literal": { "Value": "'Título'" }}} } }]
    }
  }
}
```
*Gere GUIDs únicos com `[System.Guid]::NewGuid()` em PowerShell se estiver criando de zero.*

## 📈 Tipos de Visuais e Campos Obrigatórios

* **barChart, columnChart, lineChart:** `Category`, `Y`, `Legend`, `Tooltips`
* **card, multiRowCard:** `Fields`
* **slicer:** `Field` (com opções de dropdown, lista, ou between).
* **tableEx, pivotTable (Matrix):** `Values`, `Rows`, `Columns`
* **filledMap, map:** `Location`, `Size`, `Color`
* **basicShape, image, textbox:** Usados primariamente para design estrutural.

## 📏 Posicionamento e Layout
* **Grid:** Pixel base; Origem (0, 0) no topo-esquerdo.
* **Cálculo de adjacência:** Se o visual A tem `x=0, width=400`, o B pode começar em `x=410` (margem). 
* **tabOrder:** Usado fortemente para a sequência acessível pelo teclado na navegação de tela.

## 📄 page.json — Configuração de Página

Configurações que definem cor de fundo, tamanho do Canvas, entre outros.

```json
{
  "name": "<guid>",
  "displayName": "Nome da Página",
  "displayOption": 1,
  "height": 720, "width": 1280,
  "background": {},
  "objects": {}
}
```

## 🎯 Configurações Avançadas

### Bookmarks
Localizados no Report, em `definition/bookmarks/`.
Composição: Estado do visual (visible/hidden), estado de dados, e seleções de página.

### Slicers Sincronizados
Definidos em bloco específico para linkar fatiadores entre múltiplas páginas `syncSlicerData`.

### Tooltips
Configurações para visuais customizados. `tooltipType: "reportPage"` é usado quando uma página oculta age como tooltip de um gráfico mestre.

### Drillthrough
No visual/página de destino, é configurado para ser afetado pelo Drill, definindo as entidades de cruzamento.

## ⚠️ Limitações
- Esquemas de versão do PBI mudam; certas keys antigas de design podem ficar defasadas. Avise o usuário.
- Alguns visuais de terceiros e certificados AppSource contêm schemas imprevisíveis; lide com erros graciosamente.
