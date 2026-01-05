# スクリプト自身の場所から app に移動
Set-Location "C:\EngineersData\01_Projects\09_NLP2PokeGraph\app"

Get-ChildItem -Recurse -Force |
Where-Object {
    $_.FullName -notmatch '\\(tools|external|__pycache__)($|\\)'
} |
Sort-Object FullName |
ForEach-Object {
    $depth = ($_.FullName.Substring((Get-Location).Path.Length) -split '\\').Count - 1
    ('│   ' * ($depth - 1)) + '├── ' + $_.Name
} |
Out-File -Encoding UTF8 "$PSScriptRoot\..\directory_tree.txt"
