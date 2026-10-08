"""Generate LaTeX-fitted plots, an accessibility panel, and a width proof."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import contrastcolors as cc


HERE = Path(__file__).resolve().parent


def audit(publication, figure, label: str, records: dict) -> None:
    result = publication.audit(figure)
    records[label] = {
        "passed": bool(result.passed),
        "expected_width_tex_pt": float(result.expected_width_pt),
        "figure_width_tex_pt": float(result.output_width_pt),
        "smallest_text_pdf_pt": (
            float(result.smallest_text_pt) if result.smallest_text_pt is not None else None
        ),
        "smallest_line_pdf_pt": (
            float(result.smallest_line_pt) if result.smallest_line_pt is not None else None
        ),
        "warnings": list(result.warnings),
    }
    print(f"  {label}: {'PASS' if result.passed else 'REVIEW'}")
    for warning in result.warnings:
        print("    " + warning)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tex", type=Path, default=HERE / "main.tex")
    parser.add_argument("--output", type=Path, default=HERE / "generated")
    parser.add_argument(
        "--engine", default="pdflatex",
        choices=("pdflatex", "xelatex", "lualatex"),
    )
    args = parser.parse_args()
    tex = args.tex.resolve()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)

    layout = cc.inspect_latex(tex, engine=args.engine)
    font = cc.find_latex_font(tex, engine=args.engine)
    print(f"Document: {tex}")
    print(f"  Column width: {layout.columnwidth_pt:.2f} TeX pt")
    print(f"  Text width: {layout.textwidth_pt:.2f} TeX pt")
    print(f"  Font: {layout.fontsize_pt:.2f} pt, {font.tex_font_name}")
    print(f"  Metrics: {font.metrics_path or 'not resolved'}")
    print(f"  Outlines: {font.outline_path or 'not resolved'}")

    data = np.random.default_rng(20261007)
    diagnostics: dict[str, dict] = {}
    t = np.linspace(0.0, 12.0, 220)

    with cc.latex_style(tex, width="column", engine=args.engine, rasterize=False) as pub:
        fig, ax = pub.subplots(height_ratio=0.80)
        for i in range(3):
            signal = 0.72 * np.sin(0.56 * t + 0.65 * i) + 0.22 * i + 0.04 * t
            ax.plot(t, signal, markevery=20, label=f"Series {i + 1}")
        ax.set(xlabel=r"Time ($t$)", ylabel=r"Response ($y$)")
        ax.legend(loc="upper right")
        audit(pub, fig, "lines", diagnostics)
        cc.save_accessibility_panel(
            fig, out / "accessibility.png",
            dpi=165, max_width=700, figsize=(11.2, 6.4),
        )
        pub.savefig(fig, out / "lines.pdf", audit=False)
        pub.savefig(fig, out / "lines.pgf", audit=False)
        plt.close(fig)

    with cc.latex_style(tex, width="column", engine=args.engine, rasterize=False) as pub:
        fig, ax = pub.subplots(height_ratio=0.78)
        markers = cc.scatter_scheme(
            [25, 155, 265], ratio=1.20, start_luminance=0.75, chroma=0.13
        )
        for i, style in enumerate(markers):
            x = data.normal(i * 0.65, 0.45, size=45)
            y = 0.50 * x + data.normal(i * 0.45, 0.32, size=45)
            ax.scatter(x, y, s=26, alpha=0.85, label=f"Group {i + 1}", **style)
        ax.set(xlabel="Measurement A", ylabel="Measurement B")
        ax.legend(loc="upper left")
        audit(pub, fig, "groups", diagnostics)
        pub.savefig(fig, out / "groups.pdf", audit=False)
        plt.close(fig)

    with cc.latex_style(tex, width="column", engine=args.engine, rasterize=True) as pub:
        fig, ax = pub.subplots(height_ratio=0.77)
        x = data.standard_normal(18000)
        y = 0.68 * x + 0.42 * data.standard_normal(len(x))
        points = ax.scatter(
            x, y, s=1.8, alpha=0.28, color=cc.HERI_PALETTE[1]
        )
        if not points.get_rasterized():
            raise RuntimeError("Dense scatter was not rasterized.")
        ax.set(xlabel="Feature", ylabel="Outcome")
        audit(pub, fig, "dense", diagnostics)
        pub.savefig(fig, out / "dense.pdf", audit=False, dpi=300)
        plt.close(fig)

    cc.verify_latex_placement(
        tex, out / "lines.pdf", width="column", engine=args.engine,
        proof_pdf=out / "lines_proof.pdf",
    )
    names = (
        "lines.pdf", "lines.pgf", "lines_proof.pdf",
        "groups.pdf", "dense.pdf", "accessibility.png",
    )
    for name in names:
        file = out / name
        if not file.is_file() or file.stat().st_size < 100:
            raise RuntimeError(f"Missing or empty generated file: {file}")
    report = {
        "tex_file": str(tex),
        "engine": args.engine,
        "layout": {
            "columnwidth_tex_pt": layout.columnwidth_pt,
            "textwidth_tex_pt": layout.textwidth_pt,
            "body_font_pt": layout.fontsize_pt,
            "font_family": layout.font_family,
            "font_name": layout.font_name,
        },
        "font_file": {
            "outline": str(font.outline_path) if font.outline_path else None,
            "metrics": str(font.metrics_path) if font.metrics_path else None,
            "status": font.source,
        },
        "audits": diagnostics,
        "file_sizes_bytes": {n: (out / n).stat().st_size for n in names},
    }
    (out / "report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    print("Outputs saved in", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
