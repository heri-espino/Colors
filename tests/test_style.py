from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import pytest

import contrastcolors as cc


def teardown_function():
    cc.set_style("default")
    plt.close("all")


def test_set_style_heri_applies_publication_spines_and_transparency():
    cc.set_style("heri", use_tex=False)

    assert mpl.rcParams["axes.spines.top"] is False
    assert mpl.rcParams["axes.spines.right"] is False
    assert mpl.rcParams["figure.facecolor"] == "none"
    assert mpl.rcParams["savefig.transparent"] is True
    assert mpl.rcParams["pdf.fonttype"] == 42


def test_heri_style_rasterizes_data_but_not_axis_text():
    cc.set_style("heri", use_tex=False, rasterize=True)
    fig, ax = plt.subplots()
    (line,) = ax.plot([0, 1], [0, 1])
    ax.set_xlabel("x")

    assert line.get_rasterized() is True
    assert ax.xaxis.label.get_rasterized() is False


def test_rasterization_can_be_disabled():
    cc.set_style("heri", use_tex=False, rasterize=False)
    fig, ax = plt.subplots()
    (line,) = ax.plot([0, 1], [0, 1])

    assert line.get_rasterized() is False


def test_save_figure_defaults_to_pdf(tmp_path: Path):
    cc.set_style("heri", use_tex=False)
    fig, ax = plt.subplots()
    ax.scatter([0, 1], [1, 0])

    path = cc.save_figure(fig, tmp_path / "example")
    assert path.suffix == ".pdf"
    assert path.exists()
    assert path.stat().st_size > 0


def test_style_context_restores_previous_rcparams():
    before = mpl.rcParams["axes.spines.top"]
    with cc.style_context("heri", use_tex=False):
        assert mpl.rcParams["axes.spines.top"] is False
    assert mpl.rcParams["axes.spines.top"] == before


def test_unknown_style_fails():
    with pytest.raises(ValueError):
        cc.set_style("not-a-style")
