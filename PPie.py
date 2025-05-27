from typing import List

def CreatePieChart(
        labels: List[str], values: List[float]
) -> str:
    assert len(labels) == len(values), "Sizes must match!"
   
    latexStr = ""
    latexStr +="\\begin{center} \n"
    latexStr +="\\begin{tikzpicture} \n"
    latexStr +="\\pie[radius=2.5,text=inside]{ \n"
	# 30/Cats, 45/Dogs, 25/Owls
    vec=""
    for i in range(len(values)):
        vec+=f"{values[i]}/{labels[i]}"
    latexStr +="}\n"
    latexStr +="\\end{tikzpicture} \n"
    latexStr +="\\end{center}\n"

    latexStr += "\n"
    return latexStr