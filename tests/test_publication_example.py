"""Static tests for the macOS publication showcase sources."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "examples" / "latex_publication"


def test_manuscript_has_all_demo_graphics():
    assert all((DEMO / name).is_file() for name in (
        "main.tex", "generate.py", "run_macos.sh", "README.md"))
    tex = (DEMO / "main.tex").read_text(encoding="utf-8")
    assert r"\documentclass[10pt,twocolumn,a4paper]{article}" in tex
    assert r"\usepackage{lmodern}" in tex
    assert r"\input{generated/lines.pgf}" in tex
    assert r"\includegraphics{generated/lines.pdf}" in tex
    assert r"\includegraphics{generated/dense.pdf}" in tex
    assert r"\includegraphics[width=\textwidth]{generated/accessibility.png}" in tex
    assert r"\end{document}" in tex


def test_generated_graphics_use_public_apis():
    script = (DEMO / "generate.py").read_text(encoding="utf-8")
    for part in (
        "cc.inspect_latex(", "cc.find_latex_font(", "cc.latex_style(",
        "cc.save_accessibility_panel(", "cc.scatter_scheme(",
        "cc.verify_latex_placement(",
    ):
        assert part in script
    assert "np.random.default_rng(20261007)" in script
    assert "lines.pgf" in script
    assert "lines.pdf" in script


def test_builder_only_pushes_after_opt_in():
    sh = (DEMO / "run_macos.sh").read_text(encoding="utf-8")
    assert "set -Eeuo pipefail" in sh
    assert "publication_demo.pdf" in sh
    assert "publication_accessibility.png" in sh
    assert "if ((COMMIT)); then" in sh
    assert "if ((PUSH)); then git push; fi" in sh


def test_site_navigation_and_ignore_rules():
    page = (ROOT / "docs/source/publication_demo.rst").read_text(encoding="utf-8")
    index = (ROOT / "docs/source/index.rst").read_text(encoding="utf-8")
    ignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    assert "_static/publication_demo.pdf" in page
    assert "_static/publication_accessibility.png" in page
    assert "   publication_demo" in index
    assert "examples/latex_publication/generated/" in ignore


def test_demo_python_and_bash_have_valid_syntax():
    import shutil
    import subprocess

    generator = DEMO / "generate.py"
    compile(generator.read_text(encoding="utf-8"), str(generator), "exec")
    bash = shutil.which("bash")
    if bash:
        subprocess.run([bash, "-n", str(DEMO / "run_macos.sh")], check=True)
