# Convert Word files, and one sheet of an Excel workbook, to PDF with the installed Office.
# Used by build_submission.py. Args: -Docx in.docx -Out out.pdf  or  -Xlsx in.xlsx -Sheet Name -Out out.pdf
param([string]$Docx, [string]$Xlsx, [string]$Sheet, [string]$Out)
$ErrorActionPreference = 'Stop'
if ($Docx) {
    $w = New-Object -ComObject Word.Application; $w.Visible = $false
    try {
        $d = $w.Documents.Open($Docx, $false, $true)
        $d.ExportAsFixedFormat($Out, 17)   # 17 = wdExportFormatPDF
        $d.Close($false)
    } finally { $w.Quit() }
}
if ($Xlsx) {
    $x = New-Object -ComObject Excel.Application; $x.Visible = $false; $x.DisplayAlerts = $false
    try {
        $wb = $x.Workbooks.Open($Xlsx, 0, $true)
        $ws = $wb.Worksheets.Item($Sheet)
        $ps = $ws.PageSetup
        $ps.Orientation = 2          # landscape
        $ps.PaperSize = 8            # A3
        $ps.Zoom = $false
        $ps.FitToPagesWide = 1
        $ps.FitToPagesTall = 1
        $ws.ExportAsFixedFormat(0, $Out)   # 0 = xlTypePDF
        $wb.Close($false)
    } finally { $x.Quit() }
}
