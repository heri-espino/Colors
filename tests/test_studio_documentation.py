"""Documentation and Studio controls are published together."""
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STUDIO = ROOT / "docs" / "source" / "_static" / "studio.html"
STUDIO_PAGE = ROOT / "docs" / "source" / "studio.rst"


class Elements(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.types = set()

    def handle_starttag(self, tag, attrs):
        props = dict(attrs)
        if "id" in props:
            self.ids.add(props["id"])
        if "data-plot" in props:
            self.types.add(props["data-plot"])


def test_studio_has_real_export_and_design_controls():
    content = STUDIO.read_text(encoding="utf-8")
    doc = STUDIO_PAGE.read_text(encoding="utf-8")
    elements = Elements()
    elements.feed(content)
    required_ids = {
        "nColors", "ratio", "startY", "chroma", "seriesList",
        "plotSwitcher", "chart", "alpha", "background", "preserve",
        "presetName", "savedPresetList", "savePreset", "loadPreset",
        "deletePreset", "importJson", "importFile", "downloadJson",
        "downloadPy", "copyCode", "code",
    }
    assert required_ids <= elements.ids
    assert {
        "lines", "time", "histogram", "box", "violin", "ridge",
        "scatter", "heatmap", "bar",
    } <= elements.types
    assert "cc.register_palette(" in content
    assert "plotPython(plotType)" in content
    assert "designSnapshot()" in content
    assert "applyDesign(raw)" in content
    assert "_static/studio.html" in doc
    assert "contrastcolors-studio-height" in doc


def test_palette_studio_has_visual_hue_methods_and_cvd_modes():
    html = STUDIO.read_text(encoding="utf-8")
    el = Elements()
    el.feed(html)
    assert {
        "hueStrategy", "baseHue", "baseHueColor", "contrastPreset",
        "applyStrategy", "hueWheel", "lineAtlas", "markerAtlas",
        "visionComparison",
    } <= el.ids
    for method in (
        "equidistant", "golden", "qualitative", "analogous",
        "monochrome", "custom"
    ):
        assert f'value="{method}"' in html
    for mode in ("deuteranopia", "protanopia", "tritanopia"):
        assert f'data-mode="{mode}"' in html
    for logic in ("function methodHues(", "function toCvdRgb(",
                  "function renderVisionComparison(",
                  "function linePreview(", "function hueFromHex("):
        assert logic in html
    assert "prefers-reduced-motion:reduce" in html
    assert "frame.style.height" in STUDIO_PAGE.read_text(encoding="utf-8")



def test_print_safe_studio_defaults_adapt_to_color_count():
    html = STUDIO.read_text(encoding="utf-8")
    assert 'value="print-safe" selected' in html
    assert "contrastcolors.print_safe_luminances" in html
    assert "Math.pow((light+.05)/(dark+.05),1/(n-1))" in html
    assert "ratio<1||ratio>8" in html
