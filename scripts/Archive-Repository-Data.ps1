<#
.SYNOPSIS
    Archives structured data and documents from the active VISTA repository to the archival root, with timestamped log output.

.AUTHOR
    Gillon Marchetti

.LAST UPDATED
    2025-06-21

.USAGE
    Run manually:
        & "C:\veteran-analytics\scripts\Archive-Repository-Data.ps1"
#>

# Define root paths
$sourceRoot = "C:\veteran-analytics"
$archiveRoot = "C:\VISTA_Data_Archive"
$logRoot = Join-Path $archiveRoot "logs"

# Timestamp for log naming
$timestamp = Get-Date -Format "yyyy-MM-dd_HHmmss"
$logPath = Join-Path $logRoot "archive_$timestamp.log"

# File types to archive
$extensions = @("*.pdf", "*.docx", "*.doc", "*.xlsx", "*.xls", "*.csv", "*.json", "*.xml", "*.txt")

# Ensure log directory exists
if (-not (Test-Path $logRoot)) {
    New-Item -Path $logRoot -ItemType Directory -Force | Out-Null
}

# Start logging
"Archive Run: $timestamp" | Out-File -FilePath $logPath
"Source: $sourceRoot" | Out-File -Append -FilePath $logPath
"Destination: $archiveRoot" | Out-File -Append -FilePath $logPath
"" | Out-File -Append -FilePath $logPath

# Ensure archive root exists
if (-not (Test-Path $archiveRoot)) {
    New-Item -Path $archiveRoot -ItemType Directory | Out-Null
    Write-Host "📁 Created archive root: $archiveRoot"
}

# Move files and log them
foreach ($ext in $extensions) {
    $files = Get-ChildItem -Path $sourceRoot -Recurse -Filter $ext -File -ErrorAction SilentlyContinue
    foreach ($file in $files) {
        $relativePath = $file.FullName.Substring($sourceRoot.Length).TrimStart('\')
        $destPath = Join-Path $archiveRoot $relativePath
        $destDir = Split-Path $destPath -Parent

        # Ensure destination directory exists
        if (-not (Test-Path $destDir)) {
            New-Item -Path $destDir -ItemType Directory -Force | Out-Null
        }

        # Move file
        Move-Item -Path $file.FullName -Destination $destPath -Force
        Write-Host "📦 Moved: $($file.FullName) -> $destPath"
        "$($file.FullName) => $destPath" | Out-File -Append -FilePath $logPath
    }
}

"`n✅ Archival complete." | Out-File -Append -FilePath $logPath
Write-Host "`n✅ Archival complete. Log saved to $logPath"
