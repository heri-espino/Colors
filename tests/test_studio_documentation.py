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
