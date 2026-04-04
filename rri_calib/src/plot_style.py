
"""
Matplotlib style that closely matches ProPlot defaults

"""

import matplotlib as mpl


def set_plot_style():
    mpl.rcParams.update({

        # -------------------------------------------------
        # Font: match ProPlot default (TeX Gyre Heros first)
        # -------------------------------------------------
        "font.family": "sans-serif",
        "font.sans-serif": [
            "TeX Gyre Heros",
            "DejaVu Sans",
            "Bitstream Vera Sans",
            "Computer Modern Sans Serif",
            "Arial",
            "Avenir",
            "Fira Sans",
            "Helvetica",
            "Liberation Sans",
            "Nimbus Sans",
            "Verdana",
            "sans-serif",
        ],
        "font.size": 9.0,
        "font.weight": "normal",

        # -------------------------------------------------
        # Titles & labels (ProPlot style)
        # -------------------------------------------------
        "axes.titlesize": "medium",
        "axes.titleweight": "normal",   # ProPlot default
        "axes.labelsize": "medium",
        "axes.labelweight": "normal",
        "figure.titleweight": "bold",   # ProPlot suptitle is bold

        # -------------------------------------------------
        # Figure
        # -------------------------------------------------
        "figure.figsize": (4, 4),
        "figure.dpi": 100,
        "figure.facecolor": "#f4f4f4",
        "savefig.dpi": 1000,
        "savefig.facecolor": "white",
        "savefig.format": "pdf",

        # -------------------------------------------------
        # Axes
        # -------------------------------------------------
        "axes.edgecolor": "black",
        "axes.linewidth": 0.6,
        "axes.axisbelow": True,
        "axes.grid": True,

        # -------------------------------------------------
        # Grid (subtle, ProPlot-like)
        # -------------------------------------------------
        "grid.color": "black",
        "grid.alpha": 0.1,
        "grid.linestyle": "-",
        "grid.linewidth": 0.6,

        # -------------------------------------------------
        # Ticks
        # -------------------------------------------------
        "xtick.direction": "out",
        "ytick.direction": "out",
        "xtick.major.size": 4.0,
        "ytick.major.size": 4.0,
        "xtick.major.width": 0.6,
        "ytick.major.width": 0.6,
        "xtick.minor.visible": True,
        "ytick.minor.visible": True,
        "xtick.labelsize": "medium",
        "ytick.labelsize": "medium",

        # -------------------------------------------------
        # Lines
        # -------------------------------------------------
        "lines.linewidth": 1.5,
        "lines.markersize": 6.0,

        # -------------------------------------------------
        # Legend
        # -------------------------------------------------
        "legend.fontsize": "medium",
        "legend.frameon": True,
        "legend.edgecolor": "black",
        "legend.facecolor": "white",
        "legend.framealpha": 0.8,
        "legend.fancybox": False,

        # -------------------------------------------------
        # Math / formatter (match ProPlot)
        # -------------------------------------------------
        "mathtext.default": "regular",
        "axes.formatter.use_mathtext": False,
    })