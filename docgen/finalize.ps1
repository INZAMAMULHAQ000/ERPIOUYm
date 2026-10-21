param(
  [string]$Docx = 'C:\xampp\htdocs\was\QASWA_ERP_Product_Feature_Compendium.docx',
  [string]$Pdf  = ''
)
$ErrorActionPreference = 'Stop'
if (-not $Pdf) { $Pdf = Join-Path (Split-Path $Docx -Parent) ((Get-Item $Docx).BaseName + '.pdf') }
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
  $d = $word.Documents.Open($Docx, $false, $false)
  foreach ($t in $d.TablesOfContents) { $t.Update() }
  $d.Fields.Update() | Out-Null
  $d.Repaginate()
  Write-Output ("PAGES=" + $d.ComputeStatistics(2))
  Write-Output ("WORDS=" + $d.ComputeStatistics(0))
  Write-Output ("TABLES=" + $d.Tables.Count)
  $d.SaveAs($Docx, 12)                # wdFormatXMLDocument — bakes real TOC page numbers
  $d.ExportAsFixedFormat($Pdf, 17)    # wdExportFormatPDF
  $d.Close($false)
  Write-Output ("PDF=" + $Pdf)
} finally {
  $word.Quit()
  [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
}
Write-Output "DONE"
