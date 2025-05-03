import subprocess

from PCreateTable import *
from PBox import *

def A4Invoice(latexStr:str):
    with open("content.tex", "w", encoding="utf-8") as f:
        f.write(latexStr)


    subprocess.run(["pdflatex", "main_a4_invoice"], check=True)
    subprocess.run(["pdflatex", "main_a4_invoice"], check=True)

def A5Invoice(latexStr:str):
    with open("content.tex", "w", encoding="utf-8") as f:
        f.write(latexStr)


    subprocess.run(["pdflatex", "main_a5_invoice"], check=True)
    subprocess.run(["pdflatex", "main_a5_invoice"], check=True)


tableFormats = ["p{1cm}", "X", "X", "p{1.4cm}", "X", "p{2cm}", "X", "X"]
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
    ["2", "5", "Armut", "2", "100 TL", "\\%20", "20 TL", "100 TL"],
]

tableHeaders2 = [
    "Mal Hizmet Toplam Tutarı",
    "Toplam İskonto",
    "Hesaplanan KDV(\\%20)",
    "Vergiler Dahil Toplam Tutar",
    "Ödenecek Tutar",
]
tableRows2 = [
    ["650 TL", "0 TL", "120 TL", "780 TL", "780 TL"],
]


sellerDetails = [
    "VATAN BİLGİSAYAR SANAYİ VE TİCARET ANONİM ŞİRKETİ",
    "Aşağı Kayabaşı Mahallesi, Atatürk Blv. No:6 D:6 MERKEZ/NİĞDE",
    "Büyük Mükellefler V.D. 6320023072",
    "Mersis No: V.D. 0632003607286721",
    "Ticaret Sicil No:   191942",
    "Tel: (0388) 212 01 30",
    "Fax: ",
]

buyerDetails = [
    "VATAN BİLGİSAYAR SANAYİ VE TİCARET ANONİM ŞİRKETİ",
    "Aşağı Kayabaşı Mahallesi, Atatürk Blv. No:6 D:6 MERKEZ/NİĞDE",
    "Büyük Mükellefler V.D. 6320023072",
    "Mersis No: V.D. 0632003607286721",
    "Ticaret Sicil No:   191942",
    "Tel: (0388) 212 01 30",
    "Fax: ",
]
latexStr = ""
latexStr = "\\noindent"

latexStr += Row(
    children=[
        Column(
            children=[
                CustomerBox(details=sellerDetails),
                CustomerBox(details=sellerDetails),
            ]
        ),
        Column(
            children=[
                "\\vspace{1cm}",
                InvoiceLogoBox(),
            ]
        ),
        Column(
            children=[
                LogoBox("cat_logo"),
                CustomerBox(details=sellerDetails),
            ]
        ),
    ]
)

latexStr += "\\rowcolors{2}{lightergray}{lightgray}"
latexStr += "\\noindent"
latexStr += CreateHorizontalTable(
    tableFormats=tableFormats, tableHeaders=tableHeaders, tableRows=tableRows
)
latexStr += "\\rowcolors{2}{}{}"
latexStr += "\n\\vspace{0.2cm}\n"
latexStr += EmptyBox("0.57\\textwidth")
latexStr += WrapperBox(
    width="0.4\\textwidth",
    child=CreateVerticalTable(tableHeaders=tableHeaders2, tableRows=tableRows2),
)
latexStr += "\n\\vspace{0.2cm}\n"
latexStr += ColorBox("Yalnız YediYüzSeksenTürkLirası")

A4Invoice(latexStr=latexStr)