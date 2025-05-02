def EmptyBox(width:str)->str:
    latexStr = ""
    latexStr += "\\noindent"
    latexStr += "\\begin{minipage}{"+width+"}"

    latexStr += "\\hfill"

    latexStr+="\\end{minipage}"

    return latexStr

def WrapperBox(width:str,child:str)->str:
    latexStr = ""
    latexStr += "\\noindent"
    latexStr += "\\begin{minipage}{"+width+"}"
    latexStr+=child
    latexStr+="\\end{minipage}"
    return latexStr

def ColorBox(child:str)->str:
    latexStr=""
    latexStr += "\\begin{tcolorbox}[colframe=black, colback=white, boxrule=0.8mm, sharp corners, height=2cm, width=\\textwidth]"
    latexStr+=child
    latexStr += "\\end{tcolorbox}"

    return latexStr
