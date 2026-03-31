"""
Survey Data Visualisations
===========================
Run each cell in a Jupyter notebook.
Requires: matplotlib, numpy, pandas
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd

# ══════════════════════════════════════════════════════════════════════════════
# LOAD & PARSE CSV
# ══════════════════════════════════════════════════════════════════════════════

CSV_PATH = "/Users/riccardo/Desktop/File for graphs.csv"   # update path if needed

raw = pd.read_csv(CSV_PATH, header=None, sep=";")

def pct(val):
    """Convert a value like '87%' or 87 or '30' to a float."""
    if pd.isna(val):
        return 0.0
    s = str(val).strip().replace("%", "")
    try:
        return float(s)
    except ValueError:
        return 0.0

# ── Chart 1: Willingness to change habits (rows 1-2) ─────────────────────────
chart1_title  = str(raw.iloc[0, 0]).strip()
chart1_yes    = pct(raw.iloc[1, 1])   # 87
chart1_no     = pct(raw.iloc[2, 1])   # 13

# ── Chart 2: Medium-haul flights (rows 3-6) ──────────────────────────────────
chart2_title  = str(raw.iloc[3, 0]).strip()
flight_01_total   = pct(raw.iloc[4, 1])
flight_210_total  = pct(raw.iloc[5, 1])
flight_210_will   = pct(raw.iloc[5, 2])
flight_11_total   = pct(raw.iloc[6, 1])
flight_11_will    = pct(raw.iloc[6, 2])

# ── Chart 3: Turns off X machine (rows 7-9) ──────────────────────────────────
chart3_title  = str(raw.iloc[7, 0]).strip()
chart3_yes    = pct(raw.iloc[8, 1])
chart3_no     = pct(raw.iloc[9, 1])

# ── Chart 4: Recycles plastic (rows 10-12) ───────────────────────────────────
chart4_title  = str(raw.iloc[10, 0]).strip()
plastic_yes   = pct(raw.iloc[11, 1])
plastic_no    = pct(raw.iloc[12, 1])
plastic_no_will = pct(raw.iloc[12, 2])

print("Data loaded successfully:")
print(f"  Chart 1 – Yes: {chart1_yes}%  No: {chart1_no}%")
print(f"  Chart 2 – 0-1: {flight_01_total}%  |  2-10: {flight_210_total}% (willing: {flight_210_will}%)  |  >11: {flight_11_total}% (willing: {flight_11_will}%)")
print(f"  Chart 3 – Yes: {chart3_yes}%  No: {chart3_no}%")
print(f"  Chart 4 – Yes: {plastic_yes}%  No: {plastic_no}% (willing to change: {plastic_no_will}%)")

# ── Shared style (report-friendly) ───────────────────────────────────────────
plt.rcParams.update({
    "font.family":        "sans-serif",
    "font.size":          14,
    "axes.titlesize":     18,
    "axes.titleweight":   "bold",
    "axes.labelsize":     15,
    "xtick.labelsize":    14,
    "ytick.labelsize":    14,
    "legend.fontsize":    13,
    "figure.dpi":         150,
})

# Colour palette
YES_COLOR     = "#4C9BE8"   # blue  – yes / willing
NO_COLOR      = "#E8734C"   # orange – no / not willing
NEUTRAL_COLOR = "#A8C8A0"   # soft green – 0-1 / neutral category


# ══════════════════════════════════════════════════════════════════════════════
# CHART 1 – Simple pie: Willingness to change habits
# ══════════════════════════════════════════════════════════════════════════════

fig1, ax1 = plt.subplots(figsize=(8, 7))

labels1   = ["Yes", "No"]
sizes1    = [chart1_yes, chart1_no]
colors1   = [YES_COLOR, NO_COLOR]
explode1  = (0.04, 0.04)

wedges1, texts1, autotexts1 = ax1.pie(
    sizes1,
    labels=labels1,
    colors=colors1,
    explode=explode1,
    autopct="%1.0f%%",
    startangle=90,
    wedgeprops=dict(linewidth=1.8, edgecolor="white"),
    textprops=dict(fontsize=16),
)
for at in autotexts1:
    at.set_fontsize(16)
    at.set_fontweight("bold")
    at.set_color("white")

ax1.set_title(chart1_title, pad=20, wrap=True)
fig1.tight_layout(pad=2)
plt.savefig("chart1_willingness.png", dpi=150, bbox_inches="tight")
plt.show()
print("Chart 1 saved.")


# ══════════════════════════════════════════════════════════════════════════════
# CHART 2 – Stacked bar: Medium-haul flights within Europe per year
#            with willingness-to-change breakdown for 2-10 and >11
# ══════════════════════════════════════════════════════════════════════════════

willing_pct  = [0,
                flight_210_total * flight_210_will / 100,
                flight_11_total  * flight_11_will  / 100]
unwilling_pct= [0,
                flight_210_total * (100 - flight_210_will) / 100,
                flight_11_total  * (100 - flight_11_will)  / 100]
base_pct     = [flight_01_total, 0, 0]

flight_cats  = ["0-1", "2-10", ">11"]

fig2, ax2 = plt.subplots(figsize=(9, 7))

x = np.arange(len(flight_cats))
bar_w = 0.55

b1 = ax2.bar(x, base_pct,      bar_w, label="No data on willingness", color=NEUTRAL_COLOR,
             linewidth=1.5, edgecolor="white")
b2 = ax2.bar(x, willing_pct,   bar_w, label="Willing to change",       color=YES_COLOR,
             linewidth=1.5, edgecolor="white")
b3 = ax2.bar(x, unwilling_pct, bar_w, label="Not willing to change",    color=NO_COLOR,
             bottom=willing_pct, linewidth=1.5, edgecolor="white")

def annotate_bar(bars, bottoms=None):
    for i, bar in enumerate(bars):
        h = bar.get_height()
        if h < 1:
            continue
        bot = bottoms[i] if bottoms else 0
        ax2.text(
            bar.get_x() + bar.get_width() / 2,
            bot + h / 2,
            f"{h:.0f}%",
            ha="center", va="center",
            fontsize=14, fontweight="bold", color="white",
        )

annotate_bar(b1)
annotate_bar(b2)
annotate_bar(b3, bottoms=willing_pct)

ax2.set_xticks(x)
ax2.set_xticklabels(flight_cats)
ax2.set_ylabel("% of all respondents")
ax2.set_ylim(0, 85)
ax2.set_title(f"{chart2_title}\n(with willingness to use a more sustainable alternative)", pad=18)
ax2.legend(loc="upper right", framealpha=0.9)
ax2.spines[["top", "right"]].set_visible(False)
ax2.tick_params(axis="x", bottom=False)

fig2.tight_layout(pad=2)
plt.savefig("chart2_flights.png", dpi=150, bbox_inches="tight")
plt.show()
print("Chart 2 saved.")


# ══════════════════════════════════════════════════════════════════════════════
# CHART 3 – Simple pie: Turns off the X machine in the lab
# ══════════════════════════════════════════════════════════════════════════════

fig3, ax3 = plt.subplots(figsize=(8, 7))

labels3   = ["Yes", "No"]
sizes3    = [chart3_yes, chart3_no]
colors3   = [YES_COLOR, NO_COLOR]
explode3  = (0.04, 0.04)

wedges3, texts3, autotexts3 = ax3.pie(
    sizes3,
    labels=labels3,
    colors=colors3,
    explode=explode3,
    autopct="%1.0f%%",
    startangle=90,
    wedgeprops=dict(linewidth=1.8, edgecolor="white"),
    textprops=dict(fontsize=16),
)
for at in autotexts3:
    at.set_fontsize(16)
    at.set_fontweight("bold")
    at.set_color("white")

ax3.set_title(chart3_title, pad=20)
fig3.tight_layout(pad=2)
plt.savefig("chart3_machine.png", dpi=150, bbox_inches="tight")
plt.show()
print("Chart 3 saved.")


# ══════════════════════════════════════════════════════════════════════════════
# CHART 4 – Stacked bar + donut inset: Recycles plastic in the lab
#            with willingness-to-change breakdown for "No" respondents
# ══════════════════════════════════════════════════════════════════════════════

no_total   = plastic_no
no_willing = no_total * plastic_no_will / 100
no_not     = no_total * (100 - plastic_no_will) / 100

fig4, (ax4_main, ax4_inset) = plt.subplots(
    1, 2,
    figsize=(13, 7),
    gridspec_kw={"width_ratios": [1.3, 1]},
)

# ── Left: stacked bar ────────────────────────────────────────────────────────
cats     = ["Yes\n(recycles)", "No\n(doesn't recycle)"]
yes_bar  = [plastic_yes, 0]
will_bar = [0, no_willing]
nowill_bar = [0, no_not]

x4  = np.arange(len(cats))
bw4 = 0.5

ax4_main.bar(x4, yes_bar,    bw4, color=YES_COLOR, edgecolor="white", lw=1.5,
             label="Recycles / willing to change")
ax4_main.bar(x4, will_bar,   bw4, color=YES_COLOR, edgecolor="white", lw=1.5, alpha=0.65)
ax4_main.bar(x4, nowill_bar, bw4, color=NO_COLOR,  edgecolor="white", lw=1.5,
             bottom=will_bar, label="Not willing to change")

# Labels
ax4_main.text(0, plastic_yes / 2, f"{plastic_yes}%", ha="center", va="center",
              fontsize=15, fontweight="bold", color="white")
ax4_main.text(1, no_willing / 2, f"{no_willing:.0f}%\nwilling", ha="center", va="center",
              fontsize=13, fontweight="bold", color="white")
ax4_main.text(1, no_willing + no_not / 2, f"{no_not:.0f}%\nnot willing", ha="center", va="center",
              fontsize=13, fontweight="bold", color="white")

ax4_main.set_xticks(x4)
ax4_main.set_xticklabels(cats)
ax4_main.set_ylabel("% of all respondents")
ax4_main.set_ylim(0, 90)
ax4_main.spines[["top", "right"]].set_visible(False)
ax4_main.tick_params(axis="x", bottom=False)

legend_patches = [
    mpatches.Patch(color=YES_COLOR, label="Yes / Willing to change"),
    mpatches.Patch(color=NO_COLOR,  label="Not willing to change"),
]
ax4_main.legend(handles=legend_patches, loc="upper right", framealpha=0.9)

# ── Right: donut showing willingness breakdown of the "No" group ─────────────
donut_sizes  = [plastic_no_will, 100 - plastic_no_will]
donut_colors = [YES_COLOR, NO_COLOR]
donut_labels = [f"Willing\nto change\n({plastic_no_will:.0f}%)", f"Not willing\n({100-plastic_no_will:.0f}%)"]

ax4_inset.pie(
    donut_sizes,
    labels=donut_labels,
    colors=donut_colors,
    autopct="",
    startangle=90,
    wedgeprops=dict(width=0.52, linewidth=1.8, edgecolor="white"),
    textprops=dict(fontsize=13),
)

ax4_inset.text(0, 0, f"Non-\nrecyclers\n({plastic_no:.0f}%)", ha="center", va="center",
               fontsize=13, fontweight="bold", color="#444")
ax4_inset.set_title("Willingness to change\namong non-recyclers", fontsize=15, pad=14)

ax4_main.set_title(chart4_title, pad=18)
fig4.tight_layout(pad=2.5)
plt.savefig("chart4_plastic.png", dpi=150, bbox_inches="tight")
plt.show()
print("Chart 4 saved.")
