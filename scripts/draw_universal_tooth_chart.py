import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Ellipse, Polygon, FancyArrowPatch
from matplotlib.transforms import Affine2D

BG = "#f7f5f0"
INK = "#1f3a3a"
GREY = "#8a8f8c"
COL = {  # fill, edge
    "M": ("#e3efe8", "#6b9080"),   # molar sage
    "P": ("#e6eef8", "#5b7db1"),   # premolar dusty blue
    "C": ("#f8f1e4", "#c9a46a"),   # canine sand
    "I": ("#efecf7", "#8b7fb8"),   # incisor lavender
}
NAMES = {"M": "Molars", "P": "Premolars", "C": "Canines", "I": "Incisors"}

# Order as drawn left -> right on the page (= patient's right -> left)
up_types = ["M", "M", "M", "P", "P", "C", "I", "I", "I", "I", "C", "P", "P", "M", "M", "M"]
up_w = [9.5, 10, 10.5, 7, 7, 8, 6.5, 8.5, 8.5, 6.5, 8, 7, 7, 10.5, 10, 9.5]
up_uni = list(range(1, 17))
up_fdi = [18, 17, 16, 15, 14, 13, 12, 11, 21, 22, 23, 24, 25, 26, 27, 28]
up_name = ["3rd molar", "2nd molar", "1st molar", "2nd PM", "1st PM", "Canine", "Lateral", "Central"]

lo_types = up_types
lo_w = [10.5, 10.5, 11, 7, 7, 7, 6, 5.5, 5.5, 6, 7, 7, 7, 11, 10.5, 10.5]
lo_uni = list(range(32, 16, -1))
lo_fdi = [48, 47, 46, 45, 44, 43, 42, 41, 31, 32, 33, 34, 35, 36, 37, 38]


def arch_points(widths, a, b, y_mid, upper, gap=0.9):
    """Place teeth along a half ellipse by arc length.
    upper: U shape (incisors low, molars high). lower: inverted."""
    phis = np.linspace(-math.pi / 2, math.pi / 2, 4000)
    xs = a * np.sin(phis)
    ys = b * np.cos(phis)
    seg = np.hypot(np.diff(xs), np.diff(ys))
    s = np.concatenate([[0], np.cumsum(seg)])
    total = s[-1]
    scale = total / (sum(widths) + gap * (len(widths) - 1))
    out = []
    pos = 0
    for w in widths:
        centre = (pos + w / 2) * scale
        i = np.searchsorted(s, centre)
        i = min(max(i, 1), len(s) - 2)
        x, y = xs[i], ys[i]
        dx, dy = xs[i + 1] - xs[i - 1], ys[i + 1] - ys[i - 1]
        ang = math.degrees(math.atan2(dy, dx))
        if upper:
            y = y_mid - y      # incisors lowest -> U shape
            ang = -ang
        else:
            y = y_mid + y      # incisors highest -> inverted U
        # outward normal (away from arch centre)
        nx, ny = x, (y - (y_mid - 0 if not upper else y_mid))
        out.append((x, y, ang, w * scale))
        pos += w + gap
    return out


def draw_tooth(ax, x, y, ang, w, t):
    fill, edge = COL[t]
    tr = Affine2D().rotate_deg_around(x, y, ang) + ax.transData
    if t == "M":
        h = w * 0.95
        p = FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                           boxstyle=f"round,pad=0,rounding_size={w*0.32}",
                           fc=fill, ec=edge, lw=2.2, transform=tr, zorder=3)
        ax.add_patch(p)
        # cusp grooves (a cross)
        ax.plot([x - w * 0.28, x + w * 0.28], [y, y], color=edge, lw=1.1, alpha=.6, transform=tr, zorder=4)
        ax.plot([x, x], [y - h * 0.28, y + h * 0.28], color=edge, lw=1.1, alpha=.6, transform=tr, zorder=4)
    elif t == "P":
        h = w * 1.25
        p = Ellipse((x, y), w, h, fc=fill, ec=edge, lw=2.2, transform=tr, zorder=3)
        ax.add_patch(p)
        ax.plot([x - w * 0.3, x + w * 0.3], [y, y], color=edge, lw=1.1, alpha=.6, transform=tr, zorder=4)
    elif t == "C":
        h = w * 1.25
        pts = [(x - w / 2, y), (x, y - h / 2), (x + w / 2, y), (x, y + h / 2)]
        p = Polygon(pts, closed=True, fc=fill, ec=edge, lw=2.2, joinstyle="round",
                    transform=tr, zorder=3)
        ax.add_patch(p)
    else:
        h = w * 0.6
        p = FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                           boxstyle=f"round,pad=0,rounding_size={h*0.45}",
                           fc=fill, ec=edge, lw=2.2, transform=tr, zorder=3)
        ax.add_patch(p)


fig, ax = plt.subplots(figsize=(12, 15.5), dpi=150)
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_aspect("equal")
ax.axis("off")

A, B = 44, 52
UP_MID, LO_MID = 74, -74   # vertical centres of each arch's bounding area

up = arch_points(up_w, A, B, UP_MID, upper=True)
lo = arch_points(lo_w, A, B, LO_MID, upper=False)


def label(points, types, uni, fdi, upper):
    for (x, y, ang, w), t, u, f in zip(points, types, uni, fdi):
        draw_tooth(ax, x, y, ang, w, t)
        ax.text(x, y, str(u), ha="center", va="center", fontsize=15 if w > 8 else 13,
                fontweight="bold", color=INK, zorder=5, family="DejaVu Sans")
        # FDI label pushed outward from arch centre
        cx, cy = 0, (UP_MID - B * 0.15) if upper else (LO_MID + B * 0.15)
        cx, cy = 0, (UP_MID) if upper else (LO_MID)
        vx, vy = x - cx, y - cy
        n = math.hypot(vx, vy) or 1
        off = w * 0.95 + 3
        ax.text(x + vx / n * off, y + vy / n * off, f"FDI {f}", ha="center", va="center",
                fontsize=8.5, color=GREY, zorder=5)


label(up, up_types, up_uni, up_fdi, True)
label(lo, lo_types, lo_uni, lo_fdi, False)

# Arch titles
ax.text(0, UP_MID - 14, "UPPER  (maxillary)", ha="center", fontsize=17, fontweight="bold", color=INK)
ax.text(0, UP_MID - 21, "looking up into the upper jaw", ha="center", fontsize=10.5, color=GREY)
ax.text(0, LO_MID + 18, "LOWER  (mandibular)", ha="center", fontsize=17, fontweight="bold", color=INK)
ax.text(0, LO_MID + 11, "looking down at the lower jaw", ha="center", fontsize=10.5, color=GREY)

# Side labels
for yy in (UP_MID - 6, LO_MID + 6):
    pass
ax.text(-A - 2, 0, "PATIENT'S\nRIGHT", ha="center", va="center", fontsize=14, fontweight="bold", color="#c08497")
ax.text(A + 2, 0, "PATIENT'S\nLEFT", ha="center", va="center", fontsize=14, fontweight="bold", color="#c08497")
ax.text(0, 0, "midline", ha="center", va="center", fontsize=10, color=GREY, style="italic")
ax.plot([0, 0], [16, 24], color=GREY, lw=1, ls=":")
ax.plot([0, 0], [-16, -24], color=GREY, lw=1, ls=":")

# Loop arrows: upper left->right, drop down on right side, lower right->left
def arrow(p1, p2, rad):
    ax.add_patch(FancyArrowPatch(p1, p2, connectionstyle=f"arc3,rad={rad}",
                                 arrowstyle="-|>,head_length=9,head_width=5",
                                 color="#2f5d62", lw=2.4, zorder=2, alpha=.85))

arrow((-A + 6, UP_MID + 14), (A - 6, UP_MID + 14), -0.18)
arrow((A + 21, UP_MID - 6), (A + 21, LO_MID + 6), -0.12)
arrow((A - 6, LO_MID - 14), (-A + 6, LO_MID - 14), -0.18)
ax.text(0, UP_MID + 27, "START at #1  ➜  count across the top to #16", ha="center", fontsize=12, color="#2f5d62", fontweight="bold")
ax.text(A + 26.5, 0, "drop\ndown", ha="left", fontsize=11, color="#2f5d62", fontweight="bold")
ax.text(0, LO_MID - 32, "#17  ➜  count back across the bottom  ➜  END at #32", ha="center", fontsize=12, color="#2f5d62", fontweight="bold")

# Title
ax.text(0, UP_MID + 47, "US Universal Tooth Numbering", ha="center", fontsize=24, fontweight="bold", color=INK)
ax.text(0, UP_MID + 39.5, "Big number = Universal (USA, INBDE)     small grey = FDI (India)     drawn facing the patient",
        ha="center", fontsize=11, color=GREY)

# Legend chips
lx = -48
for i, t in enumerate(["M", "P", "C", "I"]):
    fill, edge = COL[t]
    xx = lx + i * 26
    ax.add_patch(FancyBboxPatch((xx, LO_MID - 46), 5, 5, boxstyle="round,pad=0,rounding_size=1.5",
                                fc=fill, ec=edge, lw=2))
    ax.text(xx + 7.5, LO_MID - 43.5, NAMES[t], va="center", fontsize=12, color=INK)

# Anchors box
ax.text(0, LO_MID - 55, "Anchors:  wisdom 1 · 16 · 17 · 32     first molars 3 · 14 · 19 · 30     canines 6 · 11 · 22 · 27     centrals 8 · 9 · 24 · 25",
        ha="center", fontsize=11, color=INK,
        bbox=dict(boxstyle="round,pad=0.7", fc="#f8f1e4", ec="#c9a46a", lw=1.5))

ax.set_xlim(-A - 30, A + 40)
ax.set_ylim(LO_MID - 62, UP_MID + 52)
plt.savefig("universal-tooth-chart.png",
            facecolor=BG, bbox_inches="tight", pad_inches=0.4)
print("ok")
