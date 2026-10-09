"""
mlbook_style.py

Optional plotting style for ML teaching notebooks.

Usage in notebook
-----------------
try:
    from mlbook_style import (
        apply_style,
        COLORS,
        ALIASES,
        pale,
        get_color,
        savefig,
    )
    apply_style()
except ImportError:
    print("Custom style not found. Using default matplotlib settings.")

Design goals
------------
- projector contrast
- colorblind safety
- stable semantic roles across notebooks
- light variants for untuned / intermediate models
"""

from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import to_rgb, to_hex


# ---------------------------------------------------------------------
# Core palette (Okabe-Ito inspired / adapted)
# Good projector contrast and strong colorblind robustness
# ---------------------------------------------------------------------
COLORS = {
    # data
    "data": "#009E73",          # bluish green
    "data_secondary": "#56B4E9", # sky blue
    "data_unlabeled": "#7F7F7F", # neutral gray

    # classes / groups
    "class_1": "#0072B2",       # blue
    "class_2": "#E69F00",       # orange
    "class_3": "#CC79A7",       # reddish purple
    "class_4": "#D55E00",       # vermillion

    # models / predictions
    "model_1": "#0072B2",       # blue
    "model_2": "#CC79A7",       # reddish purple
    "model_3": "#D55E00",       # vermillion
    "model_4": "#E69F00",       # orange
    "model_5": "#009E73",       # green
    "model_6": "#56B4E9",       # sky blue

    # special roles
    "baseline": "#7F7F7F",      # gray
    "highlight": "#000000",     # black
    "error": "#D55E00",         # reuse vermillion
}


# ---------------------------------------------------------------------
# Optional aliases for readability in notebooks
# You can use either COLORS["model_1"] or ALIASES["linear"]
# ---------------------------------------------------------------------
ALIASES = {
    # dataset roles
    "actual": COLORS["data"],
    "train": COLORS["data"],
    "test": COLORS["data_secondary"],
    "unlabeled": COLORS["data_unlabeled"],

    # baseline
    "dummy": COLORS["baseline"],

    # common model names
    "linear": COLORS["model_1"],
    "linear_log": COLORS["model_2"],
    "tree": COLORS["model_3"],
    "knn": COLORS["model_4"],
    "poly": COLORS["model_5"],

    # classes
    "positive": COLORS["class_1"],
    "negative": COLORS["class_2"],
}


# Ordered sequence for automatic multi-model plotting
MODEL_SEQUENCE = [
    COLORS["model_1"],
    COLORS["model_2"],
    COLORS["model_3"],
    COLORS["model_4"],
    COLORS["model_5"],
    COLORS["model_6"],
]


def pale(hex_color: str, alpha: float = 0.45) -> str:
    """
    Blend a color with white to make it lighter.

    Parameters
    ----------
    hex_color : str
        Base color, e.g. '#0072B2'
    alpha : float
        0.0 -> original color
        1.0 -> white

    Recommended:
    - alpha ~ 0.35 to 0.55 for 'non-tuned' / preliminary models
    """
    rgb = to_rgb(hex_color)
    pale_rgb = tuple(c + (1.0 - c) * alpha for c in rgb)
    return to_hex(pale_rgb)


def get_color(name: str, tuned: bool = True, alpha_light: float = 0.45) -> str:
    """
    Resolve a color by semantic role or alias.

    Examples
    --------
    get_color("tree")                 -> tuned tree color
    get_color("tree", tuned=False)    -> lighter untuned tree color
    get_color("model_3")              -> model_3 color
    """
    if name in ALIASES:
        color = ALIASES[name]
    elif name in COLORS:
        color = COLORS[name]
    else:
        raise KeyError(f"Unknown color role/alias: {name}")

    return color if tuned else pale(color, alpha=alpha_light)


def apply_style() -> None:
    """Apply plotting defaults globally."""
    sns.set_theme(
        style="whitegrid",
        context="notebook",
        font="DejaVu Sans",
    )

    plt.rcParams.update({
        # figure
        "figure.figsize": (10, 5.8),
        "figure.dpi": 110,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",

        # titles / labels
        "axes.titlesize": 16,
        "axes.labelsize": 13,
        "axes.titleweight": "bold",

        # ticks
        "xtick.labelsize": 11,
        "ytick.labelsize": 11,

        # legend
        "legend.fontsize": 11,
        "legend.frameon": True,

        # lines / markers
        "lines.linewidth": 2.4,
        "lines.markersize": 6,

        # clean look
        "axes.spines.top": False,
        "axes.spines.right": False,
        "grid.alpha": 0.25,
    })


def savefig(filename: str, folder: str = "figures") -> Path:
    """
    Save current figure into a folder and return the path.
    """
    folder_path = Path(folder)
    folder_path.mkdir(parents=True, exist_ok=True)
    path = folder_path / filename
    plt.savefig(path)
    return path