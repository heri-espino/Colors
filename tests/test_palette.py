import numpy as np

from contrastcolors import contrast_grid


def test_every_column_hits_row_luminance():
    grid = contrast_grid(
        levels=5,
        hues=[50, 15, 145, 210, 290],
        ratio=1.4,
        start_luminance=0.9,
    )
    for i, row in enumerate(grid):
        for cell in row:
            assert abs(cell.actual_luminance - grid.luminances[i]) < 2e-9


def test_any_one_per_row_keeps_constant_contrast():
    grid = contrast_grid(
        levels=5,
        hues=[50, 15, 145, 210, 290],
        ratio=1.4,
        start_luminance=0.9,
    )
    palette = grid.select([4, 1, 3, 0, 2])
    np.testing.assert_allclose(palette.adjacent_contrast, 1.4, atol=2e-8)


def test_diagonal_palette_has_expected_size():
    grid = contrast_grid(levels=4, hues=[20, 120, 240], ratio=1.3)
    assert len(grid.diagonal()) == 4
