<#
.SYNOPSIS
    Выполняет команду на VPS сервере через SSH.
.DESCRIPTION
    Скрипт для удалённого выполнения команд на Jino VPS.
    Используется Copilot для автоматического деплоя и администрирования.
.PARAMETER Command
    Команда для выполнения на сервере.
.EXAMPLE
    .\scripts\ssh-vps.ps1 "docker ps"
    .\scripts\ssh-vps.ps1 "cd /opt/school-site && docker compose up -d"
#>
param(
    [Parameter(Mandatory=$true)]
    [string]$Command
)

# ── Конфигурация VPS ──
# Заполни эти значения своими данными:
$VPS_HOST = $env:VPS_HOST
$VPS_USER = $env:VPS_USER
$VPS_PORT = if ($env:VPS_PORT) { $env:VPS_PORT } else { "22" }
$VPS_KEY  = $env:VPS_KEY  # путь к приватному SSH-ключу (опционально)

# Проверка
if (-not $VPS_HOST -or -not $VPS_USER) {
    Write-Error @"
VPS credentials not configured!

Set environment variables:
  `$env:VPS_HOST = 'YOUR_VPS_IP'
  `$env:VPS_USER = 'root'
  `$env:VPS_PORT = '22'         # optional, default 22
  `$env:VPS_KEY  = 'C:\Users\...\\.ssh\id_rsa'  # optional

Or create g:\Projects\school-project\scripts\vps-env.ps1 with these values.
"@
    exit 1
}

# Собираем SSH-команду
$sshArgs = @(
    "-o", "StrictHostKeyChecking=no",
    "-o", "ConnectTimeout=10",
    "-p", $VPS_PORT
)

if ($VPS_KEY) {
    $sshArgs += @("-i", $VPS_KEY)
}

$sshArgs += @("${VPS_USER}@${VPS_HOST}", $Command)

Write-Host "──── SSH: ${VPS_USER}@${VPS_HOST}:${VPS_PORT} ────" -ForegroundColor Cyan
Write-Host "CMD: $Command" -ForegroundColor DarkGray
Write-Host ""

# Выполняем
& ssh @sshArgs
$exitCode = $LASTEXITCODE

if ($exitCode -ne 0) {
    Write-Host "" 
    Write-Host "SSH command failed with exit code $exitCode" -ForegroundColor Red
}

exit $exitCode
