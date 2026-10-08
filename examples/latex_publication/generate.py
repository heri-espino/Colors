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
        # Default plot_scheme uses an adaptive, broadly separated gray
        # scale for three groups, with different markers and dash patterns.
        line_styles = cc.plot_scheme([25, 150, 275])
        for i, style in enumerate(line_styles):
            signal = 0.72 * np.sin(0.56 * t + 0.65 * i) + 0.22 * i + 0.04 * t
            ax.plot(
                t, signal, markevery=22, linewidth=1.9,
                markersize=6.0, label=f"Series {i + 1}", **style
            )
        ax.set(xlabel=r"Time ($t$)", ylabel=r"Response ($y$)")
        # Never cover a curve with a legend; constrain layout allocates
        # room for this legend outside the axes.
        ax.legend(
            loc="lower center", bbox_to_anchor=(0.5, 1.015),
            ncol=3, frameon=False, fontsize=8,
            handlelength=2.0, columnspacing=0.85,
        )
        audit(pub, fig, "lines", diagnostics)
        cc.save_accessibility_panel(
            fig, out / "accessibility.png",
            dpi=185, max_width=850, ncols=2, figsize=(9.0, 11.4),
        )
        pub.savefig(fig, out / "lines.pdf", audit=False)
        pub.savefig(fig, out / "lines.pgf", audit=False)
        plt.close(fig)

    with cc.latex_style(tex, width="column", engine=args.engine, rasterize=False) as pub:
        fig, ax = pub.subplots(height_ratio=0.78)
        markers = cc.scatter_scheme([25, 155, 265])
        for i, style in enumerate(markers):
            x = data.normal(i * 0.65, 0.45, size=34)
            y = 0.50 * x + data.normal(i * 0.45, 0.32, size=34)
            ax.scatter(
                x, y, s=52, alpha=0.96,
                edgecolors="#292929", linewidths=0.55,
                label=f"Group {i + 1}", **style
            )
        ax.set(xlabel="Measurement A", ylabel="Measurement B")
        ax.legend(
            loc="lower center", bbox_to_anchor=(0.5, 1.015),
            ncol=3, frameon=False, fontsize=8,
            markerscale=0.95, columnspacing=0.75,
        )
        audit(pub, fig, "groups", diagnostics)
        cc.save_accessibility_panel(
            fig, out / "groups_accessibility.png",
            dpi=165, max_width=700, figsize=(11.2, 6.4),
        )
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
        "groups_accessibility.png",
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
        "adaptive_print_luminances_for_3_series": cc.print_safe_luminances(3).tolist(),
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
