/* Dependency-free startup smoke test for the static Palette & Plot Studio.
 * The DOM stub covers the UI methods exercised during initialization, allowing
 * Node.js to catch blank-page runtime regressions without downloading a browser.
 */
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const html = fs.readFileSync(
  path.resolve(__dirname, "../docs/source/_static/studio.html"), "utf8"
);
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];
assert.equal(scripts.length, 1, "Expected one self-contained Studio script");

class FakeElement {
  constructor(id) {
    this.id = id;
    this.style = {};
    this.dataset = {};
    this.children = [];
    this.options = [];
    this.innerHTML = "";
    this.textContent = "";
    this.value = "";
    this.classList = { toggle() {} };
    this.listeners = {};
  }
  append(...nodes) { this.children.push(...nodes); }
  appendChild(node) { this.children.push(node); return node; }
  setAttribute(key, value) { this[key] = value; }
  addEventListener(type, handler) { this.listeners[type] = handler; }
  add(option) { this.options.push(option); }
  focus() {}
  select() {}
  trigger(type) {
    assert.equal(typeof this.listeners[type], "function", "No handler: " + this.id + "." + type);
    this.listeners[type]();
  }
}
const initial = {
  nColors: 5, ratio: 1.596, startY: 0.50, chroma: 0.13,
  hueStrategy: "equidistant", contrastPreset: "print-safe",
  baseHue: 25, baseHueColor: "#f16847",
  alpha: 0.8, background: "#ffffff", preserve: true,
  font: "Arial", rasterize: "true", dpi: 600,
  styleName: "heri", presetName: "paper_palette"
};
const all = new Map();
function element(id) {
  if (!all.has(id)) {
    const node = new FakeElement(id);
    if (Object.hasOwn(initial, id)) node.value = String(initial[id]);
    all.set(id, node);
  }
  return all.get(id);
}
const document = {
  getElementById: element,
  createElement: tag => new FakeElement(tag),
  querySelectorAll: () => [],
  documentElement: { scrollHeight: 3200 },
  body: new FakeElement("body"),
};
const context = {
  document,
  window: { parent: null, location: { origin: "https://example.test" } },
  localStorage: { getItem: () => null, setItem() {} },
  Option: class { constructor(label, value) {this.label = label;this.value = value;} },
  console,
};
const code = scripts[0][1].replace(
  /\}\)\(\);\s*$/,
  "globalThis.smoke={methodHues,toCvdRgb,series:()=>series,renderChart};})();"
);
assert.notEqual(code, scripts[0][1], "Could not expose Studio smoke hooks");
vm.runInNewContext(code, context, { timeout: 120000 });
assert.ok(context.smoke, "Studio script did not finish loading");
assert.deepEqual(Array.from(context.smoke.series(), s=>s.hue), [25,97,169,241,313]);
const initialCR = Number(element("ratio").value);
assert.ok(initialCR > 1.5 && initialCR < 1.7, "Five-color print-safe ratio missing");
assert.equal(Number(element("startY").value), 0.5);
assert.ok(element("chart").innerHTML.includes("<path"), "Plot SVG is empty");
assert.equal(element("visionComparison").children.length, 6, "Expected six viewing modes");
assert.ok(element("lineAtlas").innerHTML.includes("stroke-dasharray"), "Line previews missing");

element("hueStrategy").value = "golden";
element("hueStrategy").trigger("change");
assert.notEqual(context.smoke.series()[1].hue, 97, "Golden-angle selection did not change hue");
element("nColors").value = "3";
element("nColors").trigger("change");
assert.ok(Number(element("ratio").value) > 2.4, "Three colors need wider grayscale separation");
element("nColors").value = "10";
element("nColors").trigger("change");
assert.equal(context.smoke.series().length, 10);

element("hueStrategy").value = "equidistant";
element("nColors").value = "5";
element("hueStrategy").trigger("change");
assert.deepEqual(Array.from(context.smoke.series(), s=>s.hue), [25,97,169,241,313]);

const before = [1,0,0];
const after = context.smoke.toCvdRgb(before, "deuteranopia");
assert.equal(after.length, 3);
assert.ok(after.every(x=>Number.isFinite(x)&&x>=0&&x<=1));
assert.ok(after.some((v,i)=>Math.abs(v-before[i])>.1),"CVD preview did not modify red");
console.log("PASS: Studio starts; 5/10 colors, hue methods, SVG plots, dash atlas and CVD");
