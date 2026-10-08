"""Test accessibility, print and marker defaults."""
import matplotlib
matplotlib.use("Agg", force=True)
import matplotlib.pyplot as plt
import numpy as np
import pytest
import contrastcolors as cc


@pytest.fixture
def small_fig():
    fig, ax = plt.subplots(figsize=(2.8, 2.0), dpi=70)
    x = np.linspace(0, 6, 80)
    for i, style in enumerate(cc.plot_scheme(
        [20, 140, 260], ratio=1.2, start_luminance=.75
    )):
        ax.plot(x, np.sin(x+i), **style)
    fig.tight_layout()
    yield fig
    plt.close("all")


def test_six_modes(small_fig):
    original = cc.figure_to_rgba(small_fig, max_width=170)
    views = cc.figure_variants(small_fig, max_width=170)
    assert tuple(views) == cc.DEFAULT_ACCESSIBILITY_MODES
    for output in views.values():
        assert output.shape == original.shape
        assert output.dtype == np.uint8
    np.testing.assert_array_equal(views["original"], original)


def test_color_vision_simulations_preserve_alpha():
    src = np.array([[[255, 0, 0, 90], [0, 255, 0, 255]]], dtype=np.uint8)
    for mode in ("deuteranopia", "protanopia", "tritanopia"):
        target = cc.simulate_cvd_image(src, mode)
        np.testing.assert_array_equal(src[..., 3], target[..., 3])
        assert np.any(src[..., :3] != target[..., :3])


def test_grayscale_and_print():
    img = np.array([[[255, 0, 0, 130]]], dtype=np.uint8)
    for transformed in (cc.to_grayscale_image(img),
                        cc.to_print_stress_image(img)):
        assert transformed[0, 0, 0] == transformed[0, 0, 1]
        assert transformed[0, 0, 1] == transformed[0, 0, 2]
        assert transformed[0, 0, 3] == 130


def test_panel_does_not_modify_original(small_fig, tmp_path):
    count = len(small_fig.axes[0].lines)
    panel, axes = cc.show_accessibility_panel(small_fig, max_width=160)
    assert len(axes) == 6
    assert len(small_fig.axes[0].lines) == count
    plt.close(panel)
    target = tmp_path / "panel.png"
    assert cc.save_accessibility_panel(small_fig, target, max_width=160) == target
    assert target.is_file()


def test_bad_inputs(small_fig):
    with pytest.raises(ValueError):
        cc.simulate_figure(small_fig, "invalid")
    with pytest.raises(ValueError):
        cc.to_grayscale_image(np.zeros((3, 2)))
    with pytest.raises(ValueError):
        cc.simulate_cvd_image(np.zeros((1, 1, 3), dtype=np.uint8),
                              "protanopia", severity=101)


def test_scheme_and_automatic_identifiers():
    scheme = cc.scatter_scheme([20, 140, 280], ratio=1.2, start_luminance=.72)
    assert all(set(item) == {"color", "marker"} for item in scheme)
    assert len(set(x["marker"] for x in scheme)) == 3
    with cc.style_context("heri", font="DejaVu Sans"):
        fig, ax = plt.subplots()
        for i in range(3):
            ax.plot([0, 1], [i, i+1])
            ax.scatter([0, 1], [i, i+1])
        assert len(set(x.get_marker() for x in ax.lines)) == 3
        assert len(set(x.get_linestyle() for x in ax.lines)) == 3
        assert len(set(len(c.get_paths()[0].vertices) for c in ax.collections)) >= 2
        plt.close(fig)



@pytest.mark.parametrize("ncols", [2, 3])
def test_panel_titles_centered_just_above_the_rendered_image(small_fig, ncols):
    panel, image_axes = cc.show_accessibility_panel(
        small_fig, ncols=ncols, max_width=220,
        figsize=(10, 12) if ncols == 2 else (13, 8),
        title_fontsize=10, title_pad=0.01,
    )
    panel.canvas.draw()
    renderer = panel.canvas.get_renderer()
    assert len(image_axes) == 6
    assert len(panel.axes) == 6
    for ax in image_axes:
        assert len(ax.texts) == 1
        title = ax.texts[0]
        text_box = title.get_window_extent(renderer)
        image_box = ax.get_window_extent(renderer)
        assert title.get_fontweight() == "normal"
        # Centered on the actual image, not on a wider header cell.
        assert abs((text_box.x0 + text_box.x1) / 2 -
                   (image_box.x0 + image_box.x1) / 2) < 2.0
        assert text_box.y0 >= image_box.y1 - 1.0
        assert text_box.y0 - image_box.y1 < 15.0
    plt.close(panel)


def test_panel_rejects_unusable_title_spacing(small_fig):
    with pytest.raises(ValueError):
        cc.show_accessibility_panel(small_fig, title_fontsize=0)
    with pytest.raises(ValueError):
        cc.show_accessibility_panel(small_fig, title_pad=-1)


@pytest.mark.parametrize("ncols", [2, 3])
def test_vector_dashboard_has_no_raster_images_and_correct_fonts(ncols, tmp_path):
    import matplotlib.collections as collections
    import matplotlib as mpl
    with cc.style_context("heri", font="DejaVu Sans", rasterize=False):
        source, ax = plt.subplots()
        x = np.arange(5)
        for i, color in enumerate(("#E69F00", "#0072B2", "#009E73")):
            ax.plot(x, x + i, label=f"Series {i+1}", marker="o",
                    color=color, linestyle=("-", "--", ":")[i])
        ax.set(xlabel="Time", ylabel="Response")
        panel, views = cc.show_vector_accessibility_panel(
            source, ncols=ncols, figsize=(7, 8 if ncols == 2 else 4.5),
            axis_label_fontsize=10, title_fontsize=10,
        )
        assert len(views) == 6
        for panel_ax in views:
            assert not panel_ax.images
            assert len(panel_ax.lines) == 3
            assert panel_ax.xaxis.label.get_fontsize() == 10
            assert panel_ax.yaxis.label.get_fontweight() == "normal"
            assert panel_ax.title.get_fontsize() == 10
        out = tmp_path / "vectors.pdf"
        with mpl.rc_context({"savefig.bbox": None}):
            panel.savefig(out, bbox_inches=None)
        content = out.read_bytes()
        assert b"/Subtype /Image" not in content
        assert out.stat().st_size > 500
        plt.close(panel)
        plt.close(source)


def test_vector_scatter_keeps_marker_geometry_alpha_and_white_edges():
    fig, ax = plt.subplots()
    for i, (color, marker) in enumerate(zip(
        ("#E69F00", "#0072B2", "#009E73"), ("o", "s", "^")
    )):
        ax.scatter([0, 1], [i, i + 1], marker=marker, c=color, s=45,
                   alpha=.62, edgecolors="white", linewidths=.22,
                   label=f"Group {i+1}")
    dest, axs = cc.show_vector_accessibility_panel(
        fig, figsize=(7, 8), ncols=2,
    )
    for a in axs:
        assert not a.images
        assert len(a.collections) == 3
        for original, copied in zip(ax.collections, a.collections):
            assert copied.get_rasterized() is False
            np.testing.assert_allclose(original.get_offsets(), copied.get_offsets())
            np.testing.assert_allclose(original.get_sizes(), copied.get_sizes())
            np.testing.assert_allclose(copied.get_linewidths(), [.22])
            np.testing.assert_allclose(copied.get_edgecolors()[:, :3], [[1, 1, 1]])
            assert np.max(copied.get_facecolors()[:, 3]) == pytest.approx(.62)
    plt.close(dest)
    plt.close(fig)


def test_vector_dashboard_rejects_unsupported_heatmaps():
    fig, ax = plt.subplots()
    ax.imshow(np.ones((2, 3)))
    with pytest.raises(ValueError, match="no line or scatter"):
        cc.show_vector_accessibility_panel(fig)
    plt.close(fig)
