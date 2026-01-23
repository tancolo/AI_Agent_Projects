Add-Type -AssemblyName System.Drawing

$imagePath = "D:\Dev-Env\Antigravity_Projects\mapleway\logo_selection\logo_web_extension_mapleway.png"
$bitmap = [System.Drawing.Bitmap]::FromFile($imagePath)

$colors = @{}

# Sample pixels
for ($x = 0; $x -lt $bitmap.Width; $x += 5) {
    for ($y = 0; $y -lt $bitmap.Height; $y += 5) {
        $pixel = $bitmap.GetPixel($x, $y)
        
        # Check Alpha (not transparent)
        if ($pixel.A -gt 50) {
            # Check if NOT white (R, G, B all > 240 is basically white)
            if ($pixel.R -lt 240 -or $pixel.G -lt 240 -or $pixel.B -lt 240) {
                $hex = "#{0:X2}{1:X2}{2:X2}" -f $pixel.R, $pixel.G, $pixel.B
                if ($colors.ContainsKey($hex)) {
                    $colors[$hex]++
                } else {
                    $colors[$hex] = 1
                }
            }
        }
    }
}

$bitmap.Dispose()

# Output top 10 non-white colors
Write-Output "--- Non-White Colors ---"
$colors.GetEnumerator() | Sort-Object Value -Descending | Select-Object -First 10 | ForEach-Object {
    Write-Output "Color: $($_.Key) - Count: $($_.Value)"
}
