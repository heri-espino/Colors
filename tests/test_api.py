import numpy as np

import contrastcolors as cc


def test_palette_maps_one_hue_to_each_luminance_level():
    p = cc.contrast_palette(
        [55, 20, 145, 210, 290],
        ratio=1.4,
        start_luminance=0.95,
    )
    assert len(p) == 5
    np.testing.assert_allclose(p.adjacent_contrast, 1.4, atol=2e-8)
    np.testing.assert_allclose([cell.hue for cell in p], [55, 20, 145, 210, 290])


def test_color_palette_returns_matplotlib_rgba():
    colors = cc.color_palette([55, 145, 290], ratio=1.3)
    assert len(colors) == 3
    assert all(len(color) == 4 for color in colors)
    assert all(0 <= channel <= 1 for color in colors for channel in color)


def test_color_palette_can_return_hex():
    colors = cc.color_palette([55, 145, 290], ratio=1.3, as_hex=True)
    assert all(color.startswith("#") and len(color) == 7 for color in colors)
