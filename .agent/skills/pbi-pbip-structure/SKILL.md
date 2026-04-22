---
name: pbi-pbip-structure
description: Orientação espacial e navegação da estrutura de projetos PBIP do Power BI
---

# 🧭 Skill: pbi-pbip-structure

Orientação espacial dentro de um projeto PBIP. Como navegar e entender a estrutura de pastas e arquivos antes de editar TMDL ou PBIR.

## 📁 Estrutura Completa do PBIP

A estrutura básica segue este formato:

```
NomeProjeto.pbip                      ← arquivo de entrada (abre no Desktop)
NomeProjeto.SemanticModel/
  definition/
    model.tmdl
    tables/
    relationships.tmdl
    roles.tmdl
    expressions.tmdl
    cultures/
  .pbi/
    localSettings.json                ← ignorar, configurações locais
    cache.abf                         ← ignorar, cache do engine
NomeProjeto.Report/
  definition/
    pages/
      NomeDaPagina/
        page.json                     ← configurações da página
        visuals/
          <guid>/
            visual.json               ← cada visual individualmente
  .pbi/
    localSettings.json
  StaticResources/
    SharedResources/
      BaseThemes/                     ← temas base (não alterar)
      CdnResources/
    RegisteredResources/
      <guid>/                         ← recursos customizados (imagens, etc)
  report.json                         ← metadados do report
```

## 🧠 Entendendo as Camadas

### O `.SemanticModel`
Contém os dados, a lógica de negócio, e os relacionamentos. Estes arquivos `.tmdl` podem ser editados em disco (usando `pbi-tmdl-authoring`) **apenas se o Desktop estiver fechado**, ou via XMLA (usando `pbi-live-connection`) se estiver aberto.

### O `.Report`
Contém a camada visual. Os arquivos `page.json` e `visual.json` dentro das páginas formatam como os dados são apresentados. Estas edições só têm efeito quando você edita o JSON e o Desktop é reaberto (ou se atualiza o report visualmente).

* **O que você DEVE editar:** TMDLs, visual.json, page.json, temas em RegisteredResources.
* **O que você NÃO DEVE editar:** `cache.abf`, arquivos `localSettings.json`, e a pasta `BaseThemes/` (pois temas nela são nativos da Microsoft).

## 🔎 Navegando pelos Visuais e Páginas

* **Páginas:** Identifique o nome interno da página pelos GUIDs nas pastas dentro de `definition/pages/`. Para saber o displayName (o nome real que o usuário vê), verifique o `page.json`.
* **Visuais:** Como a estrutura usa GUIDs na pasta de visuais, para localizar um tipo específico (ex: barChart), você precisará fazer um _grep_ de `visualType` nos arquivos `visual.json`.

```bash
# Exemplo de busca: Encontrar todos os barCharts
grep -r '"visualType": "barChart"' ./NomeProjeto.Report/definition/pages/*/visuals/*/visual.json
```

* **Temas:** Os temas (JSON) criados ficam referenciados em `report.json` via seção `themeCollection`. Para temas customizados, eles devem ficar em `RegisteredResources/`.

## 📌 Relação entre Report e Páginas

O `report.json` é o arquivo que define propriedades mestras e a lista de páginas carregadas. Quando criar uma nova página, lembre-se que ela pode não estar listada explicitamente, mas as alterações no diretório `pages/` costumam ser varridas pelo PBI na abertura do arquivo.
