---
name: pbi-quality-rules
description: Mecanismo de validação de qualidade de modelos Power BI executado via PowerShell/TOM.
---

# 🛡️ Skill: pbi-quality-rules

Substituto funcional do Best Practice Analyzer (BPA) do Tabular Editor. Permite ao agente validar o modelo contra regras declarativas de qualidade contidas em YAML.

## 📝 A Abordagem

O BPA do Tabular Editor é o padrão da indústria, mas requer o TE instalado. No Agentic Data Kit, processamos essas mesmas regras através de:
1. O arquivo `.agent/skills/pbi-quality-rules/pbi-quality-rules.yaml` carregado como base de conhecimento.
2. Uso de PowerShell e `pbi-live-connection` (TOM local) ou parsing offline de TMDL para validar essas regras em loop.

## 📊 Estrutura e Parsing (Como o Agente Executa)

Quando solicitado para rodar o check de qualidade:

1. Carregue o modelo via `pbi-live-connection` ou parsing de `TMDL`.
2. Parseie e carregue o YAML em `pbi-quality-rules.yaml`.
3. Para cada regra no YAML:
    * Se `applies_to` é `measure`, itere sobre as Measures do TOM.
    * Valide a condição PowerShell da propriedade `check`. Por exemplo `Name -cnotmatch '^[A-Z]'`.
4. Capture o array de violações com `{id, severity, object_name, message}`.
5. Formate as violações para o usuário (omitindo `info` a não ser que pedido).

### Categorias de Regras
1. **Nomeação:** Títulos e propriedades base. (Ex: Primeira letra maiúscula).
2. **DAX:** Eficiência das expressões. (Ex: Measures com BLANK() ou falta de comentários).
3. **Modelo / Relacionamentos:** Bidirecionais desnecessários, island tables.
4. **Performance:** Auto-DateTime ativado, Colunas de alta cardinalidade não essenciais.
5. **Documentação:** Presença mandatória da tag `description`.

## ⚙️ Exemplo de Script de Execução

Se você estiver em modo PowerShell interativo, a validação de regras ocorre mais ou menos assim:

```powershell
$rulesYaml = Get-Content ".\.agent\skills\pbi-quality-rules\pbi-quality-rules.yaml" | ConvertFrom-Yaml
# Iterate
foreach ($rule in $rulesYaml.rules) {
   if ($rule.applies_to -eq "measure") {
       foreach ($measure in $table.Measures) {
           $violation = Invoke-Expression $rule.check
           if ($violation) { Write-Host "[$($rule.id)] $($measure.Name) - $($rule.description)" }
       }
   }
}
```

## 🔄 Fluxo do Agente
1. Rode automaticamente após as grandes sessões de edição e refatorações de modelo semântico.
2. Apresente ao usuário os `error` e `warning` apenas.
3. Se o erro for `[error]`, ofereça correção imediata. Se for `[warning]`, sugira, mas não obrigue.
