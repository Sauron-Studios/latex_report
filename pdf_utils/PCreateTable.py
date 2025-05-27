from typing import List

def CreateHorizontalTable(
    tableFormats: List[str], tableHeaders: List[str], tableRows: List[str]
) -> str:
    if len(tableHeaders)>0:
        assert len(tableFormats) == len(tableHeaders), "Sizes must match!"
    assert len(tableFormats) == (
        len(tableRows[0]) if tableRows else 0
    ), "Sizes must match!"
    latexStr = ""

    latexStr += "\\begin{tcolorbox}[colframe=black, colback=white, boxrule=0.2mm, boxsep=0pt,left=0pt,right=0pt,top=0pt,bottom=0pt,sharp corners]"

    latexStr += "\\begin{tabularx}{\\textwidth}{"
    latexStr += "|" + "|".join(tableFormats) + "|}\\hline \n "
    
    if len(tableHeaders)>0:
        temp = ["\\textbf{" + x + "}" for x in tableHeaders]
        latexStr += " & ".join(temp) + "\\\\ \hline\n "
    
    for row in tableRows:
        latexStr += " & ".join(row) + " \\\\ \hline\n "
    latexStr += "\\end{tabularx}"

    latexStr += "\\end{tcolorbox}"
    
    latexStr += "\n"
    return latexStr


def CreateVerticalTable(tableHeaders: List[str], tableRows: List[str]) -> str:
    assert len(tableHeaders) == (
        len(tableRows[0]) if tableRows else 0
    ), "Sizes must match!"
    latexStr = ""

    latexStr += "\\begin{tcolorbox}[colframe=black, colback=white, boxrule=0.2mm, boxsep=0pt,left=0pt,right=0pt,top=0pt,bottom=0pt,sharp corners]"

    latexStr += "\\begin{tabularx}{\\linewidth}{|l|"

    cols = len(tableRows)
    latexStr += "|".join("X" * cols) + "|}\\hline \n"

    newtableRows = list(map(list, zip(*tableRows)))
    for i, row in enumerate(newtableRows):
        temp = "\\textbf{" + tableHeaders[i] + "} &"
        temp2 = " & ".join(row) + " \\\\ \hline"
        latexStr += f"{temp} {temp2} \n"

    latexStr += "\\end{tabularx}"
    latexStr += "\\end{tcolorbox}"
    
    latexStr += "\n"
    return latexStr
