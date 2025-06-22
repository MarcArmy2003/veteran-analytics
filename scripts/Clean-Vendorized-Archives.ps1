<#
.SYNOPSIS
    Scans and removes third-party archive files (e.g., .tar.gz, .whl, .zip) from the local veteran-analytics repository.

.DESCRIPTION
    Deletes files that should not be version-controlled (e.g., vendorized packages) and logs all deletions.

.AUTHOR
    Gillon Marchetti

.LAST UPDATED
    2025-06-21
#>

$repoPath = "C:\veteran-analytics"
$logDir = "C:\VISTA_Data_Archive\logs"
$timestamp = Get-Date -Format "yyyy-MM-dd_HHmmss"
$logPath = Join-Path $logDir "vendor_cleanup_$timestamp.log"

# Archive patterns to remove
$patterns = @("*.tar.gz", "*.zip", "*.whl", "*.tgz", "*.tar", "*.egg")

# Ensure log directory exists
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

"Vendor Cleanup Log - $timestamp" | Out-File -FilePath $logPath
"Repository: $repoPath" | Out-File -Append -FilePath $logPath
"" | Out-File -Append -FilePath $logPath

foreach ($pattern in $patterns) {
    Get-ChildItem -Path $repoPath -Recurse -Include $pattern -File -ErrorAction SilentlyContinue | ForEach-Object {
        Write-Host "🗑️ Removing: $($_.FullName)"
        "$($_.FullName)" | Out-File -Append -FilePath $logPath
        Remove-Item -Path $_.FullName -Force
    }
}

"`n✅ Cleanup complete. Log saved to: $logPath" | Out-File -Append -FilePath $logPath
Write-Host "`n✅ Cleanup complete. Log saved to: $logPath"
