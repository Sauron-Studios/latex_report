from http.client import HTTPException
import subprocess
import tempfile
from pathlib import Path

from django.http import FileResponse

def compile_latex_to_bytes(latex_code: str) -> FileResponse:
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            tex_path = tmp_path / "doc.tex"
            pdf_path = tmp_path / "doc.pdf"
            log_path = tmp_path / "doc.log"

            # Write LaTeX code
            tex_path.write_text(latex_code, encoding="utf-8")

            # Compile
            result = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", tex_path.name],
                cwd=tmp_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            # Compilation failed (non-zero return code)
            if result.returncode != 0:
                log_content = log_path.read_text(encoding="utf-8") if log_path.exists() else ""
                raise HTTPException(status_code=400, detail=f"LaTeX compilation failed.\n{log_content[-500:]}")

            if not pdf_path.exists():
                raise HTTPException(status_code=500, detail="PDF was not created.")

            # Return PDF
            return FileResponse(
                path=pdf_path,
                content_type="application/pdf",
                filename="report.pdf",
                as_attachment=True
            )

    except HTTPException:
        raise  # re-raise known FastAPI errors

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")