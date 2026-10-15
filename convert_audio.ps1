$root = "D:\5games\Monster-battle-Web\audio"

Get-ChildItem $root -Recurse -File -Include *.mp3,*.wav,*.ogg.mp3,*.wav.mp3 | ForEach-Object {

    $input = $_.FullName

    $base = $_.BaseName
    $base = $base -replace "\.ogg$", ""
    $base = $base -replace "\.wav$", ""

    $output = Join-Path $_.DirectoryName ($base + ".ogg")

    Write-Host "Converting $($_.Name) -> $([System.IO.Path]::GetFileName($output))"

    ffmpeg -y -loglevel error -i "$input" `
        -ac 1 `
        -ar 44100 `
        -c:a libvorbis `
        "$output"
}