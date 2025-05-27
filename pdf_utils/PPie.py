from typing import List


def CreatePieChart(labels: List[str], values: List[float]) -> str:
    assert len(labels) == len(values), "Sizes must match!"

    latexStr = ""
    latexStr += "\\begin{center} \n"
    latexStr += "\\begin{tikzpicture} \n"
    latexStr += "\\pie[radius=2.5,text=legend,explode=0.1]{ \n"
    vec = []
    for i in range(len(values)):
        vec.append(f"{values[i]}/{labels[i]}")
    latexStr += ",".join(vec)
    latexStr += "}\n"
    latexStr += "\\end{tikzpicture} \n"
    latexStr += "\\end{center}\n"

    latexStr += "\n"
    return latexStr


def CreatePieChart2(labels: List[str], values: List[float],colors:List[str]) -> str:
    assert len(labels) == len(values), "Sizes must match!"

    latexStr = ""
    latexStr += "\\begin{center} \n"
    latexStr += "\\begin{tikzpicture} \n"

    latexStr += "\\pie[text=inside,scale font,explode=0.1,color={" + ",".join(colors) + "}]\n{"
    vec = []
    for i in range(len(values)):
        # vec.append(f"{values[i]}/{labels[i]}")
        vec.append(f"{values[i]}/")
    latexStr += ",".join(vec)
    latexStr += "}\n"
    # Custom legend
    latexStr += "\\begin{scope}[shift={(5,1)}]\n"
    for i, label in enumerate(labels):
        val=values[i]
        color = colors[i]
        y = -0.7 * i
        latexStr += f"\\fill[{color}] (0,{y}) rectangle (0.5,{y+0.3});\n"
        latexStr += f"\\node[right] at (0.6,{y+0.15}) {{{label} ({val})}};\n"
    latexStr += "\\end{scope}\n"

    latexStr += "\\end{tikzpicture}\n"
    latexStr += "\\end{center}\n"

    return latexStr
