import subprocess

from PCreateTable import *
from PBox import *

tableFormats=["p{1cm}","X","X","p{1.4cm}","X","p{2cm}","X","X"]
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

tableHeaders2 = [
    "Mal Hizmet Toplam Tutarı",
    "Toplam İskonto",
    "Hesaplanan KDV(\%20)",
    "Vergiler Dahil Toplam Tutar",
    "Ödenecek Tutar",
]
tableRows2 = [
    ["650 TL", "0 TL", "120 TL", "780 TL", "780 TL"],
]

latexStr=""
latexStr += "\\noindent"
latexStr+=CreateHorizontalTable(tableFormats=tableFormats,tableHeaders=tableHeaders,tableRows=tableRows)
latexStr += "\n\\vspace{0.2cm}\n"
latexStr+=EmptyBox("0.6\\textwidth")
latexStr+="\\hfill"
latexStr+=WrapperBox(width="0.4\\textwidth",child=CreateVerticalTable(tableHeaders=tableHeaders2,tableRows=tableRows2))
latexStr += "\n\\vspace{0.2cm}\n"
latexStr+=ColorBox("Yalnız YediYüzSeksenTürkLirası")

with open("content.tex", "w", encoding="utf-8") as f:
    f.write(latexStr)




subprocess.run(["bash", "run.sh"], check=True)
