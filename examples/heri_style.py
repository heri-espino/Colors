import numpy as np
import matplotlib.pyplot as plt

import contrastcolors as cc

cc.set_style("heri", font="Arial")

x = np.linspace(0, 2 * np.pi, 500)
colors = cc.color_palette(
    hues=[55, 20, 145, 210, 290],
    ratio=1.25,
    start_luminance=0.72,
)

fig, ax = plt.subplots(figsize=(6.5, 4.0))
for k, color in enumerate(colors):
    ax.plot(x, np.sin(x + 0.35 * k), color=color, label=fr"$k={k}$")

ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$f_k(x)$")
ax.legend()

cc.save_figure(fig, "heri_style_example.pdf")
