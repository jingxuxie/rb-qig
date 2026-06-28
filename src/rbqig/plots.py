from __future__ import annotations

from pathlib import Path

from .io_utils import ensure_parent


COLORS = {
    "none": "#4b5563",
    "direct": "#2563eb",
    "llm_direct": "#7c3aed",
    "blanket_qi": "#dc2626",
    "rbqig_b2": "#059669",
    "rbqig_b4": "#0d9488",
    "rbqig_b6": "#65a30d",
}


LABELS = {
    "none": "None",
    "direct": "Direct",
    "llm_direct": "LLM direct",
    "blanket_qi": "Blanket QI",
    "rbqig_b2": "RB-QIG strict",
    "rbqig_b4": "RB-QIG balanced",
    "rbqig_b6": "RB-QIG utility",
}


def _svg_header(width: int, height: int) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<style>text{font-family:Arial,sans-serif;fill:#111827} .axis{stroke:#374151;stroke-width:1.2} .grid{stroke:#e5e7eb;stroke-width:1}</style>',
    ]


def _write_svg(path: str | Path, lines: list[str]) -> None:
    ensure_parent(path)
    Path(path).write_text("\n".join(lines + ["</svg>\n"]), encoding="utf-8")


def plot_privacy_utility(metrics: list[dict], path: str | Path) -> None:
    width, height = 780, 520
    left, right, top, bottom = 90, 40, 55, 85
    plot_w = width - left - right
    plot_h = height - top - bottom

    def xscale(value: float) -> float:
        return left + value * plot_w

    def yscale(value: float) -> float:
        return top + (1.0 - value) * plot_h

    lines = _svg_header(width, height)
    lines.append('<text x="90" y="30" font-size="20" font-weight="700">Privacy-utility frontier</text>')
    for tick in [0, 0.25, 0.5, 0.75, 1.0]:
        x = xscale(tick)
        y = yscale(tick)
        lines.append(f'<line class="grid" x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{height-bottom}"/>')
        lines.append(f'<line class="grid" x1="{left}" y1="{y:.1f}" x2="{width-right}" y2="{y:.1f}"/>')
        lines.append(f'<text x="{x-10:.1f}" y="{height-bottom+24}" font-size="12">{tick:.2g}</text>')
        lines.append(f'<text x="{left-42}" y="{y+4:.1f}" font-size="12">{tick:.2g}</text>')
    lines.append(f'<line class="axis" x1="{left}" y1="{height-bottom}" x2="{width-right}" y2="{height-bottom}"/>')
    lines.append(f'<line class="axis" x1="{left}" y1="{top}" x2="{left}" y2="{height-bottom}"/>')
    lines.append(f'<text x="{left + plot_w/2 - 95:.1f}" y="{height-26}" font-size="14">Utility fact preservation higher is better</text>')
    lines.append(f'<text x="20" y="{top + plot_h/2 + 90:.1f}" transform="rotate(-90 20 {top + plot_h/2 + 90:.1f})" font-size="14">Risk-weighted leakage lower is better</text>')

    for row in metrics:
        method = row["method"]
        x = xscale(float(row["utility_fact_preservation"]))
        y = yscale(float(row["risk_weighted_leakage"]))
        color = COLORS.get(method, "#111827")
        label = LABELS.get(method, method)
        lines.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="8" fill="{color}" opacity="0.92"/>')
        lines.append(f'<text x="{x+12:.1f}" y="{y+5:.1f}" font-size="12">{label}</text>')

    _write_svg(path, lines)


def plot_leakage_by_method(metrics: list[dict], path: str | Path) -> None:
    width, height = 850, 520
    left, right, top, bottom = 80, 30, 55, 120
    plot_w = width - left - right
    plot_h = height - top - bottom
    methods = [row["method"] for row in metrics]
    bar_group_w = plot_w / max(1, len(methods))
    bar_w = min(34, bar_group_w / 3.2)

    def yscale(value: float) -> float:
        return top + (1.0 - value) * plot_h

    lines = _svg_header(width, height)
    lines.append('<text x="80" y="30" font-size="20" font-weight="700">Residual leakage by method</text>')
    for tick in [0, 0.25, 0.5, 0.75, 1.0]:
        y = yscale(tick)
        lines.append(f'<line class="grid" x1="{left}" y1="{y:.1f}" x2="{width-right}" y2="{y:.1f}"/>')
        lines.append(f'<text x="{left-42}" y="{y+4:.1f}" font-size="12">{tick:.2g}</text>')
    lines.append(f'<line class="axis" x1="{left}" y1="{height-bottom}" x2="{width-right}" y2="{height-bottom}"/>')
    lines.append(f'<line class="axis" x1="{left}" y1="{top}" x2="{left}" y2="{height-bottom}"/>')

    for idx, row in enumerate(metrics):
        center = left + idx * bar_group_w + bar_group_w / 2
        values = [
            ("exact", float(row["exact_attribute_leakage"]), "#1d4ed8"),
            ("coarse", float(row["coarse_attribute_leakage"]), "#f97316"),
        ]
        for offset, (_, value, color) in zip([-bar_w / 1.8, bar_w / 1.8], values):
            x = center + offset - bar_w / 2
            y = yscale(value)
            h = height - bottom - y
            lines.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{h:.1f}" fill="{color}"/>')
        label = LABELS.get(row["method"], row["method"])
        lines.append(f'<text x="{center-42:.1f}" y="{height-bottom+24}" font-size="12" transform="rotate(30 {center-42:.1f} {height-bottom+24})">{label}</text>')

    legend_x = width - 210
    lines.append(f'<rect x="{legend_x}" y="58" width="14" height="14" fill="#1d4ed8"/>')
    lines.append(f'<text x="{legend_x+22}" y="70" font-size="13">Exact attribute leakage</text>')
    lines.append(f'<rect x="{legend_x}" y="82" width="14" height="14" fill="#f97316"/>')
    lines.append(f'<text x="{legend_x+22}" y="94" font-size="13">Coarse attribute leakage</text>')

    _write_svg(path, lines)
