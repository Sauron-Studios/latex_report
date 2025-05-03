import subprocess

from PCreateTable import *
from PBox import *

def A4Report(latexStr:str):
    with open("content.tex", "w", encoding="utf-8") as f:
        f.write(latexStr)


    subprocess.run(["pdflatex", "main_a4_report"], check=True)
    subprocess.run(["pdflatex", "main_a4_report"], check=True)

A4Report("")