$schema = Get-Content '.\JSON_SCHEMA_PAYLOAD_PUBLICACAO_META_DL.json' | ConvertFrom-Json
$fb = Get-Content '.\PAYLOAD_EXEMPLO_POST_FACEBOOK_DL.json' | ConvertFrom-Json
$ig = Get-Content '.\PAYLOAD_EXEMPLO_POST_INSTAGRAM_DL.json' | ConvertFrom-Json
$car = Get-Content '.\PAYLOAD_EXEMPLO_CARROSSEL_DL.json' | ConvertFrom-Json

$requiredFields = $schema.required
Write-Host "=== SCHEMA VALIDATION ==="
Write-Host "Schema required fields: $($requiredFields.Count)"

foreach ($pair in @(@{name='Facebook';obj=$fb}, @{name='Instagram';obj=$ig}, @{name='Carrossel';obj=$car})) {
    $missing = @()
    $props = $pair.obj.PSObject.Properties.Name
    foreach ($f in $requiredFields) {
        if ($f -notin $props) { $missing += $f }
    }
    if ($missing.Count -eq 0) {
        Write-Host "$($pair.name): ALL $($requiredFields.Count) required fields PRESENT [OK]"
    } else {
        Write-Host "$($pair.name): MISSING $($missing.Count) fields: $($missing -join ', ')"
    }
    Write-Host "  canal=$($pair.obj.canal) | linha_dl=$($pair.obj.linha_dl) | formato=$($pair.obj.formato) | status=$($pair.obj.status_publicacao) | killcritic=$($pair.obj.status_killcritic)"
}

Write-Host ""
Write-Host "Carrossel slides: $($car.carrossel_slides.Count)"
Write-Host "FB legenda chars: $($fb.legenda_facebook.Length)"
Write-Host "IG legenda chars: $($ig.legenda_instagram.Length) (limit 2200)"
