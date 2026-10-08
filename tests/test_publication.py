"""Publication-mode figure sizing and LaTeX probe unit tests."""
from __future__ import annotations

import math
from pathlib import Path
import re

import matplotlib
matplotlib.use("Agg", force=True)
import matplotlib as mpl
import matplotlib.pyplot as plt
import pytest

import contrastcolors as cc
import contrastcolors.publication as pub


@pytest.fixture(autouse=True)
def cleanup():
    yield
    plt.close("all")


@pytest.fixture
def layout():
    return cc.LatexLayout.from_dimensions(
        columnwidth_pt=240.0,
        textwidth_pt=500.0,
        fontsize_pt=10.0,
        baselineskip_pt=12.0,
        font_family="ptm",
    )


def test_dimensions_and_pt_to_inch(layout):
    assert math.isclose(layout.width_inches("column"), 240 / 72.27)
    assert math.isclose(layout.width_inches("text"), 500 / 72.27)
    assert layout.width_pt("page") == 500.0
    assert layout.width_pt(3.0) == pytest.approx(3 * 72.27)
    with pytest.raises(ValueError):
        layout.width_inches("bad")
    with pytest.raises(ValueError):
        layout.width_inches(0)
    with pytest.raises(ValueError):
        cc.LatexLayout.from_dimensions(
            columnwidth_pt=550, textwidth_pt=300, fontsize_pt=10
        )


def test_probe_parses_pt_and_font_identity():
    log = "\n".join([
        "CCLAYOUT:COLUMN=242.315pt",
        "CCLAYOUT:TEXT=510.123pt",
        "CCLAYOUT:FONT=10 pt",
        "CCLAYOUT:BASELINE=12.0pt",
        "CCLAYOUT:FAMILY=ppl",
        "CCLAYOUT:FONTNAME=pplr7t at 10.0pt",
    ])
    layout = pub._parse_layout_log(log)
    assert layout.columnwidth_pt == pytest.approx(242.315)
    assert layout.textwidth_pt == pytest.approx(510.123)
    assert layout.fontsize_pt == 10
    assert layout.baselineskip_pt == 12
    assert layout.font_family == "ppl"
    with pytest.raises(cc.LatexProbeError):
        pub._parse_layout_log("No measurements")


def test_preamble_probe_does_not_compile_paper_body(monkeypatch, tmp_path):
    tex = tmp_path / "main.tex"
    tex.write_text(
        "\\documentclass[twocolumn]{article}\n"
        "% \\begin{document} (not the real begin document)\n"
        "\\usepackage{amsmath}\n"
        "\\begin{document}\n"
        "THE PRIVATE MANUSCRIPT BODY MUST NOT BE COMPILED\n"
        "\\end{document}\n", encoding="utf-8"
    )
    calls = []

    def fake_run(source, *, source_dir, engine, timeout, output_pdf=None):
        calls.append((source, source_dir, engine, timeout))
        return (
            "CCLAYOUT:COLUMN=240.0pt\nCCLAYOUT:TEXT=500.0pt\n"
            "CCLAYOUT:FONT=10 pt\nCCLAYOUT:BASELINE=12 pt\n"
            "CCLAYOUT:FAMILY=cmr\n"
        )
    monkeypatch.setattr(pub, "_run_tex", fake_run)
    layout = cc.inspect_latex(tex)
    assert layout.fontsize_pt == 10
    assert "THE PRIVATE MANUSCRIPT BODY" not in calls[0][0]
    assert r"\usepackage{amsmath}" in calls[0][0]
    assert calls[0][1] == tmp_path
    assert calls[0][2] == "pdflatex"


def test_latex_style_sets_real_font_and_width(layout, tmp_path):
    before = mpl.rcParams.copy()
    with cc.latex_style(layout, width="column") as publication:
        assert mpl.rcParams["font.size"] == 10
        assert mpl.rcParams["axes.labelsize"] == 10
        assert mpl.rcParams["xtick.labelsize"] == 8
        fig, ax = publication.subplots()
        ax.plot([0, 1, 2], [3, 4, 2])
        ax.set(xlabel="Time", ylabel="Price")
        assert fig.get_size_inches()[0] == pytest.approx(layout.width_inches())
        audit = publication.audit(fig)
        assert audit.passed, audit.warnings
        assert ax.xaxis.label.get_fontsize() == 10
        path = publication.savefig(fig, tmp_path / "publication.pdf")
        assert path.exists() and path.stat().st_size > 500
        assert "MediaBox" in path.read_bytes().decode("latin-1", "ignore")
    assert mpl.rcParams["font.size"] == before["font.size"]


def test_existing_figure_fit_does_not_compound_font_scaling(layout):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot([0, 1], [0, 1])
    ax.set_xlabel("Time", fontsize=12)
    start_fontsize = ax.xaxis.label.get_fontsize()
    result = cc.fit_figure_to_latex(
        fig, layout, reference_fontsize_pt=10, max_iterations=3
    )
    assert fig.get_size_inches()[0] == pytest.approx(layout.width_inches())
    assert ax.xaxis.label.get_fontsize() == pytest.approx(12)
    assert result.iterations <= 3
    result2 = cc.fit_figure_to_latex(
        fig, layout, reference_fontsize_pt=10, max_iterations=3
    )
    assert result2.iterations <= 3
    assert ax.xaxis.label.get_fontsize() == pytest.approx(12)
    assert start_fontsize == 12


def test_width_and_readability_audit_fail_on_undersized_figure(layout):
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot([0, 1], [1, 2], linewidth=0.1)
    ax.set_xlabel("x")
    report = cc.audit_figure(fig, layout)
    assert not report.passed
    assert any("width" in issue for issue in report.warnings)
    assert any("line" in issue for issue in report.warnings)


def test_latex_proof_requires_pdf(monkeypatch, tmp_path):
    tex = tmp_path / "paper.tex"
    tex.write_text("\\documentclass{article}\n\\begin{document}\nA\n", encoding="utf-8")
    graphic = tmp_path / "panel.pdf"
    graphic.write_bytes(b"%PDF-1.4\n")

    def fake_run(source, *, source_dir, engine, timeout, output_pdf=None):
        assert r"\usepackage{graphicx}" in source
        assert r"\includegraphics[width=\columnwidth]" in source
        assert str(graphic.resolve().as_posix()) in source
        return "CCLAYOUT:COLUMN=250pt\nCCLAYOUT:TEXT=500pt\nCCLAYOUT:FONT=10pt\n"
    monkeypatch.setattr(pub, "_run_tex", fake_run)
    result = cc.verify_latex_placement(tex, graphic)
    assert result.columnwidth_pt == 250
    with pytest.raises(ValueError):
        cc.verify_latex_placement(tex, tmp_path / "not_a_pdf.png")


def test_exact_source_contains_no_body_and_engine_validation(tmp_path):
    source = r"\documentclass{article}" + "\n" + (
        r"\begin{document}" + "\nHello" + "\n" + r"\end{document}"
    )
    preamble = pub._latex_preamble(source)
    assert "Hello" not in preamble
    assert r"\documentclass" in preamble
    with pytest.raises(ValueError):
        pub._run_tex(source, source_dir=tmp_path, engine="bad", timeout=5)


def test_optional_real_latex_probe_when_installed(tmp_path):
    import shutil
    if shutil.which("pdflatex") is None:
        pytest.skip("pdflatex is not installed in CI")
    tex = tmp_path / "min.tex"
    tex.write_text(
        "\\documentclass[10pt,twocolumn]{article}\n"
        "\\begin{document}\nThis body is not needed.\n\\end{document}\n",
        encoding="utf-8",
    )
    actual = cc.inspect_latex(tex, timeout=30)
    assert actual.fontsize_pt == pytest.approx(10.0)
    assert actual.columnwidth_pt < actual.textwidth_pt
