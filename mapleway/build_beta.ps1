$version = "v0.1"
$projectRoot = "D:\Dev-Env\Antigravity_Projects\mapleway"
$sourceDir = "$projectRoot\codebase\VanillaJS"
$distDir = "$projectRoot\dist"
$tempDir = "$distDir\MapleWay_Beta_$version"
$zipPath = "$distDir\MapleWay_Beta_$version.zip"

# Clean previous build
if (Test-Path $distDir) {
    Remove-Item $distDir -Recurse -Force
}
New-Item -ItemType Directory -Path $tempDir -Force | Out-Null

Write-Host "🚧 Building MapleWay Beta $version..." -ForegroundColor Cyan

# Files/Folders to INclude
$includes = @(
    "manifest.json",
    "popup",
    "scripts",
    "icons"
)

# Copy Files
foreach ($item in $includes) {
    $srcPath = "$sourceDir\$item"
    $destPath = "$tempDir\$item"
    
    if (Test-Path $srcPath) {
        Write-Host "   Copying $item..."
        Copy-Item -Path $srcPath -Destination $destPath -Recurse
    } else {
        Write-Warning "   Missing expected file/folder: $item"
    }
}

# Copy Instructions (will be created in root next)
# Copy Instructions
Copy-Item "$projectRoot\instruction_docs\TESTER_INSTRUCTIONS.md" -Destination "$tempDir\READ_ME.md"

# Find and Copy Chinese Instructions (Fallback: Find any other TESTER instruction file)
$allGuides = Get-ChildItem "$projectRoot\instruction_docs" -Filter "TESTER_INSTRUCTIONS*.md"
$cnFile = $allGuides | Where-Object { $_.Name -ne "TESTER_INSTRUCTIONS.md" } | Select-Object -First 1

if ($cnFile) {
    Write-Host "   Copying Chinese Guide: $($cnFile.Name)..."
    Copy-Item $cnFile.FullName -Destination "$tempDir\READ_ME_CN.md"
} else {
    Write-Warning "   ❌ Chinese guide NOT found!"
}

# FIX: Update Image Paths in Instructions for Zip structure
# Repo Path: ./codebase/VanillaJS/icons/...
# Zip Path:  ./icons/...
$readmeFiles = @("$tempDir\READ_ME.md", "$tempDir\READ_ME_CN.md")
foreach ($file in $readmeFiles) {
    if (Test-Path $file) {
        (Get-Content $file -Encoding UTF8) -replace '\./codebase/VanillaJS/icons/', './icons/' | Set-Content $file -Encoding UTF8
    }
}

# Create ZIP
Write-Host "📦 Zipping package..."
Compress-Archive -Path "$tempDir\*" -DestinationPath $zipPath

# Cleanup Temp
Remove-Item $tempDir -Recurse -Force

Write-Host "✅ Build Complete!" -ForegroundColor Green
Write-Host "   Zip File: $zipPath"
