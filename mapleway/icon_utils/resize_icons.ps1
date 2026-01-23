Add-Type -AssemblyName System.Drawing

$sourcePath = "D:\Dev-Env\Antigravity_Projects\mapleway\logo_selection\logo_web_extension_mapleway.png"
$targetDir = "D:\Dev-Env\Antigravity_Projects\mapleway\codebase\VanillaJS\icons"

if (-not (Test-Path $targetDir)) {
    New-Item -ItemType Directory -Path $targetDir -Force
}

function Resize-Image {
    param([string]$Src, [string]$Dest, [int]$Size)
    
    try {
        $srcImage = [System.Drawing.Bitmap]::FromFile($Src)
        $destImage = new-object System.Drawing.Bitmap $Size, $Size
        
        $graphics = [System.Drawing.Graphics]::FromImage($destImage)
        $graphics.CompositingQuality = [System.Drawing.Drawing2D.CompositingQuality]::HighQuality
        $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
        $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
        
        $graphics.DrawImage($srcImage, 0, 0, $Size, $Size)
        
        $destImage.Save($Dest, [System.Drawing.Imaging.ImageFormat]::Png)
        
        Write-Host "Created $Dest"
    }
    catch {
        Write-Error "Failed to resize $Dest : $_"
    }
    finally {
        if ($srcImage) { $srcImage.Dispose() }
        if ($destImage) { $destImage.Dispose() }
        if ($graphics) { $graphics.Dispose() }
    }
}

Resize-Image -Src $sourcePath -Dest "$targetDir\icon16.png" -Size 16
Resize-Image -Src $sourcePath -Dest "$targetDir\icon48.png" -Size 48
Resize-Image -Src $sourcePath -Dest "$targetDir\icon128.png" -Size 128
