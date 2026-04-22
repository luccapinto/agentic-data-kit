---
name: pbi-theme-design
description: Criação e edição do arquivo JSON de tema do Power BI (paleta, formatação e consistência)
---

# 🎨 Skill: pbi-theme-design

O tema é a camada de identidade visual de um dashboard. Um arquivo JSON de tema bem definido elimina a necessidade de formatação manual visual a visual.

## 📁 Onde fica o tema no PBIP

Os temas ficam em:
```
NomeProjeto.Report/
  StaticResources/
    SharedResources/
      BaseThemes/
        CY24SU06.json       ← tema base do Desktop (NÃO EDITAR)
    RegisteredResources/
      <guid>/
        <guid>.json         ← tema customizado (AQUI o agente edita)
```

O arquivo customizado é então referenciado em `report.json` via seção `resourcePackage`.

## 🧠 Schema do Tema Power BI

Abaixo um exemplo funcional do schema do Power BI para temas:

```json
{
  "name": "NomeDoTema",
  "dataColors": ["#2B5B84", "#F48C42", "#4B90A6", "#EBC05B", "#99A9B4", "#D85B5B", "#5C9975", "#B8B8B8"], 
  "background": "#FFFFFF",
  "foreground": "#333333",
  "tableAccent": "#2B5B84",
  "visualStyles": {
    "*": {
      "*": {
        "fontSize": [{ "value": 11 }],
        "fontFamily": [{ "value": "Segoe UI" }]
      }
    },
    "barChart": {
      "*": {
        "dataPoint": [{ "fill": { "solid": { "color": "#2B5B84" } } }]
      }
    }
  },
  "textClasses": {
    "label": { "fontSize": 9, "color": "#666666" },
    "title": { "fontSize": 14, "fontBold": true, "color": "#111111" }
  }
}
```

## 🎯 O que a skill deve cobrir

### 1. Paleta de cores (`dataColors`)
* Use uma array com pelo menos 8 hexadecimais (o PBI cicla neles na ordem).
* Para design semântico, certifique-se de configurar cores de positive/negative/neutral quando o usuário pedir (em `good`, `bad`, `neutral` sob propriedades como KPI).

### 2. Formatação padrão (`visualStyles`)
* Curinga `"*"`: `{"*": {"*": {...}}}` aplica para todos os visuais, e estado padrão, útil para resetar propriedades master de fontes.
* Tipos visuais específicos (`barChart`, `lineChart`, `card`, `tableEx`).
* Propriedades suportadas: `fontSize`, `fontFamily`, `fontBold`, `background`, `border`, `dataPoint`.

### 3. Classes de Texto (`textClasses`)
* `label`: Usado em eixos e rótulos de dados.
* `title`: Títulos dos visuais e páginas.
* `header`: Cabeçalho de colunas de matriz/tabela.
* `callout`: Valor de destaquem de Cards.

### 4. Aplicar Tema ao Report
Quando criar um arquivo de tema em `RegisteredResources`, certifique-se que o UUID bate com o registrado na seção `themeCollection` em `report.json`.

## ✅ Boas Práticas

* Sempre defina pelo menos 8 `dataColors`.
* Teste constraste mínimo (WCAG AA).
* **NUNCA** sobrescreva temas em `BaseThemes/` pois eles são controlados pelo Desktop. Crie sempre em `RegisteredResources/`.
