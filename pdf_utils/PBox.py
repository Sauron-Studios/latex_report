from typing import List

def EmptyBox(width: str) -> str:
    latexStr = ""
    latexStr += "\\begin{minipage}{" + width + "} \n"
    latexStr += "\\hfill \n"
    latexStr += "\\end{minipage} \n"
    return latexStr

def WrapperBox(width: str, child: str) -> str:
    latexStr = ""
    latexStr += "\\begin{minipage}{" + width + "} \n"
    latexStr += child
    latexStr += "\\end{minipage} \n"
    return latexStr

def ColorBox(child: str) -> str:
    latexStr = ""
    latexStr += "\\begin{tcolorbox}[colframe=black, colback=white, boxrule=0.8mm, sharp corners, height=2cm, width=\\textwidth] \n"
    latexStr += child
    latexStr += "\\end{tcolorbox} \n"
    return latexStr

def CustomerBox(details: List[str]) -> str:
    latexStr = ""
    latexStr += "\\begin{minipage}[t]{\linewidth} \n"
    latexStr += "\\noindent\\rule{\\linewidth}{2pt}\\\\ \n"
    latexStr += "\\bfseries\\scriptsize "
    latexStr += "\\\\ \n".join(details)
    latexStr += "\\\\\n"
    latexStr += "\\noindent\\rule{\\linewidth}{2pt} \n"
    latexStr += "\\end{minipage} \n"
    return latexStr

def LogoBox(logo:str)->str:
    latexStr = ""
    latexStr += "\\raggedleft"
    # latexStr += "\\fbox{"
    latexStr += "\\begin{minipage}[c]{0.3\\textwidth} \n"
    latexStr += "\\centering \n"
    latexStr += "\\includegraphics[width=\\linewidth]{"+logo+"} \\\\ \n"
    latexStr += "\\end{minipage} \n"
    # latexStr += "}"

    return latexStr

def InvoiceLogoBox()->str:
    latexStr = ""
    latexStr += "\\begin{minipage}[c]{75mm} \n"
    latexStr += "\\centering \n"
    latexStr += "\\includegraphics[width=33mm]{logo} \\\\ \n"
    latexStr += "\\bfseries Fatura \n"
    latexStr += "\\end{minipage} \n"
    return latexStr

def Row(children:List[str])->str:
    latexStr = ""
    latexStr += "\\begin{tabularx}{\\textwidth}{"
    latexStr += "" + "".join("X"*len(children)) + "}\n "
    latexStr += " & ".join(children) + "\\\\ \n "
    latexStr += "\\end{tabularx}"
    return latexStr

def Column(children: List[str]) -> str:
    latexStr = ""
    latexStr += "\\begin{minipage}[t]{\linewidth} \n"
    latexStr += "\\noindent \n"
    latexStr += "\\\\ \n".join(children)
    latexStr += "\\end{minipage} \n"
    return latexStr
