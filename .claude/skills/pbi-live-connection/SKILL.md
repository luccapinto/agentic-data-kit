---
name: pbi-live-connection
description: Conexão e edição ao vivo do modelo semântico do Power BI via TOM e ADOMD.NET em PowerShell
---

# 🔌 Skill: pbi-live-connection

Ensina o agente a descobrir, conectar e operar o Analysis Services local do PBI Desktop via TOM e ADOMD.NET em PowerShell.

## 🎯 1. Quando usar esta skill

* **Sempre que o pedido envolver** adicionar, editar ou remover medidas, colunas calculadas, relações, tabelas calculadas, grupos de cálculo, hierarquias ou papéis de segurança — **e o PBI Desktop estiver aberto com o arquivo.**
* Quando o usuário quiser testar DAX contra o modelo real.
* Quando precisar enumerar o estado atual do modelo (listar medidas, tabelas, relações).
* **NÃO USAR quando:** Desktop estiver fechado (usar `pbi-tmdl-authoring`), modelo remoto/thin report, operações de Power Query / passos M.

## 🛑 2. Pré-condição obrigatória

Antes de qualquer operação, você **DEVE CONFIRMAR** se o PBI Desktop está aberto com o `.pbip` correto.

Script de verificação: ler `%LOCALAPPDATA%\Microsoft\Power BI Desktop\AnalysisServicesWorkspaces\` e listar instâncias ativas. Se estiver vazio ou for o arquivo errado, **pare imediatamente** e avise o usuário.

## 🔍 3. Descoberta de Porta

O Desktop roda o Analysis Services numa porta aleatória. Como descobrir a porta usando PowerShell:

```powershell
$workspacePath = "$env:LOCALAPPDATA\Microsoft\Power BI Desktop\AnalysisServicesWorkspaces"
$portFile = Get-ChildItem -Path $workspacePath -Recurse -Filter "msmdsrv.port.txt" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
$port = Get-Content $portFile.FullName
Write-Host "Porta: $port"
```

*Se houver múltiplos arquivos, liste para o usuário e peça que ele escolha qual o modelo correto.*

## 📦 4. Carregamento das DLLs

Carregue as bibliotecas do AMO e ADOMD via PowerShell usando os assemblies baixados localmente na pasta `bin`:

```powershell
Add-Type -Path ".\bin\amo\Microsoft.AnalysisServices.Tabular.dll" -ErrorAction Stop
Add-Type -Path ".\bin\adomd\Microsoft.AnalysisServices.AdomdClient.dll" -ErrorAction Stop
```

**Se as DLLs não existirem**, um erro será gerado. Nesse caso, **pare e peça ao usuário** para rodar o bootstrap:

> "Para conectar ao Power BI Desktop, preciso de algumas bibliotecas da Microsoft que ainda não estão na sua máquina. É uma instalação única — depois disso nunca mais precisará fazer. Execute o comando abaixo no terminal e me avise quando terminar:
> `powershell -ExecutionPolicy Bypass -File .\bin\bootstrap.ps1`"

## 🛠️ 5. Padrões de Conexão TOM

Conecte ao servidor usando a porta descoberta:

```powershell
$server = New-Object Microsoft.AnalysisServices.Tabular.Server
try {
    $server.Connect("localhost:$port")
    $db = $server.Databases[0]
    $model = $db.Model
    
    # Realizar operações
    
} finally {
    $server.Disconnect()
}
```
*Dica: Timeout recomendado é 60000ms. Sempre use try/finally com Disconnect().*

## ⚙️ 6. Padrões de Operação

Como interagir com o `$model`:

* **Adicionar Medida:** `$table.Measures.Add((New-Object Microsoft.AnalysisServices.Tabular.Measure -Property @{Name="MinhaMedida"; Expression="SUM(Tabela[Coluna])"}))` → `$model.SaveChanges()`
* **Modificar Medida:** `$measure = $table.Measures["MinhaMedida"]; $measure.Expression = "NovaExpressao"` → `$model.SaveChanges()`
* **Remover Objeto:** `$table.Measures.Remove("MinhaMedida")` → `$model.SaveChanges()`
* **Criar Relação:** `$model.Relationships.Add(...)` → `$model.SaveChanges()`

Sempre capture exceções `Microsoft.AnalysisServices.OperationException` e retorne mensagens legíveis. Os erros retornados virão diretamente do Engine do Analysis Services (ex: erro sintático de DAX).

## 🧪 7. Consulta DAX via ADOMD

Você pode rodar consultas DAX usando a string de conexão na mesma porta:

```powershell
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:$port")
try {
    $conn.Open()
    $cmd = $conn.CreateCommand()
    $cmd.CommandText = "EVALUATE ROW(""Resultado"", [SuaMedida])"
    $reader = $cmd.ExecuteReader()
    while ($reader.Read()) { Write-Host $reader[0] }
} finally {
    if ($conn.State -eq 'Open') { $conn.Close() }
}
```

## 🚨 8. Erros Comuns e Como Tratar

* `msmdsrv.port.txt` não encontrado → Desktop não está aberto, ou PBIP não foi aberto via Desktop.
* Múltiplos `port.txt` → Múltiplos arquivos PBI abertos, pedir usuário escolher.
* `OperationException: The expression refers to...` → Referência inválida no DAX, corrigir a expressão de acordo com a validação do engine e tentar salvar de novo.
* `Cannot connect to localhost` → msmdsrv travou, pedir para o usuário fechar e reabrir o Desktop.
* DLL `Add-Type` falha → O script de bootstrap não foi rodado, execute `.\bin\bootstrap.ps1`.

## 🔄 9. Fluxo Padrão

1. Confirmar Desktop aberto com o arquivo correto.
2. Descobrir a porta ativa.
3. Carregar DLLs.
4. Conectar.
5. Realizar operação(ões) via TOM (`$model.SaveChanges()`).
6. Se sucesso: rodar DAX de sanidade via ADOMD (usando a skill `pbi-dax-testing`).
7. Desconectar.
8. Informar usuário: *"Mudança aplicada — veja no Desktop. Salve com Ctrl+S se aprovar."*
