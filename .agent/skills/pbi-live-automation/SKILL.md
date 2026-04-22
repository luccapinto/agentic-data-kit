---
name: pbi-live-automation
description: Automação, testes DAX e conexão ao vivo via TOM e ADOMD.NET em PowerShell
---

# 🔌 Skill: pbi-live-automation

Ensina o agente a descobrir, conectar, operar o Analysis Services local do PBI Desktop e realizar testes automatizados DAX via TOM e ADOMD.NET em PowerShell.

## 🎯 1. Quando usar esta skill

* **Sempre que o pedido envolver** adicionar, editar ou remover medidas, colunas calculadas, relações, hierarquias ou papéis de segurança — **e o PBI Desktop estiver aberto com o arquivo.**
* Quando o usuário quiser **testar DAX** contra o modelo real para validar o funcionamento da medida.
* Quando precisar enumerar o estado atual do modelo (listar medidas, tabelas, relações).
* **NÃO USAR quando:** Desktop estiver fechado (usar `pbi-semantic-layer-tmdl`), modelo remoto/thin report.

## 🛑 2. Pré-condição obrigatória

Antes de qualquer operação, você **DEVE CONFIRMAR** se o PBI Desktop está aberto com o `.pbip` correto.

Script de verificação: ler `%LOCALAPPDATA%\Microsoft\Power BI Desktop\AnalysisServicesWorkspaces\` e listar instâncias ativas. Se estiver vazio, pare e avise o usuário.

## 🔍 3. Descoberta de Porta

O Desktop roda o Analysis Services numa porta aleatória. Descubra a porta via PowerShell:

```powershell
$workspacePath = "$env:LOCALAPPDATA\Microsoft\Power BI Desktop\AnalysisServicesWorkspaces"
$portFile = Get-ChildItem -Path $workspacePath -Recurse -Filter "msmdsrv.port.txt" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
$port = Get-Content $portFile.FullName
Write-Host "Porta: $port"
```
*Se houver múltiplos arquivos, liste para o usuário escolher o correto.*

## 📦 4. Carregamento das DLLs (AMO e ADOMD)

Carregue as bibliotecas do AMO e ADOMD via PowerShell:

```powershell
Add-Type -Path ".\bin\amo\Microsoft.AnalysisServices.Tabular.dll" -ErrorAction Stop
Add-Type -Path ".\bin\adomd\Microsoft.AnalysisServices.AdomdClient.dll" -ErrorAction Stop
```

**Se as DLLs não existirem**, pare e peça ao usuário para rodar o bootstrap:
> `powershell -ExecutionPolicy Bypass -File .\bin\bootstrap.ps1`

## 🛠️ 5. Padrões de Conexão TOM (Edição de Modelo)

```powershell
$server = New-Object Microsoft.AnalysisServices.Tabular.Server
try {
    $server.Connect("Data Source=localhost:$port")
    $db = $server.Databases[0]
    $model = $db.Model
    
    # Exemplo: Editar Medida
    # $measure = $model.Tables["Tabela"].Measures["MinhaMedida"]; $measure.Expression = "NovaExpressao"
    # $model.SaveChanges()
} finally {
    $server.Disconnect()
}
```

## 🧪 6. Testes DAX via ADOMD (Validação)

Após editar o modelo, você pode rodar testes DAX (Sanidade, Granularidade, Non-blank) via ADOMD:

```powershell
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:$port")
try {
    $conn.Open()
    $cmd = $conn.CreateCommand()
    
    # Teste 1: Sanidade Básica
    $cmd.CommandText = "EVALUATE ROW(""Resultado"", [SuaMedida])"
    
    # Teste 2: Granularidade (Agrupamento)
    # $cmd.CommandText = "EVALUATE SUMMARIZECOLUMNS(Tabela[Dimensao], ""Valor"", [SuaMedida]) ORDER BY [Valor] DESC"
    
    $reader = $cmd.ExecuteReader()
    while ($reader.Read()) { Write-Host $reader[0] }
} finally {
    if ($conn.State -eq 'Open') { $conn.Close() }
}
```

## 🔄 7. Fluxo Padrão
1. Confirmar Desktop aberto e arquivo correto.
2. Descobrir a porta ativa.
3. Carregar DLLs e Conectar.
4. Realizar edição via TOM (`$model.SaveChanges()`).
5. Se sucesso: rodar DAX de sanidade via ADOMD para garantir validade matemática.
6. Desconectar e informar o usuário para salvar (`Ctrl+S`).

## 📁 8. Regras de Criação de Arquivos (PS1 Encoding)

Sempre que criar scripts `.ps1` ou arquivos que contenham caracteres especiais (emojis, acentos), **VOCÊ DEVE** garantir que o arquivo seja salvo em **UTF-8 com BOM**.

O Windows PowerShell 5.1 interpreta arquivos `.ps1` sem BOM como `Windows-1252` (ANSI). Como consequência, qualquer emoji ou caractere especial dentro de uma string causará erro de parse.

**Como salvar corretamente via PowerShell:**
```powershell
$content | Out-File -FilePath "script.ps1" -Encoding utf8
```
*(Nota: No PS 5.1, `-Encoding utf8` força o BOM. No PS 7+, o padrão já é UTF-8 sem BOM e ele entende ambos.)*
