# Dilim C - bir kalite kapisi adimini kosturur, suresini olcer, ciktisini kanit dosyasina yazar.
# Kullanim: powershell -File TST-run-step.ps1 -WorkDir <kopya> -Cmd "<komut>" -Out <kanit dosyasi> [-Turbo0]
# stdout+stderr birlikte yakalansin diye komut cmd.exe uzerinden kosar (PS 5.1'de 2>&1 native stderr'i bozar).
param(
    [Parameter(Mandatory = $true)][string]$WorkDir,
    [Parameter(Mandatory = $true)][string]$Cmd,
    [Parameter(Mandatory = $true)][string]$Out,
    [switch]$Turbo0
)

Set-Location $WorkDir
if ($Turbo0) { $env:PHPSTAN_TURBO = '0' }

$tmp = "$Out.body"
$started = Get-Date
$elapsed = Measure-Command { cmd /c "$Cmd > `"$tmp`" 2>&1" }
$exit = $LASTEXITCODE

$header = @(
    "# Komut : $Cmd",
    "# Dizin : $WorkDir",
    "# Ortam : PHPSTAN_TURBO=$($env:PHPSTAN_TURBO)",
    "# Baslangic: $($started.ToString('yyyy-MM-dd HH:mm:ss'))",
    "# Sure  : $([math]::Round($elapsed.TotalSeconds, 1)) sn (Measure-Command)",
    "# Cikis kodu: $exit",
    "# ---------------------------------------------------------------"
)
$header | Out-File -FilePath $Out -Encoding utf8
Get-Content $tmp -Encoding utf8 | Out-File -FilePath $Out -Encoding utf8 -Append
Remove-Item $tmp -Confirm:$false
"EXIT=$exit SURE=$([math]::Round($elapsed.TotalSeconds, 1))sn"
