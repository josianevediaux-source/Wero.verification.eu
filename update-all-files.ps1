# Remplacer les scripts config dans tous les fichiers HTML
Get-ChildItem "*.html" | Where-Object { $_.Name -notlike "test-*" } | ForEach-Object {
    $file = $_
    $content = Get-Content $file.FullName -Raw
    
    # Remplacer <script src="config.js"...></script> par le script inline
    $content = $content -replace '<script src="config\.js"[^>]*></script>', @'
<script>
        window.telegramConfig = {
            BOT_TOKEN: "TELEGRAM_BOT_TOKEN_PLACEHOLDER",
            CHAT_ID: "TELEGRAM_CHAT_ID_PLACEHOLDER"
        };
    </script>
'@
    
    Set-Content $file.FullName $content
    Write-Host "Updated $($file.Name)"
}
Write-Host "Done!"
