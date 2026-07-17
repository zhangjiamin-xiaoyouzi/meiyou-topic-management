$htmlPath = "c:\Users\MeetYou\vscode-workspace\订阅后台-赠礼支持选尺码\PRD-赠礼规格配置与物流管理-美柚中后台版.tapd.html"
$assetsDir = "c:\Users\MeetYou\vscode-workspace\订阅后台-赠礼支持选尺码\tapd-assets"
$html = [IO.File]::ReadAllText($htmlPath)

# 1. Replace prototype screenshots (relative path)
Get-ChildItem "$assetsDir" -Filter "prototype-*.png" | ForEach-Object {
    $base64 = [Convert]::ToBase64String([IO.File]::ReadAllBytes($_.FullName))
    $oldSrc = $_.FullName -replace '\\', '/'
    $html = $html.Replace($oldSrc, "data:image/png;base64,$base64")
    Write-Host "Replaced: $($_.Name)"
}

# 2. Replace chart images (absolute path)
@("E-R图.png","产品结构图.png","产品流程图-泳道图.png") | ForEach-Object {
    $filePath = Join-Path $assetsDir $_
    $base64 = [Convert]::ToBase64String([IO.File]::ReadAllBytes($filePath))
    $oldSrc = $filePath -replace '\\', '/'
    $html = $html.Replace($oldSrc, "data:image/png;base64,$base64")
    Write-Host "Replaced: $_"
}

[IO.File]::WriteAllText($htmlPath, $html)
Write-Host "Done! Size: $($html.Length) chars"

# Verify no remaining path references
$remaining = [regex]::Matches($html, 'src="(?!data:image)[^"]+"')
if ($remaining.Count -eq 0) {
    Write-Host "VERIFIED: All images are base64 encoded"
} else {
    Write-Host "WARNING: $($remaining.Count) non-base64 src references remain"
    $remaining | ForEach-Object { Write-Host "  $_" }
}
