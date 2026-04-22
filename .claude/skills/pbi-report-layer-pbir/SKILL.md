---
name: pbi-report-layer-pbir
description: Navegação, edição de páginas e visuais (PBIR), e injeção de Temas no Power BI
---

# 🎨 Skill: pbi-report-layer-pbir

A camada de interface visual (`.Report`) de um projeto PBIP é baseada inteiramente em JSON. Esta skill aborda como navegar, criar visuais, páginas e aplicar temas.

## 🛑 Pré-Condição Obrigatória

O Power BI Desktop **DEVE ESTAR FECHADO** durante a edição de qualquer arquivo `.json` nesta estrutura. A edição em tempo real causará corrupção ou sobrescrita silenciosa.

## 📂 Arquitetura do `.Report`

```
NomeProjeto.Report/
  definition/
    pages/
      <NomeDaPagina>/                ← Pasta da página (geralmente nome limpo, mas usa GUIDs internamente)
        page.json                    ← Tamanho do canvas, cor de fundo, displayName
        visuals/
          <guid>/
            visual.json              ← Definição isolada de cada gráfico/tabela
  StaticResources/
    RegisteredResources/
      <guid>/
        <guid>.json                  ← Temas customizados (Onde você deve criar novos temas)
    SharedResources/
      BaseThemes/                    ← NUNCA EDITAR (Temas nativos da Microsoft)
  report.json                        ← Metadados mestres, incluindo o themeCollection
```

## 🔎 Navegando e Localizando Elementos

* **Páginas:** Encontre as páginas varrendo os diretórios em `definition/pages/`. Leia o arquivo `page.json` para obter o campo `displayName` (o nome que o usuário realmente vê).
* **Visuais:** Se o usuário pedir para alterar "o gráfico de barras", procure com _grep_ nos arquivos `visual.json` pela propriedade `"visualType": "barChart"`. Os arquivos ficam mascarados sob GUIDs (ex: `visuals/123e4567.../visual.json`).

## 🔧 Estrutura de um `visual.json` (PBIR)

Se precisar criar do zero ou debugar um visual, ele possui a seguinte anatomia:

```json
{
  "name": "<Gere um GUID novo se estiver criando>",
  "position": {
    "x": 10, "y": 20,
    "width": 400, "height": 300,
    "tabOrder": 1
  },
  "visual": {
    "visualType": "barChart",
    "query": {
      "queryState": {
        "Category": { "projections": [...] },
        "Y": { "projections": [...] }
      }
    }
  }
}
```

*Dica:* O posicionamento obedece a um grid em pixels (X=0, Y=0 no topo-esquerdo).

## 🎨 Temas (Identidade Visual)

Para criar ou alterar o tema do dashboard:

1. **Onde criar:** Crie o arquivo JSON do tema sempre dentro de `StaticResources/RegisteredResources/<guid>/<guid>.json`. Gere o `<guid>` via comando nativo.
2. **Ativando no Projeto:** Edite o `report.json` raiz para registrar esse novo `<guid>` dentro do array `themeCollection`.
3. **Boas Práticas de Tema:** Defina um array de `dataColors` com pelo menos 8 cores (hex). Se o pedido for "padronize a fonte", use o nó `visualStyles` curinga:
   ```json
   "visualStyles": {
     "*": {
       "*": {
         "fontSize": [{ "value": 11 }],
         "fontFamily": [{ "value": "Segoe UI" }]
       }
     }
   }
   ```

## ⚠️ Limitações Importantes
* O schema visual da Microsoft muda constantemente com updates do Desktop. Keys de design mais antigas podem ser ignoradas nas versões novas.
* Avise sempre o usuário para rodar testes manuais (abrindo o arquivo) e utilizar controle de versão (Git) antes de refactors massivos de UI.
