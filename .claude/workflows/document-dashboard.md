---
name: document-dashboard
description: Gera automaticamente documentação completa do projeto PBIP em Markdown.
---

# 📚 Workflow: /document-dashboard

**Comando:** `/document-dashboard [caminho/do/projeto.pbip] [--output caminho/saida.md]`

Elimina a necessidade manual de se manter catálogos de dados e metadados sobre modelos do Power BI, orquestrando um parse massivo no modelo semântico e visual gerando output em formato Markdown puro.

Default output file: `DASHBOARD_DOC.md` na raiz do projeto analisado.

## 🔄 Passos do Fluxo

### 1. Orientação e Inventário
Utilizando o skill `pbi-pbip-structure`, levanta dados quantitativos base (Número de tabelas, medidas, relações, páginas e gráficos).

### 2. Parsers de Fonte
O agente precisa coletar metadados ativamente de duas frentes do PBIP:
1. **Dados do Semantic Model (`.tmdl`):** Extrai nome, data types, `description`, `expressions` e a topologia de ligações na pasta `relationships.tmdl`.
2. **Dados do Report (`.json`):** Vasculha os `pages/*/visuals/*/visual.json`. Procura pelas chaves de identificação (tipo de visual), titulo (se existente nas propriedades) e os campos/medidas utilizados (olhando para a array de `projections`).

### 3. Geração Documental
Utiliza a skill-mãe `pbi-dashboard-documentation` para compilar todo esse dado de parser em um markdown fluído com as sessões essenciais de uma governança enxuta.
A documentação final deve conter pelo menos:
1. Resumo e Visão Geral.
2. Data Dictionary de tabelas referenciadas.
3. Listagem de Medidas formatadas com DAX code-block.
4. Mapa de Referência Visual → Medida → Coluna por Página.
5. Diagrama Relacional (Listagem simples com Tabelas, Direção e Cardinalidade).

### 4. Resumo e Entrega
Após salvar o arquivo `DASHBOARD_DOC.md`, informe na conversa:
* Local e sucesso na salvaguarda do arquivo.
* A porcentagem geral (cobertura) de documentação (Tabelas e Medidas contendo descrições vs O Total).
* **Se a cobertura for inferior a 80%:** Aconselhe rodar o workflow `/validate-pbi` para evidenciar os gargalos onde o dicionário estagnou ou ofereça ajuda para documentar (adicionar DAX comment / desc) via TMDL.
