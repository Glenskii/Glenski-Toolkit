[CmdletBinding()]
param(
    [string]$TaskName = "InboxGuardianService",
    [ValidateRange(5, 1440)]
    [int]$IntervalMinutes = 15,
    [switch]$Uninstall
)

$ErrorActionPreference = "Stop"
$scriptsDirectory = Split-Path -Parent $PSCommandPath
$skillDirectory = Split-Path -Parent $scriptsDirectory
$launcher = Join-Path $scriptsDirectory "run_silent.vbs"
$pythonWindowless = Join-Path $skillDirectory ".venv\Scripts\pythonw.exe"

if ($Uninstall) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
    Write-Host "Removed scheduled task: $TaskName"
    exit 0
}

if (-not (Test-Path -LiteralPath $launcher)) {
    throw "Missing silent launcher: $launcher"
}
if (-not (Test-Path -LiteralPath $pythonWindowless)) {
    throw "Missing virtual-environment pythonw.exe. Run the Windows setup steps first."
}

$action = New-ScheduledTaskAction -Execute "wscript.exe" -Argument "`"$launcher`"" -WorkingDirectory $skillDirectory
$startTime = (Get-Date).AddMinutes(1)
$trigger = New-ScheduledTaskTrigger -Once -At $startTime -RepetitionInterval (New-TimeSpan -Minutes $IntervalMinutes)
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -MultipleInstances IgnoreNew

Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Settings $settings -Description "Local Inbox Guardian background sweep" -Force | Out-Null
Write-Host "Installed $TaskName. It runs silently every $IntervalMinutes minutes while Windows is awake."
