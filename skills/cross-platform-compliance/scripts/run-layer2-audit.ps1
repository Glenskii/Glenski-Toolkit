<#
File: scripts/run-layer2-audit.ps1
Updated: 2026-07-28
Change: Run the Layer 2 compliance audit from a temporary harness.

Usage:
  .\scripts\run-layer2-audit.ps1 -BaseUrl http://localhost:4173 -Paths "/,/register/"
  .\scripts\run-layer2-audit.ps1 -BaseUrl https://example.com -Browsers "chromium,firefox,webkit"
#>

[CmdletBinding()]
param(
  [Parameter(Mandatory = $true)]
  [string]$BaseUrl,

  [string]$Paths = "/",

  [string]$Browsers = "chromium",

  [int]$MaxPages = 10,

  [switch]$DiscoverLinks,

  [switch]$FailOnWarn,

  [string]$HarnessRoot = ""
)

$ErrorActionPreference = "Stop"

$skillRoot = Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")
$runnerPath = Join-Path $skillRoot "scripts\compliance-audit.spec.js"

if (-not (Test-Path -LiteralPath $runnerPath)) {
  throw "Missing runner: $runnerPath"
}

if ([string]::IsNullOrWhiteSpace($HarnessRoot)) {
  $safeName = "glenski-compliance-audit-" + (Get-Date -Format "yyyyMMdd-HHmmss")
  $HarnessRoot = Join-Path $env:TEMP $safeName
}

New-Item -ItemType Directory -Path $HarnessRoot -Force | Out-Null
Copy-Item -LiteralPath $runnerPath -Destination (Join-Path $HarnessRoot "compliance-audit.spec.js") -Force

Push-Location -LiteralPath $HarnessRoot
try {
  if (-not (Test-Path -LiteralPath "package.json")) {
    npm init -y | Out-Null
  }

  npm install --save-dev @playwright/test @axe-core/playwright

  $browserList = $Browsers.Split(",") | ForEach-Object { $_.Trim() } | Where-Object { $_ }
  if ($browserList.Count -eq 0) {
    $browserList = @("chromium")
  }

  npx playwright install $browserList

  $env:BASE_URL = $BaseUrl
  $env:AUDIT_PATHS = $Paths
  $env:AUDIT_BROWSERS = ($browserList -join ",")
  $env:AUDIT_MAX_PAGES = [string]$MaxPages
  $env:AUDIT_DISCOVER_LINKS = if ($DiscoverLinks) { "1" } else { "0" }
  $env:COMPLIANCE_FAIL_ON_WARN = if ($FailOnWarn) { "1" } else { "0" }

  npx playwright test --reporter=list --workers=1
}
finally {
  Pop-Location
}
