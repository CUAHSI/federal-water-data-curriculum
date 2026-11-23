# Build the blank final-assessment scoring sheet (Excel) for demo graders.
# Usage (Windows PowerShell, needs Excel installed):
#   powershell -ExecutionPolicy Bypass -File teaching-materials\how-to-build\tools\assessment_scoring_sheet.ps1 `
#     -out "$PWD\teaching-materials\materials\assessment\final-assessment_scoring-sheet.xlsx" -rows 10
# Columns: Learner, Option, criteria 1-4 (whole numbers 1-4, validated), Notes. A "Key" tab has short
# instructions. Staff prefill Learner and Option per grader before the demos.
param([Parameter(Mandatory = $true)][string]$out, [int]$rows = 10)
$ErrorActionPreference = "Stop"
$xl = New-Object -ComObject Excel.Application
try {
    $xl.Visible = $false; $xl.DisplayAlerts = $false
    $wb = $xl.Workbooks.Add()
    $ws = $wb.Worksheets.Item(1)
    $ws.Name = "Scores"
    $last = $rows + 1
    $h = @("Learner", "Option", "1. Data selection", "2. Data access", "3. Combining", "4. Limitations", "Notes")
    for ($c = 1; $c -le $h.Count; $c++) { $ws.Cells.Item(1, $c).Value2 = $h[$c - 1] }
    $hdr = $ws.Range("A1:G1")
    $hdr.Font.Bold = $true; $hdr.Font.Color = 0xFFFFFF; $hdr.Interior.Color = 0x50382A
    $hdr.WrapText = $true; $hdr.VerticalAlignment = -4108
    $ws.Range("A2:B$last").Interior.Color = 0xF2F2F2
    $ws.Range("C2:F$last").Interior.Color = 0xDDF5FF
    $ws.Range("C2:F$last").HorizontalAlignment = -4108
    $v = $ws.Range("C2:F$last").Validation
    $v.Delete(); $v.Add(1, 1, 1, "1", "4")
    $v.ErrorMessage = "Enter a whole number from 1 to 4"
    $v.InputMessage = "1 Beginning, 2 Developing, 3 Proficient, 4 Exemplary"
    $widths = @(24, 8, 11, 11, 11, 11, 60)
    for ($c = 1; $c -le $widths.Count; $c++) { $ws.Columns.Item($c).ColumnWidth = $widths[$c - 1] }
    $ws.Range("G2:G$last").WrapText = $true
    $ws.Range("A1:G$last").Borders.LineStyle = 1
    $ws.Range("A1:G$last").Borders.Color = 0xBFBFBF
    $ws.Rows.Item(1).RowHeight = 32
    $ws.Activate(); $xl.ActiveWindow.SplitRow = 1; $xl.ActiveWindow.FreezePanes = $true
    $k = $wb.Worksheets.Add([Type]::Missing, $ws); $k.Name = "Key"
    $lines = @("Grader:", "Group:", "",
        "Scores: 1 Beginning, 2 Developing, 3 Proficient, 4 Exemplary (see the grader packet, section 4).",
        "Notes: anything worth noting, including flags (e.g. 'Flag (3): said valid time, plot uses issue time') and 'ran out of time'.",
        "Flags in two or more criteria: tell the lead instructor after the block.",
        "Criterion 5 is scored by CUAHSI staff after the demos.")
    for ($i = 0; $i -lt $lines.Count; $i++) { $k.Cells.Item($i + 1, 1).Value2 = $lines[$i] }
    $k.Range("A1:A2").Font.Bold = $true; $k.Columns.Item(1).ColumnWidth = 100
    $ws.Activate()
    $wb.SaveAs($out, 51)
    $wb.Close()
    "wrote $out"
}
finally {
    $xl.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($xl) | Out-Null
}
