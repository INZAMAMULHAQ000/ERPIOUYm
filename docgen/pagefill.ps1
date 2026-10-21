param([string]$Docx = 'C:\xampp\htdocs\was\QASWA_ERP_Product_Feature_Compendium.docx')
$ErrorActionPreference = 'Stop'
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
  $d = $word.Documents.Open($Docx, $false, $true)
  $pages = $d.ComputeStatistics(2)
  $sparse = 0
  for ($i = 1; $i -le $pages; $i++) {
    $start = $d.GoTo(1, 1, $i).Start
    if ($i -lt $pages) { $end = $d.GoTo(1, 1, ($i + 1)).Start } else { $end = $d.Content.End }
    $txt = (($d.Range($start, $end)).Text -replace '\s+', ' ').Trim()
    $w = ($txt.Split(' ') | Where-Object { $_ -ne '' }).Count
    $head = $txt; if ($head.Length -gt 62) { $head = $head.Substring(0, 62) }
    if ($w -lt 200) { $sparse++; $tag = 'LIGHT' } else { $tag = '  ok  ' }
    Write-Output ("p{0:d3} {1} words={2:d3}  {3}" -f $i, $tag, $w, $head)
  }
  Write-Output ("TOTAL_PAGES=" + $pages + " LIGHT_PAGES=" + $sparse)
  $d.Close($false)
} finally {
  $word.Quit()
  [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
}
