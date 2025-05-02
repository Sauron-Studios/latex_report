import subprocess

from PCreateTable import *

tableFormats=["p{1cm}","X","X","p{1.5cm}","X","p{2cm}","X","X"]
tableHeaders = [
    "Sıra No",
    "Stok Kodu",
    "Mal Hizmet",
    "Miktar",
    "Birim Fiyatı",
    "KDV Oranı",
    "KDV Tutarı",
    "Mal Hizmet Tutarı",
]
tableRows = [
    ["1", "3", "Elma", "3", "350 TL", "\\%20", "70 TL", "350 TL"],
    ["2", "5", "Armut", "2","100 TL","\\%20","20 TL","100 TL"],
]

latexStr=""
latexStr += "\\noindent"
latexStr+=CreateHorizontalTable(tableFormats=tableFormats,tableHeaders=tableHeaders,tableRows=tableRows)


latexStr += "\\begin{minipage}[t]{0.48\\textwidth}"
latexStr+="\\end{minipage}"

latexStr+="\\hfill"

latexStr += "\\noindent"
latexStr += "\\begin{minipage}[t]{0.48\\textwidth}"
latexStr+=CreateVerticalTable(tableHeaders=tableHeaders,tableRows=tableRows)
latexStr+="\\end{minipage}"


with open("content.tex", "w", encoding="utf-8") as f:
    f.write(latexStr)




subprocess.run(["bash", "run.sh"], check=True)
