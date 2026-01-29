$port = 8000
$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://localhost:$port/")
$listener.Start()

Write-Host "Server listening at http://localhost:$port/"
Write-Host "Press Ctrl+C to stop."

function Get-MimeType($file) {
    switch ([System.IO.Path]::GetExtension($file).ToLower()) {
        ".html" { return "text/html" }
        ".css"  { return "text/css" }
        ".js"   { return "application/javascript" }
        ".png"  { return "image/png" }
        ".jpg"  { return "image/jpeg" }
        ".jpeg" { return "image/jpeg" }
        ".gif"  { return "image/gif" }
        ".svg"  { return "image/svg+xml" }
        ".ico"  { return "image/x-icon" }
        default { return "application/octet-stream" }
    }
}

try {
    while ($listener.IsListening) {
        $context = $listener.GetContextAsync().Result
        $request = $context.Request
        $response = $context.Response
        
        $path = $request.Url.LocalPath
        $filePath = Join-Path $PWD $path.TrimStart('/')
        
        # Default to landing.html for root
        if ($path -eq "/" -or $path -eq "") { 
            $filePath = Join-Path $PWD "landing.html" 
        }

        if (Test-Path $filePath -PathType Leaf) {
            $content = [System.IO.File]::ReadAllBytes($filePath)
            $response.ContentType = Get-MimeType $filePath
            $response.ContentLength64 = $content.Length
            $response.OutputStream.Write($content, 0, $content.Length)
            $response.StatusCode = 200
        } else {
            $response.StatusCode = 404
            $msg = [System.Text.Encoding]::UTF8.GetBytes("404 Not Found")
            $response.OutputStream.Write($msg, 0, $msg.Length)
        }
        $response.Close()
    }
} finally {
    $listener.Stop()
}
